import json
import os
from typing import List, Any

from openai import OpenAI, RateLimitError
from openai.types.chat import ChatCompletion, ChatCompletionMessage, ChatCompletionMessageToolCall

from menschmachine.event import events
from menschmachine.llm.types import FileRequestCallbackType, QuestionCallbackType, CreateFileCallbackType, \
    SearchFilesCallbackType, \
    ApiInterface, ApiResponse, MaxNumberOfLoops, ApiCosts, Agent, ModelRegistry
from menschmachine.log import get_logger
from menschmachine.util import symetric_dict

_MODEL_REGISTRY = ModelRegistry("haiku")

# Register models with their aliases
_MODEL_REGISTRY.register("anthropic/claude-3-haiku:beta", ["haiku3", "claude-haiku3", "haiku-3", "claude-haiku-3"],
                         0.25, 1.25)
_MODEL_REGISTRY.register("anthropic/claude-3.5-sonnet:beta", ["sonnet", "claude-sonnet"], 3, 15)
_MODEL_REGISTRY.register("anthropic/claude-3-7-sonnet:beta", ["sonnet-3.7", "claude-sonnet-3.7"], 3, 15)
_MODEL_REGISTRY.register("anthropic/claude-3-opus:beta", ["opus", "claude-opus"], 15, 75)
_MODEL_REGISTRY.register("openai/gpt-4o-2024-11-20", ["gpt4o", "gpt4", "gpt-4o"], 2.5, 10)
_MODEL_REGISTRY.register("openai/o1-mini-2024-09-12", ["gpt4o-mini", "gpt4-mini"], 3, 12)
_MODEL_REGISTRY.register("openai/o1", ["o1", "gpt-01"], 15, 60)
_MODEL_REGISTRY.register("openai/o3-mini", ["o3-mini", "gpt-03-mini", "gpt-03mini"], 1.1, 4.4)
_MODEL_REGISTRY.register("deepseek/deepseek-chat", ["deepseek-chat"], 0.14, 0.28)
_MODEL_REGISTRY.register("deepseek/deepseek-r1", ["deepseek", "r1"], 0.55, 2.19)
_MODEL_REGISTRY.register("google/gemini-pro-1.5", ["gemini-pro"], 1.25, 5)
_MODEL_REGISTRY.register("google/gemini-flash-1.5", ["gemini-flash"], 0.075, 0.3)
_MODEL_REGISTRY.register("openai/o1-preview-2024-09-12", ["o1", "gpt-o1", "o1-preview"], 15, 60)
_MODEL_REGISTRY.register("anthropic/claude-3-5-haiku:beta",
                         ["haiku-3.5", "claude-haiku-3.5", "claude-haiku",
                          "haiku-35", "claude-haiku-35", "haiku",
                          "haiku-3-5", "claude-haiku-3-5"],
                         1., 5.)
_MODEL_REGISTRY.register("perplexity/sonar", ["perplexity", "sonar"], 1., 1.)


