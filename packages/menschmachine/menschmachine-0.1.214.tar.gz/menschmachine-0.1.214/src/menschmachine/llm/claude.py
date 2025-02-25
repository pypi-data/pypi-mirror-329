import os
from typing import Any

from anthropic import Anthropic, RateLimitError
from anthropic.types import Message

from menschmachine.event import events
from menschmachine.llm.types import FileRequestCallbackType, QuestionCallbackType, CreateFileCallbackType, \
    SearchFilesCallbackType, \
    ApiInterface, ApiResponse, MaxNumberOfLoops, ApiCosts, Agent
from menschmachine.log import get_logger
from menschmachine.patch import Patch
from menschmachine.util import symetric_dict

models = {
    "claude-3-haiku-20240307": {
        "max_input_tokens": 200000,
        "max_output_tokens": 4096,
    },
    "claude-3-5-sonnet-20241022": {
        "max_input_tokens": 200000,
        "max_output_tokens": 8192,
    },
    "claude-3-5-haiku-20241022": {
        "max_input_tokens": 200000,
        "max_output_tokens": 4096,
    },
    "claude-3-7-sonnet-20250219": {
        "max_input_tokens": 200000,
        "max_output_tokens": 8192,
    }
}


def get_max_output_tokens(model: str) -> int:
    if model in models:
        return models[model]["max_output_tokens"]
    else:
        return 4096


_LATEST_HAIKU_MODEL = "claude-3-haiku-20240307"
_LATEST_HAIKU_3_5_MODEL = "claude-3-5-haiku-20241022"
_LATEST_SONNET_3_7_MODEL = "claude-3-7-sonnet-20250219"
_LATEST_SONNET_MODEL = _LATEST_SONNET_3_7_MODEL
_LATEST_OPUS_MODEL = "claude-3-opus-20240229"


def raw(messages: list[dict],
        tools: list[dict] = None,
        tool_choice: dict = None,
        model: str = _LATEST_HAIKU_MODEL,
        temperature=0.0,
        ) -> Message:
    client = Anthropic()
    model = get_model(model)
    if temperature is None:
        temperature = 0.0
    if tools is None or len(tools) == 0:
        return client.messages.create(
            max_tokens=get_max_output_tokens(model),
            temperature=temperature,
            messages=messages,
            model=model,
        )
    else:
        if tool_choice is None:
            return client.messages.create(
                max_tokens=get_max_output_tokens(model),
                temperature=temperature,
                messages=messages,
                tools=tools,
                model=model,
            )
        else:
            return client.messages.create(
                max_tokens=get_max_output_tokens(model),
                temperature=temperature,
                messages=messages,
                tools=tools,
                tool_choice=tool_choice,
                model=model,
            )


def get_model(model: str) -> str:
    if "UNIVERSAL_MODEL" in os.environ:
        model = os.environ["UNIVERSAL_MODEL"]
    if model is None:
        return _LATEST_HAIKU_MODEL
    if _get_supported_model(model) is not None:
        return _get_supported_model(model)
    return model


def _get_supported_model(model: str) -> str | None:
    if model is not None:
        if model.lower() == "haiku":
            return _LATEST_HAIKU_MODEL
        elif model.lower() == "haiku-3.5":
            return _LATEST_HAIKU_3_5_MODEL
        elif model.lower() == "sonnet":
            return _LATEST_SONNET_MODEL
        elif model.lower() == "sonnet-3.7":
            return _LATEST_SONNET_3_7_MODEL
        elif model.lower() == "opus":
            return _LATEST_OPUS_MODEL
    return None


