from typing import Any

from langchain_anthropic import ChatAnthropic
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from menschmachine.llm.types import ApiInterface, Agent, ApiCosts, ApiResponse, FileRequestCallbackType, \
    QuestionCallbackType, SearchFilesCallbackType, CreateFileCallbackType, ModelRegistry

MODEL_REGISTRY = ModelRegistry("haiku")
MODEL_REGISTRY.register("claude-3-haiku-20240307", ["haiku", "claude-haiku"], 0.25, 1.25)
MODEL_REGISTRY.register("claude-3-5-sonnet-20240620", ["sonnet", "claude-sonnet"], 3, 15)
MODEL_REGISTRY.register("gemini-1.5-flash", ["gemini-flash"], 0.075, 0.3)


def raw(messages: list[BaseMessage] | list[dict[str, str]],
        tools: list[dict] = None,
        tool_choice: dict = None,
        model: str = "haiku",
        temperature=0.0,
        ) -> Any:
    client = L4ngCh4in()
    chat = client.create_chat(MODEL_REGISTRY.get_model(model))
    if temperature is None:
        temperature = 0.0
    if tools is None or len(tools) == 0:
        return raw_without_tools(chat, messages, temperature)
    else:
        if tool_choice is None:
            return raw_with_tools(chat, messages, temperature, tools)
        else:
            return raw_with_tools_and_choices(chat, messages, temperature, tool_choice, tools)


def raw_with_tools_and_choices(chat, messages: list[BaseMessage], temperature, tool_choice, tools) -> BaseMessage:
    return chat.invoke(
        input=messages,
        tools=tools,
    )


def raw_with_tools(chat: BaseChatModel, messages: list[BaseMessage], temperature, tools) -> BaseMessage:
    return chat.invoke(
        input=messages,
        tools=tools,
    )


def raw_without_tools(chat: BaseChatModel, messages: list[BaseMessage], temperature: float) -> BaseMessage:
    return chat.invoke(input=messages)


class L4ngCh4in(ApiInterface):

    # noinspection PyMethodMayBeStatic
    def create_chat(self, model: str) -> BaseChatModel:
        if "claude" in model:
            return ChatAnthropic(model_name=model)
        elif "gemini" in model:
            return ChatGoogleGenerativeAI(model=model)
        else:
            raise ValueError(model)

    def ping(self) -> ApiResponse:
        return self.ask("Ping!")

    def _get_api_costs_from_response(self, model, response):
        in_tokens = response.usage_metadata["input_tokens"]
        out_tokens = response.usage_metadata["output_tokens"]
        costs = ApiCosts(tokens_in=in_tokens,
                         tokens_out=out_tokens,
                         model=model,
                         estimated_cost_in_us_cent=self.estimate_costs(model,
                                                                       in_tokens,
                                                                       out_tokens))
        return costs

    def is_model_supported(self, model: str) -> bool:
        raise NotImplementedError()

    def ask(self, prompt: str, model: str = None, max_tokens: int = 4096, temperature=0.0,
            assistant_msg=None) -> ApiResponse:
        model = MODEL_REGISTRY.get_official_name(model)
        chat = self.create_chat(model)
        response = chat.invoke(prompt)
        costs = self._get_api_costs_from_response(model, response)
        return ApiResponse(message=response.content, error=None, costs=costs, files=None)

    async def with_tools_loop(self, prompt: str, file_content_callback: FileRequestCallbackType,
                              follow_up_question_callback: QuestionCallbackType,
                              search_files_callback: SearchFilesCallbackType,
                              create_file_callback: CreateFileCallbackType, model: str, max_tokens: int = 4096,
                              temperature: float = 0.1) -> ApiResponse:
        raise NotImplementedError("deprecated")

    async def agent_loop(self, uuid: str, prompt: str, agent_ids: list[str], model: str, max_tokens: int = 4096,
                         temperature: float = 0.1, max_nr_of_loops: int = 10) -> ApiResponse:
        raise NotImplementedError()

    def estimate_costs(self, model: str, prompt_tokens: int, completion_tokens: int) -> float:
        def costs(nr_tokens, price_per_million: float):
            return (nr_tokens * (price_per_million / (1000. * 1000.))) / 100.  # in cent

        in_price, out_price = MODEL_REGISTRY.get_prices(model)
        return costs(prompt_tokens, in_price) + costs(completion_tokens, out_price)

    async def loop(self, uuid: str, model: str, agent_map: dict[str, Agent], nr_of_loops: int, max_nr_of_loops: int,
                   messages: list, temperature: float, costs: ApiCosts) -> Any:
        raise NotImplementedError()
