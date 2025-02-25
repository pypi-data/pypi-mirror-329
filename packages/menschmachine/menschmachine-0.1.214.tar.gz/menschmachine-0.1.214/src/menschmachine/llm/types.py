import json
import os
import tempfile
from abc import ABC, abstractmethod, ABCMeta
from dataclasses import dataclass, field
from inspect import isawaitable
from typing import Callable, Awaitable, Optional, Any, Coroutine, List, Dict, Set, Tuple

from dataclasses_json import dataclass_json
from fastapi.encoders import jsonable_encoder

from menschmachine.event import events
from menschmachine.log import get_logger
from menschmachine.util import symetric_dict

FileRequestCallbackType = Callable[[list[str]], Awaitable[dict[str, str]]]
QuestionCallbackType = Callable[[str], Awaitable[str]]
CreateFileCallbackType = Callable[[str, str], Awaitable[str]]
SearchFilesCallbackType = Callable[[str], Awaitable[list[str]]]


@dataclass
class FileQueryResponse:
    answer: str
    files: dict[str, str] = field(default_factory=dict)


@dataclass
class ApiError:
    message: str


@dataclass
class RateLimitError(ApiError):
    pass


@dataclass
class ApiCosts:
    tokens_in: int
    tokens_out: int
    model: str
    estimated_cost_in_us_cent: float = field(repr=False)
    price: Optional[float] = 0.

    def add(self, costs):
        self.tokens_in += costs.tokens_in
        self.tokens_out += costs.tokens_out
        self.estimated_cost_in_us_cent += costs.estimated_cost_in_us_cent
        self.price = round(self.estimated_cost_in_us_cent, 4)

    @classmethod
    def from_json(cls, api_costs_json: dict) -> 'ApiCosts':
        """

        Args:
            api_costs_json:

        {'estimated_cost_in_us_cent': 5.8822499999999995e-05, 'model': 'claude-3-haiku-20240307', 'price': 0.0001,
         'tokens_in': 15469, 'tokens_out': 1612}
        Returns:

        """

        return ApiCosts(estimated_cost_in_us_cent=api_costs_json['estimated_cost_in_us_cent'],
                        model=api_costs_json['model'],
                        tokens_out=api_costs_json['tokens_out'],
                        tokens_in=api_costs_json['tokens_in'],
                        price=api_costs_json['price'])


@dataclass_json
@dataclass
class ApiResponse:
    message: str
    error: ApiError | None
    costs: ApiCosts
    files: Optional[dict[str, str]] = None


@dataclass
class ToolProperty:
    name: str
    description: str
    required: bool = True
    type: str = "string"


CollectResultCallable = Callable[[Any, Any, str, str], Coroutine[Any, Any, None]]


class Agent:

    def __init__(self,
                 name: str,
                 description: str,
                 properties: list[ToolProperty],
                 callback: Callable[[str, dict], Any] = None):
        super().__init__()
        self.name = name
        self.description = description
        self.properties = properties
        self.callback = callback

    async def call(self,
                   uuid: str,
                   msg: dict,
                   response: Any,
                   tool_use_id: str | None,
                   collect_result: CollectResultCallable | None = None) -> Any:
        get_logger().debug(f"Agent {self.name} called with {msg}")
        result = self.callback(uuid, msg)
        if isawaitable(result):
            result = await result
        events.emit(f"/mm/agent/call/result/{uuid}", uuid, None,
                    symetric_dict(result, self.name, msg, response, tool_use_id))
        get_logger().debug(f"Agent {self.name} result: {result}")
        if collect_result is not None:
            return await collect_result(result, response, self.name, tool_use_id)
        else:
            return result


