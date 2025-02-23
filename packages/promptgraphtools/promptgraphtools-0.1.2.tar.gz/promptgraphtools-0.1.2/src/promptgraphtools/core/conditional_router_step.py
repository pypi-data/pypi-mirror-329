from typing import Any, Dict, List, Optional

from ..base_classes.step_like import StepLike

class ConditionalRouterStep(StepLike):
    """
    A conditional router step that delegates execution to one of several steps based on
    the presence of keys in the input. The router is configured with a dictionary mapping
    route keys to steps. When run, it searches the input for these keys:
    
    - If exactly one route key is found, its associated step is executed.
    - If none are found, and a default step is provided, the default step is executed.
    - If none are found and no default is provided, an error is raised.
    - If more than one is found, an error is raised due to ambiguity.
    """
    
    def __init__(
        self,
        name: str,
        steps: Dict[str, StepLike],
        default: Optional[StepLike] = None,
        required_inputs: Optional[List[str]] = None,
        required_outputs: Optional[List[str]] = None,
    ):
        """
        Args:
            name: Name of this router.
            steps: A dictionary mapping route keys to StepLike instances. These keys are expected
                   to appear in the inputs to select the route.
            default: An optional default StepLike to execute if none of the route keys are present.
            required_inputs: A list of required input keys.
            required_outputs: A list of required output keys.
        """
        self._name = name
        self._steps = steps
        self._default = default
        self._required_inputs = required_inputs or []
        self._required_outputs = required_outputs or []
    
    def name(self) -> str:
        return self._name
    
    def required_inputs(self) -> List[str]:
        return self._required_inputs
    
    def required_outputs(self) -> List[str]:
        return self._required_outputs
    
    async def run_async(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Delegates execution to an appropriate step based on the keys found in the inputs.
        
        The method looks for any keys in the input that match the keys provided to the router.
        If exactly one such key is found, the corresponding step is executed.
        If none or more than one key is found, the method either falls back to the default step
        (if provided) or raises a ValueError.
        """
        # Identify the keys in the input that match any of the keys provided in the steps.
        matching_keys = [key for key in self._steps if key in inputs]
        
        if len(matching_keys) > 1:
            raise ValueError(
                f"Ambiguous routing: multiple route keys found in input: {matching_keys}"
            )
        elif len(matching_keys) == 1:
            route_key = matching_keys[0]
            step = self._steps[route_key]
        else:
            if self._default is not None:
                step = self._default
            else:
                raise ValueError("No routing key found in input and no default route provided.")
        
        return await step.run_async(inputs)
