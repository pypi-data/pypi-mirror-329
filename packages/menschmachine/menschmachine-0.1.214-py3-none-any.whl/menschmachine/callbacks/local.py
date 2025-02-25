import logging
import os
from typing import Callable, Awaitable, Union

from menschmachine.callbacks import Callbacks
from menschmachine.patch import Patch
from menschmachine.platform_adapter import PlatformAdapter


class LocalCallbacks(Callbacks):

    def __init__(self, logger: logging.Logger, fs: PlatformAdapter):
        super().__init__()
        self.fs = fs
        self.logger = logger

    def get_question_callback(self) -> Callable[[str, dict], Union[str, Awaitable[str]]]:

        def question_callback(uuid: str, q: dict) -> str:
            question = q['question']
            return self.fs.ask_user(question)

        return question_callback

    def get_file_list_callback(self) -> Callable[[str, dict], Union[str, Awaitable[str]]]:

        def filelist_callback(uuid: str, ignore) -> str:
            return str(self.fs.get_file_list())

        return filelist_callback

    def get_run_shell_command_callback(self) -> Callable[[str, dict], Union[str, Awaitable[str]]]:

        def run_shell_command_callback(uuid: str, q: dict) -> str:
            cmd = q["command"]
            (stdout, stderr, exit_code) = self.fs.execute(cmd)
            return f"Result of the command is STDOUT: {stdout}\nSTDERR: {stderr}\nEXIT_CODE: {exit_code}"

        return run_shell_command_callback

    def get_search_files_callback(self) -> Callable[[str, dict], Union[str, Awaitable[str]]]:

        def search_callback(uuid: str, q: dict) -> str:
            regex = q['regex']
            return str(self.fs.search_files(regex))

        return search_callback

    def get_file_content_callback(self) -> Callable[[str, dict], Union[str, Awaitable[str]]]:

        def file_content_callback(uuid: str, q: dict) -> str:
            filepath = q['filepath']
            if os.path.exists(filepath):
                return self.fs.read_file(filepath)
            else:
                return f"FAILED: File {filepath} not found"

        return file_content_callback

    def get_patch_callback(self) -> Callable[[str, dict], Union[str, Awaitable[str]]]:

        def patch_callback(uuid: str, q: dict) -> str:
            patch = Patch.from_dirty_xml(q["xml_patch"])
            try:
                for applied in patch.apply_merged(lambda path: self.fs.read_file(path)):
                    self.logger.info(f"Patching {applied.filename}")
                    self.fs.write_file(applied.filename, applied.source)
                return "OK"
            except Exception as e:
                self.logger.error(f"Error applying patch", exc_info=True)
                return f"Patch could not be applied: {e}"

        return patch_callback

    def get_create_file_callback(self) -> Callable[[str, dict], Union[str, Awaitable[str]]]:

        def create_file_callback(uuid: str, q: dict) -> str:
            filename_ = q["filepath"]
            if os.path.exists(filename_):
                return f"FAILED: the file {filename_} already exists, you have to use the patch_file tool in this case"
            else:
                self.fs.write_file(filename_, q["content"])
                return "SUCCESS"

        return create_file_callback

    def get_delete_file_callback(self) -> Callable[[str, dict], Union[str, Awaitable[str]]]:
        raise NotImplementedError

    def get_create_directory_callback(self) -> Callable[[str, dict], Union[str, Awaitable[str]]]:
        raise NotImplementedError

    def get_delete_directory_callback(self) -> Callable[[str, dict], Union[str, Awaitable[str]]]:
        raise NotImplementedError
