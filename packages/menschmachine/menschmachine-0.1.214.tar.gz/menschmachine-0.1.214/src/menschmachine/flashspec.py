import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Tuple, Generator, Awaitable

import yaml

from menschmachine.llm.types import ApiResponse
from menschmachine.log import get_logger
from menschmachine.platform_adapter import PlatformAdapter
from menschmachine.project import StepCallback, Step, Task


@dataclass
class CodeGenerationStep:
    coroutine: Awaitable[ApiResponse]
    step: Step
    task: Task
    task_number: int
    total_number_of_tasks: int


class AbortGeneration(Exception):
    pass


class FlashSpec(ABC):

    @abstractmethod
    def create_spec(self,
                    uuid: str,
                    model: str,
                    extend: bool = False) -> str:
        pass

    @abstractmethod
    def create_breakdown(self,
                         uuid: str,
                         spec: str,
                         model: str,
                         extend: bool = False) -> str:
        pass

    @abstractmethod
    def create_code(self,
                    uuid: str,
                    spec: str,
                    breakdown: str,
                    model: str,
                    resume_at: int = 0,
                    extend: bool = False,
                    step_completed_callback: StepCallback = StepCallback()) \
            -> Generator[CodeGenerationStep, None, None]:
        pass


def run_check_command(fs: PlatformAdapter) -> Tuple[str, str, int]:
    if os.path.exists(".flashspec.yaml"):
        with open(".flashspec.yaml") as stream:
            try:
                config = yaml.safe_load(stream)
                if "check_command" in config:
                    check_command = config["check_command"]
                    return fs.execute(check_command, user_confirmation=False)
            except yaml.YAMLError as e:
                get_logger().warning("Cannot parse config file", e)
    return "", "", 0
