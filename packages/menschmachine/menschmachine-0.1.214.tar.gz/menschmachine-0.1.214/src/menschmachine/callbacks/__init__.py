from abc import ABC, abstractmethod
from typing import Callable, Any, Union, Awaitable


class Callbacks(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_file_list_callback(self) -> Callable[[Any], Union[str, Awaitable[str]]]:
        pass

    @abstractmethod
    def get_question_callback(self) -> Callable[[Any], Union[str, Awaitable[str]]]:
        pass

    @abstractmethod
    def get_run_shell_command_callback(self) -> Callable[[Any], Union[str, Awaitable[str]]]:
        pass

    @abstractmethod
    def get_search_files_callback(self) -> Callable[[Any], Union[str, Awaitable[str]]]:
        pass

    @abstractmethod
    def get_file_content_callback(self) -> Callable[[Any], Union[str, Awaitable[str]]]:
        pass

    @abstractmethod
    def get_patch_callback(self) -> Callable[[Any], Union[str, Awaitable[str]]]:
        pass

    @abstractmethod
    def get_create_file_callback(self) -> Callable[[Any], Union[str, Awaitable[str]]]:
        pass

    @abstractmethod
    def get_delete_file_callback(self) -> Callable[[Any], Union[str, Awaitable[str]]]:
        pass

    @abstractmethod
    def get_create_directory_callback(self) -> Callable[[Any], Union[str, Awaitable[str]]]:
        pass

    @abstractmethod
    def get_delete_directory_callback(self) -> Callable[[Any], Union[str, Awaitable[str]]]:
        pass
