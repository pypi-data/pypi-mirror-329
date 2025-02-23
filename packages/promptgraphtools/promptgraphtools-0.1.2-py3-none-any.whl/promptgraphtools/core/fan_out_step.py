import asyncio
from typing import List, Dict, Any, Optional, Callable
from ..base_classes.step_like import StepLike
from .step_graph import StepGraph

dynamic_input = "dynamic_input"
MAX_CONCURRENCY = 5


class FanOutStep(StepLike):
    """
    A hybrid step that supports dynamic fan-out over a list of inputs,
    with functionality for generic Python functions, templates, LLM clients, and StepGraphs.

    Parameters:
      step_name (str): Name of the step.
      input_key (str): The key in the inputs dict containing the list to process.
      output_key (str): The key for the combined output in the results dict.
      function (Optional[Callable]): A function or coroutine to process each input.
      template (Optional[str]): A template for LLM-based processing.
      llm_client (Optional[Any]): An LLM client for processing inputs using a template.
      step_graph (Optional[StepGraph]): A StepGraph instance to be executed for each item.
      concurrency (int): Maximum number of items processed concurrently (max=10).
      batch_mode (bool): If True, process items in discrete batches of size `concurrency`.
                         If False, process items in a continuous stream limited by the semaphore.
    """

    def __init__(
        self,
        step_name: str,
        input_key: str,
        output_key: str = "results",
        function: Optional[Callable] = None,
        template: Optional[str] = None,
        llm_client: Optional[Any] = None,
        step_graph: Optional[StepGraph] = None,
        concurrency: int = MAX_CONCURRENCY,
        batch_mode: bool = True,
    ):
        self._name = step_name
        self._input_key = input_key
        self._output_key = output_key
        self._function = function
        self._template = template
        self._llm_client = llm_client
        self._step_graph = step_graph
        self._required_inputs = [self._input_key]
        self._required_outputs = [self._output_key]

        self._concurrency = min(concurrency, MAX_CONCURRENCY)
        self._semaphore = asyncio.Semaphore(self._concurrency)
        self._batch_mode = batch_mode

    def name(self) -> str:
        return self._name

    def required_inputs(self) -> List[str]:
        return self._required_inputs

    def required_outputs(self) -> List[str]:
        return self._required_outputs

    async def run_async(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processes a list of inputs dynamically using the provided function,
        template, LLM client, or StepGraph.
        """
        self.validate_inputs(inputs)

        input_list = inputs.get(self._input_key, [])
        if not isinstance(input_list, list):
            raise ValueError(
                f"Input '{self._input_key}' must be a list, but got {type(input_list).__name__}."
            )

        # Approach 1: "Batch mode" => process in chunks of size self._concurrency
        if self._batch_mode:
            results = []
            # Process items in slices
            for i in range(0, len(input_list), self._concurrency):
                chunk = input_list[i : i + self._concurrency]
                tasks = [self._process_item(item, inputs) for item in chunk]
                chunk_results = await asyncio.gather(*tasks)
                results.extend(chunk_results)

        # Approach 2: "Always up to N running" => create all tasks at once,
        # rely on the semaphore to limit how many run concurrently
        else:
            tasks = [
                asyncio.create_task(self._process_item(item, inputs))
                for item in input_list
            ]
            results = await asyncio.gather(*tasks)

        out_dict = {self._output_key: results}
        self.validate_outputs(out_dict)
        return out_dict

    async def _process_item(
        self, item: Any, inputs: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Processes a single item using the specified logic:
        - Template + LLM client
        - Function
        - StepGraph
        """
        # Ensure concurrency is limited by the semaphore. Even in batch mode,
        # you can keep this so you have the option to limit concurrency *inside each batch*.
        async with self._semaphore:
            # Assign the current item to the dynamic input key
            inputs[dynamic_input] = item

            # Option A: Process using template + LLM client
            if self._template and self._llm_client:
                response = await self._llm_client.run(
                    self._build_llm_vertex_parts(self._template, inputs)
                )
                return {"item": item, "output": response["output"]}

            # Option B: Process using a generic Python function
            elif self._function:
                # If the function is a coroutine, await it
                if asyncio.iscoroutinefunction(self._function):
                    return await self._function(item, inputs)
                else:
                    return self._function(item, inputs)

            # Option C: Process using a StepGraph
            elif self._step_graph:
                graph_inputs = inputs.copy()
                # Run the StepGraph with the item-specific inputs
                graph_output = await self._step_graph.run_async(graph_inputs)
                required_outputs = self._step_graph.required_outputs()
                output_key = "output" if len(required_outputs) == 0 else required_outputs[0]
                return {"item": item, "output": graph_output[output_key]}

            else:
                raise ValueError(
                    f"Step '{self._name}' requires either a function, a template + llm_client, or a step_graph."
                )
