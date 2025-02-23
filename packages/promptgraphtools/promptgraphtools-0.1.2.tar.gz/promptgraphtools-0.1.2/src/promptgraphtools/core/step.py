import asyncio
from asyncio.log import logger
from typing import List, Dict, Any, Optional

from ..base_classes.step_like import StepLike
from ..base_classes.llm_client import LLMClient


class Step(StepLike):
    """
    A single step that can do:
      - Generic Python function if provided
      - LLM templating if template + llm_client (Gemini wrapper) are provided, with optional chat-based continuation
        until an end tag is found.  Now correctly handling List[str] for prompt parts.
    """

    def __init__(
        self,
        step_name: str,
        required_inputs: Optional[List[str]] = None,
        required_outputs: Optional[List[str]] = None,
        function: Optional[Any] = None,
        template: Optional[str] = None,
        llm_client: Optional[LLMClient] = None,
        end_tag: Optional[str] = None,
        end_instructions: Optional[str] = None,
    ):
        self._name = step_name
        self._required_inputs = required_inputs or []
        self._required_outputs = required_outputs or []
        self._function = function
        self._template = template
        self._llm_client = llm_client
        self._end_tag = end_tag
        self._end_instructions = end_instructions
        self._chat_session = None

    def name(self) -> str:
        return self._name

    def required_inputs(self) -> List[str]:
        return self._required_inputs

    def required_outputs(self) -> List[str]:
        return self._required_outputs

    async def run_async(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes the step's logic asynchronously.

        If a template and LLM client are provided, it performs LLM-based templating.
        Optionally, it continues in chat mode until an end tag is found.
        If a function is provided, it executes the Python function.

        Args:
            inputs (Dict[str, Any]): Input data for the step.

        Returns:
            Dict[str, Any]: Output data from the step, with the first required output
                              as the key and the accumulated LLM output as the value if
                              using template/LLM, or the output of the function if used.
        """
        self.validate_inputs(inputs)

        logger.info(f"Running step: {self._name}\n")

        # Option A: Template and LLM Client Logic
        if self._template and self._llm_client:
            vertex_parts = self._build_llm_vertex_parts(self._template, inputs)
            prompt_text = " ".join(vertex_parts)

            accumulated_output = ""
            found_end_tag = False

            # Initial LLM Call
            llm_run_response_dict = await self._llm_client.run(vertex_parts)
            initial_llm_output_replies = llm_run_response_dict.get('replies', [''])
            initial_llm_output = initial_llm_output_replies[0] if initial_llm_output_replies is not None and initial_llm_output_replies[0] is not None and len(initial_llm_output_replies) > 0 else (self._end_tag or "")
            accumulated_output += initial_llm_output

            logger.info(f"\n\n----Current step output: {initial_llm_output} \n\n----")

            if self._end_tag and self._end_tag in accumulated_output:
                accumulated_output = accumulated_output.replace(self._end_tag, "").strip()
                found_end_tag = True
            elif self._end_tag is not None:
                # Start Chat Session with initial prompt and initial LLM response as history
                await self._llm_client.start_chat(history=[{'user': [prompt_text], 'model': [initial_llm_output]}])

                while not found_end_tag:
                    continuation_prompt = "You didn't finish your generation, seamlessly keep going from exactly where you left off without extra commentary, just like you are finishing a story, while you continue to follow the instructions I gave you at the start of our conversation. You are also **required** follow these instructions for what to include at the end of your generation: " + self._end_instructions
                    llm_chat_response_dict = await self._llm_client.send_message(message=continuation_prompt)
                    chat_turn_model_output_replies = llm_chat_response_dict.get('replies', [''])
                    chat_turn_model_output = chat_turn_model_output_replies[0] if chat_turn_model_output_replies else ''

                    accumulated_output += chat_turn_model_output

                    if self._end_tag in accumulated_output:
                        logger.info(f"End tag '{self._end_tag}' found.\nFinal output chunk: {chat_turn_model_output} \n\n End of continuation mode stream.\n")
                        accumulated_output = accumulated_output.replace(self._end_tag, "").strip()
                        found_end_tag = True
                        break
                    else:
                        logger.info(f"\nEnd tag '{self._end_tag}' still not found in continuation. Keep going...\n Current accumulated output chunk: {chat_turn_model_output} \n...")

            response = {}
            if accumulated_output is not None:
                first_key_of_required_outputs = next(iter(self._required_outputs))
                response[first_key_of_required_outputs] = accumulated_output
            else:
                logger.info(f"Malformed step output.\n")

            self.validate_outputs(response)
            return response

        # Option B: Function Logic (Normal Python Function)
        elif self._function:
            # If the function is a coroutine, await it
            if asyncio.iscoroutinefunction(self._function):
                out_dict = await self._function(inputs)
            else:
                out_dict = self._function(inputs)
            self.validate_outputs(out_dict)
            return out_dict

        # Option C: Error - Neither template+LLM nor function provided
        else:
            raise ValueError(
                f"Step '{self._name}' has neither a function nor a template + llm_client."
            )
