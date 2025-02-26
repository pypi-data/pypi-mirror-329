import json
from pydantic import BaseModel
from typing import Any, Dict, Optional, List, Union
from xpander_sdk import (
    ToolCall,
    ToolCallType,
    ToolCallResult,
    ILocalTool,
    LLMProvider,
)
from .base import SDKAdapter
import chainlit as cl


class ChainlitAdapter(SDKAdapter):
    """
    Adapter class for integrating Chainlit with xpander.ai.

    This class extends SDKAdapter and provides methods to interact with Chainlit while utilizing
    xpander.ai's capabilities. It manages tool calls, tasks, and thread IDs.

    Attributes:
        agent (SDKAdapter): Inherited agent instance.
    """

    def __init__(
        self,
        api_key: str,
        agent_id: str,
        base_url: Optional[str] = None,
        organization_id: Optional[str] = None,
    ):
        """
        Initialize the ChainlitAdapter.

        Args:
            api_key (str): The API key for authentication with xpander.ai.
            agent_id (str): The ID of the xpander.ai agent.
            base_url (Optional[str], optional): The base URL for the xpander.ai API. Defaults to None.
            organization_id (Optional[str], optional): The organization ID, if applicable. Defaults to None.
        """
        super().__init__(api_key, agent_id, base_url, organization_id)
        self.agent.disable_agent_end_tool()  # No need since SmolAgents handles it.

    def get_system_prompt(self) -> str:
        """
        Retrieve the system prompt with additional instructions for interactive chat.

        Returns:
            str: The formatted system prompt.
        """
        return super().get_system_prompt() + (
            "\nImportant: You are an assistant engaged in an interactive chat. "
            "Always communicate your reasoning, decisions, and actions to the user. "
            "When performing tool calls, clearly explain what you are doing, why you are doing it, "
            "and what results you expect. "
            "Provide insights into your thought process at each step to ensure transparency and clarity."
        )

    def get_tools(self, llm_provider: LLMProvider = LLMProvider.OPEN_AI) -> List[Any]:
        """
        Retrieve the tools available for the specified LLM provider.

        Args:
            llm_provider (LLMProvider, optional): The LLM provider. Defaults to LLMProvider.OPEN_AI.

        Returns:
            List[Any]: A list of available tools.
        """
        return self.agent.get_tools(llm_provider=llm_provider)

    def get_thread_id(self) -> Optional[str]:
        """
        Retrieve the thread ID associated with the Chainlit session.

        Returns:
            Optional[str]: The thread ID if available, otherwise None.
        """
        return cl.user_session.get("xpander_thread_id", None)

    def add_task(
        self,
        input: Any,
        files: Optional[List[Any]] = None,
        use_worker: bool = False,
        thread_id: Optional[str] = None,
    ):
        """
        Add a task to the agent and associate it with the Chainlit thread.

        Args:
            input (Any): The input for the task.
            files (Optional[List[Any]], optional): Additional files for processing. Defaults to None.
            use_worker (bool, optional): Whether to use a worker. Defaults to False.
            thread_id (Optional[str], optional): The thread ID for association. Defaults to None.
        """
        super().add_task(input, files, use_worker, thread_id)
        cl.user_session.set("xpander_thread_id", self.agent.execution.memory_thread_id)

    def aggregate_tool_calls_stream(
        self,
        tool_calls: Optional[Dict[int, ToolCall]] = None,
        tool_call_requests: Optional[List[Any]] = None,
    ) -> Dict[int, ToolCall]:
        """
        Aggregate tool calls from tool call requests.

        Args:
            tool_calls (Optional[Dict[int, ToolCall]], optional): Existing tool calls. Defaults to None.
            tool_call_requests (Optional[List[Any]], optional): List of tool call requests. Defaults to None.

        Returns:
            Dict[int, ToolCall]: Aggregated tool calls.
        """
        if not tool_calls:
            tool_calls = {}

        if tool_call_requests:
            for tc in tool_call_requests:
                if tc.index not in tool_calls:
                    tool_calls[tc.index] = ToolCall(
                        name=tc.function.name,
                        tool_call_id=tc.id,
                        type=ToolCallType.XPANDER,
                        payload="",
                    )
                else:
                    tool_calls[tc.index].payload += tc.function.arguments

        return tool_calls

    @cl.step(type="tool")
    def process_tool_calls(self, tool_calls: Dict[int, ToolCall]):
        """
        Process tool calls by formatting their payloads and executing them.

        Args:
            tool_calls (Dict[int, ToolCall]): The tool calls to process.
        """
        for tc in tool_calls.values():
            if tc.payload:
                tc.payload = json.loads(tc.payload)

        tool_calls_list = list(tool_calls.values())

        self.agent.add_messages(
            messages=[
                {
                    "role": "assistant",
                    "content": "",
                    "tool_calls": [
                        {
                            "name": tc.name,
                            "payload": json.dumps(tc.payload),
                            "tool_call_id": tc.tool_call_id,
                        }
                        for tc in tool_calls_list
                    ],
                }
            ]
        )
        
        for tool_call in tool_calls.values():
            current_step = cl.context.current_step
            current_step.name = tool_call.name
            current_step.input = tool_call.payload
            tool_call_result = self.agent.run_tool(tool=tool_call)
            current_step.output = tool_call_result.result
            current_step.language = "json"

        # Reset tool calls
        tool_calls.clear()