class ClaudeApi(ApiInterface):

    def __init__(self):
        super().__init__()

    def estimate_costs(self, model: str, prompt_tokens: int, completion_tokens: int) -> float:
        def costs(nr_tokens, price_per_million: float):
            return (nr_tokens * (price_per_million / (1000. * 1000.))) / 100.  # in cent

        if "sonnet" in model:
            return costs(prompt_tokens, 3) + costs(completion_tokens, 15)
        elif "haiku-3.5" in model:
            return costs(prompt_tokens, 1) + costs(completion_tokens, 5)
        elif "haiku" in model:
            return costs(prompt_tokens, 0.25) + costs(completion_tokens, 1.25)
        elif "opus" in model:
            return costs(prompt_tokens, 15) + costs(completion_tokens, 75)
        else:
            return -1.

    def is_model_supported(self, model: str) -> bool:
        return _get_supported_model(model) is not None

    def ping(self) -> ApiResponse:
        return self.ask("ping", _LATEST_HAIKU_MODEL)

    async def with_tools_loop(self,
                              prompt: str,
                              file_content_callback: FileRequestCallbackType,
                              follow_up_question_callback: QuestionCallbackType,
                              search_files_callback: SearchFilesCallbackType,
                              create_file_callback: CreateFileCallbackType,
                              model: str = _LATEST_HAIKU_MODEL,
                              max_tokens: int = models[_LATEST_HAIKU_MODEL]["max_output_tokens"],
                              temperature: float = 0.1,
                              ) -> ApiResponse:
        tools = [
            {
                "name": "get_file_content",
                "description": "Get the content of a file in the repository",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "filepath": {
                            "type": "string",
                            "description": "The complete path of the file as presented in the file_list array"
                        }
                    },
                    "required": ["filepath"]
                }
            },
            {
                "name": "create_file",
                "description": "Create a new file in the repository, use only for files which do not exist yet. If the file exists, create a patch in the xml format shown to you.",
                "input_schema": {
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
            },
            {
                "name": "search_files",
                "description":
                    "Perform a regex search across all files in the repository, returning a list of all filenames matching the regex.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "regex": {
                            "type": "string",
                            "description": "The regular expression pattern to search for. Uses Rust regex syntax.",
                        }
                    },
                    "required": ["regex"],
                },
            },
            {
                "name": "ask_followup_question",
                "description":
                    """Ask the user a question to gather additional information needed to complete the task. 
                    This tool should be used when you encounter ambiguities, need clarification, or require more details to proceed effectively. 
                    It allows for interactive problem-solving by enabling direct communication with the user. 
                    Use this tool judiciously to maintain a balance between gathering necessary information and avoiding excessive back-and-forth.",
                    """,
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "question": {
                            "type": "string",
                            "description":
                                "The question to ask the user. This should be a clear, specific question that addresses the information you need.",
                        },
                    },
                    "required": ["question"],
                },
            },
        ]
        messages = [
            {
                "role": "user",
                "content": prompt,
            }
        ]
        files = {}
        costs = self.get_api_costs(model, 0, 0)

        async def loop() -> ApiResponse:
            response = raw(messages=messages, tools=tools, model=model, temperature=temperature)
            costs.add(self.get_api_costs(model, response.usage.input_tokens, response.usage.output_tokens))
            if response.stop_reason == 'tool_use':
                msg = response.content[len(response.content) - 1]
                tool_use_id = msg.id
                tool_name = msg.name
                get_logger().info(f"Tool requested: {tool_name}")
                if tool_name == "get_file_content":
                    await get_file_content_exec(msg, response, tool_use_id)
                elif tool_name == "ask_followup_question":
                    await ask_followup_question(msg, response, tool_use_id)
                elif tool_name == "search_files":
                    await search_files(msg, response, tool_use_id)
                elif tool_name == "create_file":
                    await create_file(msg, response, tool_use_id)
                return await loop()
            elif response.stop_reason == 'max_tokens':
                messages.append({"role": "assistant", "content": response.content[0].text.strip()})
                tools.clear()  # should be last call and claude refuses to continue with tools enabled
                return await loop()
            else:
                return ApiResponse(message=response.content[0].text, error=None, costs=costs, files=files)

        async def create_file(msg, response, tool_use_id):
            filepath = msg.input['filepath']
            content = msg.input['content']
            try:
                # check if it is a patch
                patch = Patch.from_dirty_xml(content)
                if patch is not None:
                    return content
            except:
                pass
            result = await create_file_callback(filepath, content)
            await append_next_step(result, response, tool_use_id)

        async def search_files(msg, response, tool_use_id):
            q = msg.input['regex']
            files = await search_files_callback(q)
            content = []
            for f in files:
                content.append({"type": "text", "text": f})
            await append_next_step(content, response, tool_use_id)

        async def ask_followup_question(msg, response, tool_use_id):
            q = msg.input['question']
            a = await follow_up_question_callback(q)
            await append_next_step(a, response, tool_use_id)

        async def get_file_content_exec(msg, response, tool_use_id):
            files_requested = [msg.input['filepath']]
            file_content_result = await file_content_callback(files_requested)
            file_content = list()
            for file in file_content_result:
                file_content.append({"type": "text", "text": file + ":\n" + file_content_result[file]})
                files[file] = file_content_result[file]
            await append_next_step(file_content, response, tool_use_id)

        async def append_next_step(tool_result: Any, response, tool_use_id):
            messages.append({"role": "assistant", "content": response.content})
            messages.append(
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "tool_result",
                            "tool_use_id": tool_use_id,
                            "content": tool_result
                        }
                    ]
                })

        return await loop()

    def ask(self,
            prompt: str,
            model: str = _LATEST_HAIKU_MODEL,
            max_tokens: int = models[_LATEST_HAIKU_MODEL]["max_output_tokens"],
            temperature=0.0,
            assistant_msg=None
            ) -> ApiResponse:
        model = get_model(model)

        client = Anthropic()
        if temperature is None:
            temperature = 0.0
        try:
            if assistant_msg is None:
                message = client.messages.create(
                    temperature=temperature,
                    max_tokens=max_tokens,
                    messages=[
                        {
                            "role": "user",
                            "content": prompt,
                        }
                    ],
                    model=model,
                )
            else:
                message = client.messages.create(
                    temperature=temperature,
                    max_tokens=max_tokens,
                    messages=[
                        {
                            "role": "user",
                            "content": prompt,
                        },
                        {
                            "role": "assistant",
                            "content": assistant_msg
                        }
                    ],
                    model=model,
                )
            answer = message.content[0].text
            costs = self.get_api_costs(model, message.usage.input_tokens, message.usage.output_tokens)

            return ApiResponse(message=answer, error=None, costs=costs)

        except RateLimitError as e:
            headers = e.response.headers
            rate_limit_info = {
                'x-should-retry': headers.get('x-should-retry'),
                'anthropic-ratelimit-requests-limit': headers.get('anthropic-ratelimit-requests-limit'),
                'anthropic-ratelimit-requests-remaining': headers.get('anthropic-ratelimit-requests-remaining'),
                'anthropic-ratelimit-requests-reset': headers.get('anthropic-ratelimit-requests-reset'),
                'anthropic-ratelimit-tokens-limit': headers.get('anthropic-ratelimit-tokens-limit'),
                'anthropic-ratelimit-tokens-remaining': headers.get('anthropic-ratelimit-tokens-remaining'),
                'anthropic-ratelimit-tokens-reset': headers.get('anthropic-ratelimit-tokens-reset'),
                'retry-after': headers.get('retry-after'),
            }

            # Create a log message to show exceeded limits
            exceeded_limits = []

            # Check for exceeded limits
            if int(rate_limit_info['anthropic-ratelimit-tokens-remaining']) == 0:
                exceeded_limits.append('Tokens limit exceeded')

            if int(rate_limit_info['anthropic-ratelimit-requests-remaining']) == 0:
                exceeded_limits.append('Requests limit exceeded')

            # Prepare the log message
            if exceeded_limits:
                get_logger().error(f"Rate limit exceed: [{', '.join(exceeded_limits)}]")
                exceeded_info = {key: value for key, value in rate_limit_info.items() if value is not None}
                get_logger().debug(f"Rate limits exceeded: {exceeded_info}")
            else:
                get_logger().info("No rate limits exceeded.")
            raise e

    async def agent_loop(self,
                         uuid: str,
                         prompt: str,
                         agent_ids: list[str],
                         model: str = _LATEST_HAIKU_MODEL,
                         max_tokens: int = 4096,
                         temperature: float = 0.1,
                         max_nr_of_loops: int = 100
                         ) -> ApiResponse:

        model = get_model(model)
        get_logger().debug(f"Using model: {model}")
        agent_map = self.get_agent_map(agent_ids)
        tools = self.tools_from_agent_map(agent_map)
        messages = [
            {
                "role": "user",
                "content": prompt,
            }
        ]
        events.emit(f"/mm/agent/init/{uuid}", uuid, "claude",
                    symetric_dict(prompt, model, tools, messages, agent_ids, max_nr_of_loops, temperature))

        costs = self.get_api_costs(model, 0, 0)
        return await self.loop(uuid, model, agent_map, 0, max_nr_of_loops, messages, temperature, costs)

    def tools_from_agent_map(self, agent_map):
        tools = []
        for agent_name in agent_map:
            agent = agent_map[agent_name]
            properties, required_properties = self.properties_for_agent(agent)
            input_schema = self.input_schema_from_properties(properties, required_properties)
            tools.append(
                {
                    "name": agent.name,
                    "description": agent.description,
                    "input_schema": input_schema
                }
            )
        return tools

    async def loop(self,
                   uuid: str,
                   model: str,
                   agent_map: dict[str, Agent],
                   nr_of_loops: int,
                   max_nr_of_loops: int,
                   messages: list,
                   temperature: float,
                   costs: ApiCosts) -> ApiResponse:

        async def append_next_step(tool_result: Any, _response: Message, function_name: str, _tool_use_id: str):
            get_logger().debug(f"append_next_step: {tool_result}")
            messages.append({"role": "assistant", "content": _response.content})
            messages.append(
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "tool_result",
                            "tool_use_id": _tool_use_id,
                            "content": tool_result
                        }
                    ]
                })
            events.emit(f"/mm/agent/step/{uuid}", uuid, "claude", messages)

        nr_of_loops += 1
        get_logger().debug(f"loop: {nr_of_loops}")
        if nr_of_loops > max_nr_of_loops:
            get_logger().warning("Max number of loops reached")
            raise MaxNumberOfLoops()
        try:
            tools = self.tools_from_agent_map(agent_map)
            response = raw(messages=messages, tools=tools, model=model, temperature=temperature)
            get_logger().debug(f"response: {response} in loop: {nr_of_loops}")
            costs.add(self.get_api_costs(model, response.usage.input_tokens, response.usage.output_tokens))
            msg = response.content[len(response.content) - 1]
            if response.stop_reason == 'tool_use':
                tool_use_id = msg.id
                tool_name = msg.name
                get_logger().info(f"Tool requested: {tool_name}")
                get_logger().debug(f"Tool request messsage: {msg}")
                if tool_name not in agent_map:
                    raise ValueError(f"Unknown tool requested: {tool_name}")
                try:
                    await agent_map[tool_name].call(uuid, msg.input, response, tool_use_id, append_next_step)
                except Exception as e:
                    self.handle_tool_call_exception(messages, tool_name, e)
                return await self.loop(uuid,
                                       model,
                                       agent_map,
                                       nr_of_loops,
                                       max_nr_of_loops,
                                       messages,
                                       temperature,
                                       costs)
            elif response.stop_reason == 'max_tokens':
                messages.append({"role": "assistant", "content": response.content[0].text.strip()})
                return await self.loop(uuid,
                                       model,
                                       dict(),  # should be last call and claude refuses to continue with tools enabled
                                       nr_of_loops,
                                       max_nr_of_loops,
                                       messages,
                                       temperature,
                                       costs)
            elif response.stop_reason == 'end_turn':
                get_logger().info("Agent loop completed successfully")
                events.emit(f"/mm/agent/completed/{uuid}", uuid, "claude", symetric_dict(response, costs))
                return ApiResponse(message=msg.text, error=None, costs=costs)
            else:
                get_logger().warning(f"Unexpected stop reason: {response.stop_reason}")
                return ApiResponse(message=msg.text, error=None, costs=costs)
        except Exception as e:
            events.emit(f"/mm/agent/error/{uuid}", uuid, "claude", symetric_dict(e, costs))
            get_logger().error(f"Error in agent loop: {str(e)}")
            raise