class AgentRepository:
    _instance = None

    def __init__(self):
        super().__init__()
        self.agents: dict[str, Agent] = {}

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(AgentRepository, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def register(self, agent_id: str, agent: Agent):
        self.agents[agent_id] = agent

    def get(self, agent_id: str) -> Agent:
        return self.agents[agent_id]


agent_repository: AgentRepository = AgentRepository()


class MaxNumberOfLoops(Exception):
    pass


class ApiInterface(ABC, metaclass=ABCMeta):

    def __init__(self):
        self.failed_at = -1
        self.success_at = -1
        self.failed_reason: Exception | None = None

    @abstractmethod
    def ping(self) -> ApiResponse:
        raise NotImplementedError()

    @abstractmethod
    def is_model_supported(self, model: str) -> bool:
        return False

    @abstractmethod
    def ask(self,
            prompt: str,
            model: str = None,
            max_tokens: int = 4096,
            temperature=0.0,
            assistant_msg=None
            ) -> ApiResponse:
        raise NotImplementedError()

    @abstractmethod
    async def with_tools_loop(
            self,
            prompt: str,
            file_content_callback: FileRequestCallbackType,
            follow_up_question_callback: QuestionCallbackType,
            search_files_callback: SearchFilesCallbackType,
            create_file_callback: CreateFileCallbackType,
            model: str,
            max_tokens: int = 4096,
            temperature: float = 0.1,
    ) -> ApiResponse:
        raise NotImplementedError()

    @abstractmethod
    async def agent_loop(self,
                         uuid: str,
                         prompt: str,
                         agent_ids: list[str],
                         model: str,
                         max_tokens: int = 4096,
                         temperature: float = 0.1,
                         max_nr_of_loops: int = 10
                         ) -> ApiResponse:
        raise NotImplementedError()

    def get_api_costs(self, model, tokens_in, tokens_out) -> ApiCosts:
        return ApiCosts(tokens_in=tokens_in,
                        tokens_out=tokens_out,
                        model=model,
                        estimated_cost_in_us_cent=self.estimate_costs(model,
                                                                      tokens_in,
                                                                      tokens_out))

    @abstractmethod
    def estimate_costs(self, model: str, prompt_tokens: int, completion_tokens: int) -> float:
        raise NotImplementedError()

    # noinspection PyMethodMayBeStatic
    def input_schema_from_properties(self, properties, required_properties):
        input_schema = {
            "type": "object",
            "properties": properties,
            "required": required_properties
        }
        return input_schema

    # noinspection PyMethodMayBeStatic
    def properties_for_agent(self, agent):
        required_properties = []
        properties = {}
        for prop in agent.properties:
            properties[prop.name] = {
                "type": prop.type,
                "description": prop.description
            }
            if prop.required:
                required_properties.append(prop.name)
        return properties, required_properties

    # noinspection PyMethodMayBeStatic
    def get_agent_map(self, agent_ids: list[str]) -> dict[str, Agent]:
        return {agent_repository.get(agent_id).name: agent_repository.get(agent_id) for agent_id in agent_ids}

    # noinspection PyMethodMayBeStatic
    def handle_tool_call_exception(self, message, tool_name, e: Exception):
        get_logger().error(f"Error calling agent {tool_name}", exc_info=True)
        dirpath = tempfile.mkdtemp()
        get_logger().info(f"Saving debug info to {dirpath}")
        with open(os.path.join(dirpath, f"{tool_name}-msg-debug.json"), "w") as f:
            try:
                f.write(message.to_json())
            except:
                f.write(json.dumps(jsonable_encoder(message)))
            f.flush()
        raise e

    @abstractmethod
    async def loop(self,
                   uuid: str,
                   model: str,
                   agent_map: dict[str, Agent],
                   nr_of_loops: int,
                   max_nr_of_loops: int,
                   messages: list,
                   temperature: float,
                   costs: ApiCosts) -> Any:
        raise NotImplementedError()


class ModelInfo:
    def __init__(self, long_name: str, short_names: List[str], input_price: float, output_price: float,
                 official_name: str):
        self.long_name = long_name
        self.short_names = short_names
        self.input_price = input_price
        self.output_price = output_price
        self.official_name = official_name


class ModelRegistry:
    def __init__(self, default_model: str):
        self.models: Dict[str, ModelInfo] = {}
        self.short_to_long: Dict[str, str] = {}
        self.default_model = default_model

    def register(self, long_name: str, short_names: List[str], input_price: float, output_price: float,
                 official_name: str = None):
        model_info = ModelInfo(long_name, short_names, input_price, output_price, official_name)
        self.models[long_name] = model_info
        for short_name in short_names:
            self.short_to_long[short_name.lower()] = long_name

    def get_long_name(self, name: str) -> str:
        return self.short_to_long.get(name.lower(), name)

    def is_supported(self, name: str) -> bool:
        long_name = self.get_long_name(name)
        return long_name in self.models

    def get_all_names(self) -> Set[str]:
        return set(self.models.keys()) | set(self.short_to_long.keys())

    def get_prices(self, name: str) -> Tuple[float, float]:
        long_name = self.get_long_name(name)
        if long_name in self.models:
            model_info = self.models[long_name]
            return model_info.input_price, model_info.output_price
        return -1.0, -1.0  # unknown, not found

    def get_model(self, model: str) -> str:
        if "UNIVERSAL_MODEL" in os.environ:
            model = os.environ["UNIVERSAL_MODEL"]
        if model is None:
            model = self.get_long_name(self.default_model)
        return self.get_long_name(model)

    def get_supported_models(self) -> Set[str]:
        return self.get_all_names()

    def get_official_name(self, model):
        model = self.get_model(model)
        for m in self.models:
            if m == model and self.models[m].official_name is not None:
                return self.models[m].official_name
        return model
