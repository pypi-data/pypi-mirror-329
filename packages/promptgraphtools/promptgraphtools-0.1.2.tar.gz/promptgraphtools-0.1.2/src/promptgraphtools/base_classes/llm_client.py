from typing import Any, Dict, List, Optional

class LLMClient:
    """
    Abstract interface for a Large Language Model (LLM).
    """

    async def start_chat(self, history: Optional[List[Dict[str, str]]] = None) -> None:
        """
        Starts a new chat session with the LLM.

        :param history: Optional chat history to initialize the chat with.
        """
        raise NotImplementedError("start_chat method must be implemented.")

    async def send_message(self, message: str) -> Dict[str, Any]:
        """
        Sends a message to the active chat session and gets the model's response.

        :param message: The message to send to the LLM.
        :returns: A dictionary with the model's response.
        """
        raise NotImplementedError("send_message method must be implemented.")

    async def run(self, prompt_parts: List[str]) -> Dict[str, Any]:
        """
        Generates content using the LLM in a non-chat setting.

        Args:
            prompt_parts (List[str]): The prepared prompt sections to send to the LLM.

        Returns:
            Dict[str, Any]: A dictionary containing the output text.
        """
        raise NotImplementedError("run method must be implemented.")

    def component_run_stats(self, prompt_parts: List[str], replies: List[str]) -> Dict[str, Any]:
        """
        Calculates and returns component run statistics, including token usage.

        Args:
            prompt_parts (List[str]): The input prompt parts.
            replies (List[str]): The LLM's replies.

        Returns:
            Dict[str, Any]: A dictionary containing component run statistics.
        """
        raise NotImplementedError("component_run_stats method must be implemented.")
