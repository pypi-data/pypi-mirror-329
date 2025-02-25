import json
import os
import uuid as uuidgen
from typing import Any

import google.generativeai as genai
from google.api_core import exceptions
from google.generativeai.types import GenerateContentResponse

from menschmachine.event import events
from menschmachine.llm.types import FileRequestCallbackType, QuestionCallbackType, CreateFileCallbackType, \
    SearchFilesCallbackType, \
    ApiInterface, ApiResponse, MaxNumberOfLoops, ApiCosts, Agent, ModelRegistry
from menschmachine.log import get_logger
from menschmachine.patch import Patch
from menschmachine.util import symetric_dict

MODEL_REGISTRY = ModelRegistry("gemini-pro")

# Register models with their aliases
MODEL_REGISTRY.register("gemini-pro", ["gemini-pro"], 0.25, 0.5, "gemini-pro")
MODEL_REGISTRY.register("gemini-pro-vision", ["gemini-pro-vision"], 0.25, 0.5, "gemini-pro-vision")
MODEL_REGISTRY.register("gemini-ultra", ["gemini-ultra"], 1.25, 2.5, "gemini-ultra")
MODEL_REGISTRY.register("gemini-flash", ["gemini-flash"], 0.075, 0.3, "gemini-1.5-flash-latest")


def raw(messages: list[dict],
        tools: list[dict] = None,
        tool_choice: dict | str | None = None,
        model: str = None,
        max_tokens: int = 4000,
        temperature=0.0,
        ) -> GenerateContentResponse:
    client = create_client()
    model = MODEL_REGISTRY.get_model(model)
    official_name = MODEL_REGISTRY.get_official_name(model)

    if temperature is None:
        temperature = 0.0
    try:
        chat = client.GenerativeModel(official_name).start_chat()
        if tools is None or len(tools) == 0:
            result = chat.send_message(
                content=messages[-1]['content'],
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=max_tokens,
                    temperature=temperature,
                )
            )
        else:
            result = chat.send_message(
                content=messages[-1]['content'],
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=max_tokens,
                    temperature=temperature,
                ),
                tools=tools
            )
        return result

    except exceptions.GoogleAPICallError as e:
        get_logger().error(f"Google API Call Error: {str(e)}")
        raise e


def create_client():
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    return genai