class OpenRouterApi(ApiInterface):

    def __init__(self):
        super().__init__()

    def raw(self, messages: list[dict],
            tools: list[dict] = None,
            tool_choice: dict | str | None = None,
            model: str = None,
            max_tokens: int = 4000,
            temperature=0.0,
            ) -> ChatCompletion:
        client = self.create_client()
        extra_headers = self.get_extra_headers()
        model = self.get_model(model)
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
                    extra_headers=extra_headers
                )
            else:
                if tool_choice is None:
                    result = client.chat.completions.create(
                        max_tokens=max_tokens,
                        temperature=temperature,
                        messages=messages,
                        tools=tools,
                        model=model,
                        extra_headers=extra_headers
                    )
                else:
                    result = client.chat.completions.create(
                        max_tokens=max_tokens,
                        temperature=temperature,
                        messages=messages,
                        tools=tools,
                        tool_choice=tool_choice,
                        model=model,
                        extra_headers=extra_headers
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

    def get_extra_headers(self):
        extra_headers = {
            "HTTP-Referer": "https://menschmachine.com",
            "X-Title": "MenschMachine"
        }
        return extra_headers

    def create_client(self):
        client = OpenAI(
            api_key=os.environ["OPENROUTER_API_KEY"],
            base_url="https://openrouter.ai/api/v1"
        )
        return client

    @staticmethod
    def token_counts_from_response(response):
        usage = response.usage
        if usage is not None:
            prompt_tokens = usage.prompt_tokens
            completion_tokens = usage.completion_tokens
        else:
            prompt_tokens = -1
            completion_tokens = -1
        return completion_tokens, prompt_tokens

    def is_model_supported(self, model: str) -> bool:
        return self.get_model_registry().is_supported(model)

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
        return self.ask("ping", self.get_long_name("haiku"))

    def ask(self,
            prompt: str,
            model: str = None,
            max_tokens: int = 4096,
            temperature=0.0,
            assistant_msg=None) -> ApiResponse:

        messages = [{"role": "user", "content": prompt}]
        if assistant_msg:
            messages.append({"role": "assistant", "content": assistant_msg})

        model = self.get_model(model)
        response = self.raw(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature
        )
        completion_tokens, prompt_tokens = self.token_counts_from_response(response)
        costs = self.get_api_costs(model, prompt_tokens, completion_tokens)
        answer = response.choices[0].message.content

        return ApiResponse(message=answer, error=None, costs=costs)

    async def with_tools_loop(self, prompt: str,
                              file_content_callback: FileRequestCallbackType,
                              follow_up_question_callback: QuestionCallbackType,
                              search_files_callback: SearchFilesCallbackType,
                              create_file_callback: CreateFileCallbackType,
                              model: str,
                              max_tokens: int = 100000,
                              temperature: float = 0.1) -> ApiResponse:
        model = self.get_model(model)
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_file_content",
                    "description": "Get the content of a file in the repository",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "filepath": {
                                "type": "string",
                                "description": "The complete path of the file as presented in the file_list array"
                            }
                        },
                        "required": ["filepath"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "create_file",
                    "description": "Create a new file in the repository, use only for files which do not exist yet. If the file exists, create a patch in the xml format shown to you.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "filepath": {
                                "type": "string",
                                "description": "The complete path of the file to create"
                            },
                            "content": {
                                "type": "string",
                                "description": "The content of the new file to create"
                            }
                        },
                        "required": ["filepath", "content"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "search_files",
                    "description": "Perform a regex search across all files in the repository, returning a list of all filenames matching the regex.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "regex": {
                                "type": "string",
                                "description": "The regular expression pattern to search for. Uses Rust regex syntax.",
                            }
                        },
                        "required": ["regex"],
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "ask_followup_question",
                    "description": "Ask the user a question to gather additional information needed to complete the task.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "question": {
                                "type": "string",
                                "description": "The question to ask the user. This should be a clear, specific question that addresses the information you need.",
                            },
                        },
                        "required": ["question"],
                    }
                }
            },
        ]

        messages: list[dict[str, str] | ChatCompletionMessage] = [{"role": "user", "content": prompt}]
        files = {}
        costs = self.get_api_costs(model, 0, 0)

        async def loop() -> ApiResponse:

            response = self.raw(
                model=model,
                messages=messages,
                tools=tools,
                tool_choice="auto",
                max_tokens=max_tokens,
                temperature=temperature,
            )

            message = response.choices[0].message
            messages.append(message)
            completion_tokens, prompt_tokens = self.token_counts_from_response(response)
            costs.add(self.get_api_costs(model, prompt_tokens, completion_tokens))

            if message.tool_calls is not None and len(message.tool_calls) > 0:
                tool_calls: List[ChatCompletionMessageToolCall] = message.tool_calls
                tool_call_results = list()
                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    function_args = tool_call.function.arguments
                    tool_call_id = tool_call.id

                    if function_name == "get_file_content":
                        tool_call_results.append(
                            {"role": "tool", "tool_call_id": tool_call_id,
                             "content": await get_file_content_exec(function_args)})
                    elif function_name == "ask_followup_question":
                        tool_call_results.append(
                            {"role": "tool", "tool_call_id": tool_call_id,
                             "content": await ask_followup_question(function_args)})
                    elif function_name == "search_files":
                        tool_call_results.append(
                            {"role": "tool", "tool_call_id": tool_call_id,
                             "content": await search_files(function_args)})
                    elif function_name == "create_file":
                        tool_call_results.append(
                            {"role": "tool", "tool_call_id": tool_call_id, "content": await create_file(function_args)})

                messages.extend(tool_call_results)
                return await loop()
            else:
                return ApiResponse(message=message.content, error=None, costs=costs, files=files)

        async def create_file(args):
            args_dict = json.loads(args)
            filepath = args_dict['filepath']
            content = args_dict['content']
            return await create_file_callback(filepath, content)

        async def search_files(args):
            args_dict = json.loads(args)
            q = args_dict['regex']
            files_ = await search_files_callback(q)
            return json.dumps(files_)

        async def ask_followup_question(args):
            args_dict = json.loads(args)
            q = args_dict['question']
            a = await follow_up_question_callback(q)
            return a

        async def get_file_content_exec(args):
            args_dict = json.loads(args)
            files_requested = [args_dict['filepath']]
            file_content_result = await file_content_callback(files_requested)
            for file in file_content_result:
                files[file] = file_content_result[file]
            return json.dumps(file_content_result)

        return await loop()

    async def loop(self,
                   uuid: str,
                   model: str,
                   agent_map: dict[str, Agent],
                   nr_of_loops: int,
                   max_nr_of_loops: int,
                   messages: list,
                   temperature: float,
                   costs: ApiCosts) -> Any:

        async def append_next_step(tool_result: Any, _response: str, function_name: str, _tool_use_id: str):
            messages.append({"role": "assistant", "content": _response})
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": _tool_use_id,
                    "name": function_name,
                    "content": json.dumps(tool_result)
                })
            events.emit(f"/mm/agent/step/{uuid}", uuid, "openrouter", messages)

        nr_of_loops += 1
        get_logger().debug(f"Loop number: {nr_of_loops}")
        if nr_of_loops > max_nr_of_loops:
            get_logger().warning("Max number of loops reached")
            raise MaxNumberOfLoops()
        tools = self.tools_from_agent_map(agent_map)
        try:
            response = self.raw(
                model=model,
                messages=messages,
                tools=tools,
                temperature=temperature,
                max_tokens=4096
            )

            completion_tokens, prompt_tokens = self.token_counts_from_response(response)
            costs.add(self.get_api_costs(model, prompt_tokens, completion_tokens))
            choice = response.choices[0]
            message = choice.message
            get_logger().debug(f"Choice: {choice}")
            if choice.finish_reason == 'tool_calls':

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
            elif choice.finish_reason == 'end_turn' or choice.finish_reason == 'STOP':
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

        in_price, out_price = self.get_prices(model)
        return costs(prompt_tokens, in_price) + costs(completion_tokens, out_price)

    def get_model(self, model):
        return self.get_model_registry().get_model(model)

    def get_model_registry(self) -> ModelRegistry:
        return _MODEL_REGISTRY

    def get_prices(self, model):
        return self.get_model_registry().get_prices(model)

    def get_long_name(self, param):
        return self.get_model_registry().get_long_name(param)
