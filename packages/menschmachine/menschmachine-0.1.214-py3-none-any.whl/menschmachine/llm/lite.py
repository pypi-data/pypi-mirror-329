import json
import os
from typing import List, Any

import litellm
from openai import OpenAI, RateLimitError
from openai.types.chat import ChatCompletion, ChatCompletionMessageToolCall

from menschmachine.event import events
from menschmachine.llm.types import FileRequestCallbackType, QuestionCallbackType, CreateFileCallbackType, \
    SearchFilesCallbackType, \
    ApiInterface, ApiResponse, MaxNumberOfLoops, ApiCosts, Agent, ModelRegistry
from menschmachine.log import get_logger
from menschmachine.util import symetric_dict

MODEL_REGISTRY = ModelRegistry("haiku")

# Register models with their aliases
MODEL_REGISTRY.register("litellm-haiku", ["haiku", "claude-haiku"], 0.25, 1.25, "anthropic/claude-3-haiku-20240307")
MODEL_REGISTRY.register("litellm-sonnet", ["sonnet", "claude-sonnet"], 3, 15, "anthropic/claude-3-5-sonnet-20240620")
MODEL_REGISTRY.register("litellm-opus", ["opus", "claude-opus"], 15, 75, "anthropic/claude-3-opus-20240229")
MODEL_REGISTRY.register("litellm-gpt-4o", ["gpt4o", "gpt4", "gpt-4o"], 2.5, 10, "openai/gpt-4o")
MODEL_REGISTRY.register("litellm-o1-mini", ["gpt4o-mini", "gpt4-mini"], 3, 12)
MODEL_REGISTRY.register("litellm-gemini-pro", ["gemini-pro"], 1.25, 5)
MODEL_REGISTRY.register("litellm-gemini-flash", ["gemini-flash"], 0.075, 0.3, "gemini/gemini-1.5-flash-latest")
MODEL_REGISTRY.register("litellm-o1-preview-2024-09-12", ["o1", "gpt-o1", "o1-preview"], 15, 60)


def raw(messages: list[dict],
        tools: list[dict] = None,
        tool_choice: dict | str | None = None,
        model: str = None,
        max_tokens: int = 4000,
        temperature=0.0,
        ) -> ChatCompletion:
    client = create_client()
    model = MODEL_REGISTRY.get_model(model)
    official_name = MODEL_REGISTRY.get_official_name(model)
    assert litellm.supports_function_calling(model=official_name)

    if temperature is None:
        temperature = 0.0
    try:
        result = None
        if tools is None:
            result = client.chat.completions.create(
                max_tokens=max_tokens,
                temperature=temperature,
                messages=messages,
                model=model,
            )
        else:
            if tool_choice is None:
                result = client.chat.completions.create(
                    max_tokens=max_tokens,
                    temperature=temperature,
                    messages=messages,
                    tools=tools,
                    model=model,
                )
            else:
                result = client.chat.completions.create(
                    max_tokens=max_tokens,
                    temperature=temperature,
                    messages=messages,
                    tools=tools,
                    tool_choice=tool_choice,
                    model=model,
                )
        return result

    except RateLimitError as e:
        headers = e.response.headers
        rate_limit_info = {
            'x-ratelimit-limit-requests': headers.get('x-ratelimit-limit-requests'),
            'x-ratelimit-remaining-requests': headers.get('x-ratelimit-remaining-requests'),
            'x-ratelimit-reset-requests': headers.get('x-ratelimit-reset-requests'),
            'x-ratelimit-limit-tokens': headers.get('x-ratelimit-limit-tokens'),
            'x-ratelimit-remaining-tokens': headers.get('x-ratelimit-remaining-tokens'),
            'x-ratelimit-reset-tokens': headers.get('x-ratelimit-reset-tokens'),
            'retry-after': headers.get('retry-after'),
        }

        # Create a log message to show exceeded limits
        exceeded_limits = []

        # Check for exceeded limits
        if int(rate_limit_info['x-ratelimit-remaining-tokens']) == 0:
            exceeded_limits.append('Tokens limit exceeded')

        if int(rate_limit_info['x-ratelimit-remaining-requests']) == 0:
            exceeded_limits.append('Requests limit exceeded')

        # Prepare the log message
        if exceeded_limits:
            get_logger().error(f"Rate limit exceed: [{', '.join(exceeded_limits)}]")
            exceeded_info = {key: value for key, value in rate_limit_info.items() if value is not None}
            get_logger().debug(f"Rate limits exceeded: {exceeded_info}")
        else:
            get_logger().info("No rate limits exceeded.")
        raise e


def create_client():
    client = OpenAI(
        api_key=os.environ["LITELLM_API_KEY"],
        base_url="http://code.thefamouscat.com:4000/api/v1"
    )
    return client