class GeminiApi(ApiInterface):

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
        events.emit(f"/mm/agent/init/{uuid}", uuid, "google_ai", symetric_dict(prompt, model, tools, messages))
        return await self.loop(uuid, model, agent_map, 0, max_nr_of_loops, messages, temperature, costs)

    def tools_from_agent_map(self, agent_map):
        tools = []
        for agent_id in agent_map:
            agent = agent_map[agent_id]
            properties, required_properties = self.properties_for_agent(agent)
            input_schema = self.input_schema_from_properties(properties, required_properties)
            tools.append(
                {
                    "name": agent.name,
                    "description": agent.description,
                    "parameters": input_schema
                },
            )
        return tools

    def ping(self) -> ApiResponse:
        return self.ask("ping", MODEL_REGISTRY.get_long_name("gemini-pro"))

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
        costs = self.get_api_costs(model, response.usage_metadata.prompt_token_count,
                                   response.usage_metadata.candidates_token_count)
        answer = response.text
        return ApiResponse(message=answer, error=None, costs=costs)

    async def with_tools_loop(self,
                              prompt: str,
                              file_content_callback: FileRequestCallbackType,
                              follow_up_question_callback: QuestionCallbackType,
                              search_files_callback: SearchFilesCallbackType,
                              create_file_callback: CreateFileCallbackType,
                              model: str,
                              max_tokens: int = 4000,
                              temperature: float = 0.1,
                              ) -> ApiResponse:
        tools = [
            {
                "function_declarations": [
                    {
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
                    },
                    {
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
                    },
                    {
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
                    },
                    {
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
                ]
            }
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
            costs.add(self.get_api_costs(model, response.usage_metadata.prompt_token_count,
                                         response.usage_metadata.candidates_token_count))

            if response.candidates[0].content.parts[-1].function_call:
                function_call = response.candidates[0].content.parts[-1].function_call
                tool_name = function_call.name
                get_logger().info(f"Tool requested: {tool_name}")
                if tool_name == "get_file_content":
                    await get_file_content_exec(function_call)
                elif tool_name == "ask_followup_question":
                    await ask_followup_question(function_call)
                elif tool_name == "search_files":
                    await search_files(function_call)
                elif tool_name == "create_file":
                    await create_file(function_call)
                return await loop()
            else:
                return ApiResponse(message=response.text, error=None, costs=costs, files=files)

        async def create_file(function_call):
            args = json.loads(function_call.args)
            filepath = args['filepath']
            content = args['content']
            try:
                patch = Patch.from_dirty_xml(content)
                if patch is not None:
                    return content
            except:
                pass
            result = await create_file_callback(filepath, content)
            await append_next_step(result, function_call)

        async def search_files(function_call):
            args = json.loads(function_call.args)
            q = args['regex']
            files = await search_files_callback(q)
            await append_next_step(files, function_call)

        async def ask_followup_question(function_call):
            args = json.loads(function_call.args)
            q = args['question']
            a = await follow_up_question_callback(q)
            await append_next_step(a, function_call)

        async def get_file_content_exec(function_call):
            args = json.loads(function_call.args)
            files_requested = [args['filepath']]
            file_content_result = await file_content_callback(files_requested)
            for file in file_content_result:
                files[file] = file_content_result[file]
            await append_next_step(file_content_result, function_call)

        async def append_next_step(tool_result: Any, function_call):
            messages.append({"role": "model", "content": json.dumps(function_call.dict())})
            messages.append(
                {
                    "role": "function",
                    "name": function_call.name,
                    "content": json.dumps(tool_result)
                })

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

        async def append_next_step(tool_result: Any, _response: str, function_name: str, tool_call_id: str):
            messages.append({"role": "assistant", "content": _response})
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call_id,
                    "name": function_name,
                    "content": json.dumps(tool_result),
                })
            events.emit(f"/mm/agent/step/{uuid}", uuid, "google_ai", messages)

        nr_of_loops += 1
        get_logger().debug(f"Loop number: {nr_of_loops}")
        if nr_of_loops > max_nr_of_loops:
            get_logger().warning("Max number of loops reached")
            raise MaxNumberOfLoops()
        tools = [
            {
                "function_declarations": self.tools_from_agent_map(agent_map)
            }
        ]
        try:
            response = raw(
                model=model,
                messages=messages,
                tools=tools,
                temperature=temperature,
                max_tokens=4096
            )
            costs.add(self.get_api_costs(model, response.usage_metadata.prompt_token_count,
                                         response.usage_metadata.candidates_token_count))
            message = response.text
            get_logger().debug(f"Response: {message}")

            # Google AI doesn't have a direct equivalent to OpenAI's tool_calls
            # We need to parse the response to determine if a tool was called
            tool_call_results = []
            for tool in tools:
                tool_name = tool['function']['name']
                if tool_name in message:
                    # Extract arguments from the message (this is a simplification)
                    function_args = json.dumps({})  # You'll need to implement proper argument extraction
                    tool_use_id = str(uuidgen.uuid4())  # Generate a unique ID for the tool call
                    get_logger().info(f"Tool requested: {tool_name}")
                    get_logger().debug(f"Tool request message: {message}")
                    if tool_name not in agent_map:
                        raise ValueError(f"Unknown tool requested: {tool_name}")
                    try:
                        await agent_map[tool_name].call(uuid,
                                                        json.loads(function_args),
                                                        response,
                                                        tool_use_id,
                                                        append_next_step)
                    except Exception as e:
                        self.handle_tool_call_exception(message, tool_name, e)
                    tool_call_results.append({
                        "role": "tool",
                        "tool_call_id": tool_use_id,
                        "name": tool_name,
                        "content": json.dumps(function_args),
                    })

            if tool_call_results:
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
            else:
                get_logger().info("Agent loop completed successfully")
                events.emit(f"/mm/agent/completed/{uuid}", uuid, "google_ai", symetric_dict(response, costs))
                return ApiResponse(message=message, error=None, costs=costs)
        except Exception as e:
            events.emit(f"/mm/agent/error/{uuid}", uuid, "google_ai", symetric_dict(e, costs))
            get_logger().error(f"Error in agent loop: {str(e)}")
            raise

    def estimate_costs(self, model: str, prompt_tokens: int, completion_tokens: int) -> float:
        def costs(nr_tokens, price_per_million: float):
            return (nr_tokens * (price_per_million / (1000. * 1000.))) / 100.  # in cent

        in_price, out_price = MODEL_REGISTRY.get_prices(model)
        return costs(prompt_tokens, in_price) + costs(completion_tokens, out_price)
