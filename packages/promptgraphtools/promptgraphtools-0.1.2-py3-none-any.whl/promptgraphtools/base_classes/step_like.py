from abc import ABC, abstractmethod
from typing import Any, Dict, List, Set
from jinja2.sandbox import SandboxedEnvironment
from jinja2 import meta

class DynamicInput:
    def __init__(self, input: str, codebase_file_data: Any = None):
        self.input = input
        self.codebase_file_data = codebase_file_data


class StepLike(ABC):
    """
    Base interface for DAG steps, with built-in optional templating utilities.
    """

    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def required_inputs(self) -> List[str]:
        pass

    @abstractmethod
    def required_outputs(self) -> List[str]:
        pass

    @abstractmethod
    async def run_async(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        pass
    
    def validate_inputs(self, inputs: Dict[str, Any]) -> None:
        if not self._required_inputs:
            raise ValueError(f"Step '{self.name()}' must provide at least one input.")
        
        for key in self._required_inputs:
            if key not in inputs:
                raise ValueError(
                    f"Step '{self.name()}' missing required input '{key}'."
                )
    
    def validate_outputs(self, outputs: Dict[str, Any]) -> None:
        if not self._required_outputs:
            raise ValueError(f"Step '{self.name()}' must provide at least one output.")
        
        for key in self._required_outputs:
            if key not in outputs:
                raise ValueError(
                    f"Step '{self.name()}' missing required output '{key}'."
                )

    def _apply_special_templating_to_dynamic_inputs(self, parts: List[DynamicInput]) -> List[str]:
        new_parts = []
        for part in parts:
            codebase_file_data = part.codebase_file_data
            if codebase_file_data:
                new_parts.append(
                    f"<code-metadata-reference>\n"
                    f"Path: `{codebase_file_data.path}`\n"
                    f"Full File Contents: {part.input}\n"
                    f"Symbols In File As Well As Symbol References: {codebase_file_data.symbols}\n"
                    f"</code-metadata-reference>"
                )
            else:
                new_parts.append(f"{part.input}\n")
        return new_parts

    def _get_template_variables(self, template: str) -> Set[str]:
        env = SandboxedEnvironment()
        parsed_content = env.parse(template)
        variables = meta.find_undeclared_variables(parsed_content)
        return variables

    def _assert_has_required_input_keys(self, parts_input_keys: Set[str], parts: Dict[str, Any]) -> None:
        for key in parts_input_keys:
            if key not in parts:
                if key in self.required_inputs():
                    raise ValueError(f"Missing required part input: {key}")
                else:
                    parts[key] = ""

    def _split_template_into_parts(self, template: str, variables: Set[str]) -> List[str]:
        parts = []
        last_end = 0
        sorted_variables = sorted(variables, key=lambda var: template.find(f"{{{{{var}}}}}"))

        for var in sorted_variables:
            var_placeholder = f"{{{{{var}}}}}"
            start = template.find(var_placeholder)
            if start != -1:
                if last_end != start:
                    parts.append(template[last_end:start])
                parts.append(var)
                last_end = start + len(var_placeholder)
        if last_end < len(template):
            parts.append(template[last_end:])
        return parts

    # TODO: these aren't vertex parts, redo this eventually
    def _build_llm_vertex_parts(
        self,
        template: str,
        inputs: Dict[str, Any]
    ) -> List[str]:
        """
        This function reproduces the exact snippet from your GeminiWithSearch `run()` method:
          1) Collect template variables
          2) Assert required placeholders exist in inputs
          3) Split template into literal segments and placeholders
          4) For each placeholder 'inputs', call `_apply_special_templating_to_dynamic_inputs`
             otherwise just use `inputs[placeholder]` or literal text
          5) Return the final 'vertex_parts'
        """
        parts_input_keys = self._get_template_variables(template)
        self._assert_has_required_input_keys(parts_input_keys, inputs)
        prompt_parts = self._split_template_into_parts(template, parts_input_keys)

        vertex_parts: List[str] = []

        DYNAMIC_INPUTS_KEYWORD = "inputs"
        for part in prompt_parts:
            if part in inputs and part != DYNAMIC_INPUTS_KEYWORD:
                # e.g. variable placeholder -> input data
                vertex_parts.append(inputs[part])
            elif part == DYNAMIC_INPUTS_KEYWORD:
                # apply special templating logic for dynamic inputs
                dyn_inputs = self._apply_special_templating_to_dynamic_inputs(inputs[part])
                vertex_parts.extend(dyn_inputs)
            else:
                vertex_parts.append(part)

        return vertex_parts
