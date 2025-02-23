import asyncio
from typing import Any, Dict, List, Optional, Set
from collections import deque

from ..base_classes.step_like import StepLike

class StepGraph(StepLike):
    """
    A concurrency-first DAG of steps (which can themselves be StepGraph instances).
    Steps that have no unsatisfied dependencies run in parallel in each layer.

    Supports iterative re-runs if any step sets 'should_rerun' = True in its output.
    Automatically propagates updated outputs from the previous iteration into the inputs.
    """

    def __init__(
        self,
        graph_name: str,
        steps: List[StepLike],
        dependencies: Dict[str, List[str]],
        required_inputs: Optional[List[str]] = None,
        required_outputs: Optional[List[str]] = None,
        max_iterations: int = 50,
    ):
        self._graph_name = graph_name
        self._steps = {s.name(): s for s in steps}
        self._dependencies = dependencies
        self._required_inputs = required_inputs or []
        self._required_outputs = required_outputs or []
        self._max_iterations = max_iterations

        # Validate references
        for step_name, deps in dependencies.items():
            if step_name not in self._steps:
                raise ValueError(f"Dependency error: step '{step_name}' not in graph.")
            for d in deps:
                if d not in self._steps:
                    raise ValueError(f"Dependency error: unknown dep '{d}' for '{step_name}'.")

    def name(self) -> str:
        return self._graph_name

    def required_inputs(self) -> List[str]:
        return self._required_inputs

    def required_outputs(self) -> List[str]:
        return self._required_outputs

    async def _execute_layer(
        self,
        layer: Set[str],
        inputs: Dict[str, Any],
        output_context: Dict[str, Any],
    ) -> None:
        """
        Executes all steps in the given layer concurrently. 
        Merges each step's outputs into both `output_context` and `inputs`
        so subsequent layers can see them.
        """
        # Snapshot 'inputs' for each step to avoid them mutating the same dict in parallel
        tasks = [
            self._execute_step(self._steps[step_name], dict(inputs))
            for step_name in layer
        ]
        results_list = await asyncio.gather(*tasks)

        # Merge each step's output into the shared contexts
        for res in results_list:
            output_context.update(res)
            inputs.update(res)

    async def _execute_step(self, step_obj: StepLike, local_ctx: Dict[str, Any]) -> Dict[str, Any]:
        """Awaits the step's async run()."""
        return await step_obj.run_async(local_ctx)

    async def run_async(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run the step graph asynchronously, re-running from the top if 'should_rerun' = True
        after any layer. The loop ends once no layer sets should_rerun or we hit max_iterations.
        """
        iteration_count = 0

        while True:
            iteration_count += 1
            self.validate_inputs(inputs)

            output_context: Dict[str, Any] = {}
            layers = self._topological_sort()

            # Walk through each layer in topological order
            for layer in layers:
                # 1) Run the layer
                await self._execute_layer(layer, inputs, output_context)

                # 2) If any step signaled should_rerun, short-circuit this iteration
                #    so that we immediately re-run from the top in the next iteration
                if output_context.get("should_rerun", False):
                    # Merge outputs into inputs so next iteration sees the new data
                    inputs.update(output_context)
                    break
            else:
                # If we never hit the 'break' above => no short-circuit => iteration is complete
                self.validate_outputs(output_context)

                # If overall graph is done or iteration limit is reached, break out
                if (
                    iteration_count < self._max_iterations
                    and self._iteration_condition_check(output_context)
                ):
                    inputs.update(output_context)
                    continue
                else:
                    # Merge final outputs
                    inputs.update(output_context)
                    break

            # If we short-circuited the for-loop, check iteration limit
            if iteration_count >= self._max_iterations:
                raise RuntimeError(
                    f"Graph '{self._graph_name}' exceeded max_iterations: {self._max_iterations}"
                )
            # Otherwise, re-run from the top in a fresh iteration

        return inputs

    def _iteration_condition_check(self, output_context: Dict[str, Any]) -> bool:
        """
        Default check for 'should_rerun' = True in the outputs.
        Override or replace if you have a different condition.
        """
        return bool(output_context.get("should_rerun", False))

    def _topological_sort(self) -> List[Set[str]]:
        """
        Standard topological sort for concurrency in layers:
        - Each layer is a set of steps with no remaining dependencies.
        - Steps in the same layer can run in parallel.
        """
        in_degree = {n: 0 for n in self._steps}
        for node, deps in self._dependencies.items():
            for d in deps:
                in_degree[node] += 1

        queue = deque([n for n, deg in in_degree.items() if deg == 0])
        layers: List[Set[str]] = []

        while queue:
            layer_size = len(queue)
            layer_nodes = set()
            for _ in range(layer_size):
                node = queue.popleft()
                layer_nodes.add(node)
            if layer_nodes:
                layers.append(layer_nodes)

            # Decrement in-degree for children that depend on these layer nodes
            for node in layer_nodes:
                for child, deps in self._dependencies.items():
                    if node in deps:
                        in_degree[child] -= 1
                        if in_degree[child] == 0:
                            queue.append(child)

        # Detect cycle if any node still has in_degree > 0
        if any(deg > 0 for deg in in_degree.values()):
            raise ValueError("Cycle detected in step graph.")

        return layers
