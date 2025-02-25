import os
import time
from typing import Any, List

from menschmachine.llm.claude import ClaudeApi
from menschmachine.llm.lite import LiteLlmApi
from menschmachine.llm.oai import OAI
from menschmachine.llm.openrouter import OpenRouterApi
from menschmachine.llm.types import ApiInterface, FileRequestCallbackType, QuestionCallbackType, \
    SearchFilesCallbackType, \
    CreateFileCallbackType, ApiResponse, Agent, ApiCosts
from menschmachine.log import get_logger


class ApiProxy(ApiInterface):
    _instances = {}

    def __new__(cls):
        if cls not in cls._instances:
            cls._instances[cls] = super(ApiProxy, cls).__new__(cls)
            # noinspection PyProtectedMember
            cls._instances[cls]._initialize()
        return cls._instances[cls]

    def _initialize(self, wait_for_retry_secs=600):
        api_order = os.environ.get('MENSCHMACHINE_APIS', 'OpenRouterApi,ClaudeApi,OpenAI').split(',')
        api_mapping = {
            'OpenRouterApi': OpenRouterApi,
            'ClaudeApi': ClaudeApi,
            'LiteLlmApi': LiteLlmApi,
            'OpenAI': OAI,
        }

        self.apis: List = []
        for api_name in api_order:
            api_class = api_mapping.get(api_name.strip())
            if api_class:
                self.apis.append(api_class())
            else:
                raise ValueError(f"Warning: Unknown API '{api_name}' specified in MENSCHMACHINE_APIS")

        self.wait_for_retry_secs = wait_for_retry_secs

    def estimate_costs(self, model: str, prompt_tokens: int, completion_tokens: int) -> float:
        return self._get_api(model).estimate_costs(model, prompt_tokens, completion_tokens)

    def is_model_supported(self, model: str) -> bool:
        for api in self.apis:
            if api.is_model_supported(model):
                return True
        return False

    async def agent_loop(self,
                         uuid: str,
                         prompt: str,
                         agent_ids: list[str],
                         model: str,
                         max_tokens: int = 4096,
                         temperature: float = 0.1,
                         max_nr_of_loops: int = 10) -> ApiResponse:
        return await self._get_api(model).agent_loop(uuid, prompt, agent_ids, model, max_tokens, temperature,
                                                     max_nr_of_loops)

    def ping(self) -> ApiResponse:
        return self._get_api().ping()

    def _get_supported_apis(self, model: str) -> list[ApiInterface]:
        apis = list()
        for api in self.apis:
            if model is None or api.is_model_supported(model):
                apis.append(api)
        return apis

    def _get_api(self, model: str = None) -> ApiInterface:
        if "UNIVERSAL_MODEL" in os.environ:
            model = os.environ["UNIVERSAL_MODEL"]
        if model is None:
            if "DEFAULT_MODEL" in os.environ:
                model = os.environ["UNIVERSAL_MODEL"]
            else:
                model = "haiku"
        apis = self._get_supported_apis(model)
        for api in apis:
            if self.wait_for_retry_secs + api.failed_at > time.time():
                continue  # means api is marked as 'failing'
            elif self.wait_for_retry_secs + api.success_at > time.time():
                # recently pinged successfully, no ping() needded
                return api
            else:
                try:
                    api.ping()
                    api.success_at = time.time()
                    api.failed_at = -1
                    api.failed_reason = None
                    return api
                except Exception as e:
                    get_logger().info(f"Api {api.__class__.__name__} is failing. Reason: {e}")
                    get_logger().debug(f"Api {api.__class__.__name__} is failing", exc_info=True)
                    api.failed_at = time.time()
                    api.failed_reason = e
                    api.success_at = -1
        raise ValueError(f"No api found supporting {model} which is not marked as failing")

    def ask(self,
            prompt: str,
            model: str = None,
            max_tokens: int = 4096,
            temperature=0.0,
            assistant_msg=None) -> ApiResponse:
        response = self._get_api(model).ask(prompt, model, max_tokens, temperature, assistant_msg)
        get_logger().info(f"{response.costs}")
        return response

    async def with_tools_loop(self,
                              prompt: str,
                              file_content_callback: FileRequestCallbackType,
                              follow_up_question_callback: QuestionCallbackType,
                              search_files_callback: SearchFilesCallbackType,
                              create_file_callback: CreateFileCallbackType,
                              model: str,
                              max_tokens: int = 4096,
                              temperature: float = 0.1) -> ApiResponse:
        response = await self._get_api(model).with_tools_loop(prompt, file_content_callback,
                                                              follow_up_question_callback,
                                                              search_files_callback, create_file_callback, model,
                                                              max_tokens, temperature)
        get_logger().info(f"{response.costs}")
        return response

    async def loop(self, uuid: str, model: str, agent_map: dict[str, Agent], nr_of_loops: int, max_nr_of_loops: int,
                   messages: list, temperature: float, costs: ApiCosts) -> Any:
        return await self._get_api(model).loop(uuid, model, agent_map,
                                               nr_of_loops, max_nr_of_loops,
                                               messages, temperature, costs)


# Create a single instance of ApiProxy
api_proxy = ApiProxy()
