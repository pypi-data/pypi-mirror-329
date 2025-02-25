from openai import OpenAI

from menschmachine.llm.openrouter import OpenRouterApi
from menschmachine.llm.types import ModelRegistry

_MODEL_REGISTRY = ModelRegistry("o3-mini")

# Register models with their aliases
_MODEL_REGISTRY.register("gpt-4o-2024-11-20", ["gpt4o", "gpt4", "gpt-4o"], 2.5, 10)
_MODEL_REGISTRY.register("o1-mini", ["gpt4o-mini", "gpt4-mini"], 3, 12)
_MODEL_REGISTRY.register("o1", ["o1", "gpt-01"], 15, 60)
_MODEL_REGISTRY.register("o3-mini", ["o3-mini", "gpt-03-mini", "gpt-03mini"], 1.1, 4.4)
_MODEL_REGISTRY.register("o1-preview", ["o1", "gpt-o1", "o1-preview"], 15, 60)


class OAI(OpenRouterApi):
    def create_client(self):
        return OpenAI()

    def get_model_registry(self) -> ModelRegistry:
        return _MODEL_REGISTRY