class LiteLlmApi(ApiInterface):

    def __init__(self):
        super().__init__()

    def is_model_supported(self, model: str) -> bool:
        return MODEL_REGISTRY.is_supported(model)

    async def agent_loop(self,
                         uuid: str,
                         prompt: str,
                         agent_ids: list[str],
                         model: str,
                         max_tokens: int = 4096,
                         temperature: float = 0.1,
                         max_nr_of_loops: int = 10) -> ApiResponse:

        costs = self.get_api_costs(model, 0, 0)
        agent_map = self.get_agent_map(agent_ids)
        tools = self.tools_from_agent_map(agent_map)
        messages = [
            {
                "role": "user",
                "content": prompt,
            }
        ]
        events.emit(f"/mm/agent/init/{uuid}", uuid, "openrouter", symetric_dict(prompt, model, tools, messages))
        return await self.loop(uuid, model, agent_map, 0, max_nr_of_loops, messages, temperature, costs)

    def tools_from_agent_map(self, agent_map):
        tools = []
        for agent_id in agent_map:
            agent = agent_map[agent_id]
            properties, required_properties = self.properties_for_agent(agent)
            input_schema = self.input_schema_from_properties(properties, required_properties)
            tools.append(
                {
                    "type": "function",
                    "function": {
                        "name": agent.name,
                        "description": agent.description,
                        "parameters": input_schema
                    }
                }
            )
        return tools

    def ping(self) -> ApiResponse:
        return self.ask("ping", MODEL_REGISTRY.get_long_name("haiku"))

    def ask(self,
            prompt: str,
            model: str = None,
            max_tokens: int = 4096,
            temperature=0.0,
            assistant_msg=None) -> ApiResponse:

        messages = [{"role": "user", "content": prompt}]
        if assistant_msg:
            messages.append({"role": "assistant", "content": assistant_msg})

        model = MODEL_REGISTRY.get_model(model)
        response = raw(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature
        )
        costs = self.get_api_costs(model, response.usage.prompt_tokens, response.usage.completion_tokens)
        answer = response.choices[0].message.content
        return ApiResponse(message=answer, error=None, costs=costs)

    async def with_tools_loop(self, prompt: str,
                              file_content_callback: FileRequestCallbackType,
                              follow_up_question_callback: QuestionCallbackType,
                              search_files_callback: SearchFilesCallbackType,
                              create_file_callback: CreateFileCallbackType,
                              model: str,
                              max_tokens: int = 4000,
                              temperature: float = 0.1) -> ApiResponse:
        raise NotImplementedError("deprecated, use loop()")

    async def loop(self,
                   uuid: str,
                   model: str,
                   agent_map: dict[str, Agent],
                   nr_of_loops: int,
                   max_nr_of_loops: int,
                   messages: list,
                   temperature: float,
                   costs: ApiCosts) -> Any:

        async def append_next_step(tool_result: Any, _response: str, function_name: str, tool_call_id: str):
            messages.append({"role": "assistant", "content": _response})
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call_id,
                    "name": function_name,
                    "content": json.dumps(tool_result),
                })
            events.emit(f"/mm/agent/step/{uuid}", uuid, "openrouter", messages)

        nr_of_loops += 1
        get_logger().debug(f"Loop number: {nr_of_loops}")
        if nr_of_loops > max_nr_of_loops:
            get_logger().warning("Max number of loops reached")
            raise MaxNumberOfLoops()
        tools = self.tools_from_agent_map(agent_map)
        try:
            response = raw(
                model=model,
                messages=messages,
                tools=tools,
                temperature=temperature,
                max_tokens=4096
            )
            costs.add(self.get_api_costs(model, response.usage.prompt_tokens, response.usage.completion_tokens))
            choice = response.choices[0]
            message = choice.message
            get_logger().debug(f"Choice: {choice}")
            if choice.finish_reason == 'tool_calls' or (message.tool_calls is not None and len(message.tool_calls) > 0):

                tool_calls: List[ChatCompletionMessageToolCall] = message.tool_calls
                tool_call_results = list[dict]()
                for tool_call in tool_calls:
                    function_args = tool_call.function.arguments
                    tool_use_id = tool_call.id
                    tool_name = tool_call.function.name
                    get_logger().info(f"Tool requested: {tool_name}")
                    get_logger().debug(f"Tool request messsage: {message}")
                    if tool_name not in agent_map:
                        raise ValueError(f"Unknown tool requested: {tool_name}")
                    # noinspection DuplicatedCode
                    try:
                        await agent_map[tool_name].call(uuid,
                                                        json.loads(function_args),
                                                        response,
                                                        tool_use_id,
                                                        append_next_step)
                    except Exception as e:
                        self.handle_tool_call_exception(message, tool_name, e)
                    await self.loop(
                        uuid,
                        model,
                        agent_map,
                        nr_of_loops,
                        max_nr_of_loops,
                        messages,
                        temperature,
                        costs)
                messages.extend(tool_call_results)
                return await self.loop(
                    uuid,
                    model,
                    agent_map,
                    nr_of_loops,
                    max_nr_of_loops,
                    messages,
                    temperature,
                    costs)
            elif choice.finish_reason == 'end_turn' or choice.finish_reason.lower() == 'stop':
                get_logger().info("Agent loop completed successfully")
                events.emit(f"/mm/agent/completed/{uuid}", uuid, "openrouter", symetric_dict(response, costs))
                return ApiResponse(message=message.content, error=None, costs=costs)
            else:
                get_logger().warning(f"Unexpected stop reason: {choice.finish_reason}")
                return ApiResponse(message=message.content, error=None, costs=costs)
        except Exception as e:
            events.emit(f"/mm/agent/error/{uuid}", uuid, "openrouter", symetric_dict(e, costs))
            get_logger().error(f"Error in agent loop: {str(e)}")
            raise

    def estimate_costs(self, model: str, prompt_tokens: int, completion_tokens: int) -> float:
        def costs(nr_tokens, price_per_million: float):
            return (nr_tokens * (price_per_million / (1000. * 1000.))) / 100.  # in cent

        in_price, out_price = MODEL_REGISTRY.get_prices(model)
        return costs(prompt_tokens, in_price) + costs(completion_tokens, out_price)
