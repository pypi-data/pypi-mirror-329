import logging
import os
import subprocess
from abc import ABC, abstractmethod
from contextlib import contextmanager
from pathlib import Path
from typing import Optional, Tuple, Callable

from rich.console import Console
from rich.progress import Progress
from ripgrepy import Ripgrepy


class PlatformAdapter(ABC):
    @abstractmethod
    def get_file_list(self, file_filter: Callable[[str], bool] = None) -> list[str]:
        pass

    @abstractmethod
    def read_file(self, file: str) -> str:
        pass

    @abstractmethod
    def write_file(self, file_, content):
        pass

    @abstractmethod
    def ask_user(self, question: str) -> str:
        pass

    @abstractmethod
    def show_progress(self, description: str):
        pass

    @abstractmethod
    def search_files(self, regex: str) -> list[str]:
        pass

    @abstractmethod
    def get_root_dir(self) -> str:
        pass

    @abstractmethod
    def execute(self, cmd: str, user_confirmation: bool = True) -> Tuple[str, str, int]:
        pass


class LocalFilesystemAdapter(PlatformAdapter):

    def get_file_list(self, file_filter: Callable[[str], bool] = None) -> list[str]:
        files = []
        for root, _, filenames in os.walk('.'):
            if '.git' in root.split(os.sep):
                continue
            for filename in filenames:
                f = os.path.join(root, filename)
                if file_filter is None or file_filter(f):
                    files.append(f)
        return files

    def __init__(self, logger: logging.Logger, batch_mode: bool = False):
        self.logger = logger
        self.current_progress_description = None
        self.current_task = None
        self.current_progress = None
        self.batch_mode = batch_mode
        self.console = Console()

    @contextmanager
    def show_progress(self, description: str):
        self.current_progress_description = description
        if self.batch_mode:
            yield
        else:
            with Progress(refresh_per_second=10) as progress:
                self.current_progress = progress
                self.current_task = progress.add_task(description, total=None, transient=True)
                yield self.current_progress
                self.current_progress.update(self.current_task, completed=True)

    def cancel_progress(self):
        if self.current_progress:
            self.current_progress.stop()

    def ask_user(self, question: str) -> str:
        self.cancel_progress()
        a = self.console.input(f"{question}\n> ")
        if self.current_progress_description is not None:
            with self.show_progress(self.current_progress_description):
                return a
        else:
            return a

    def read_file(self, file: str) -> Optional[str]:
        if self.is_readable(file):
            return Path(file).read_text()
        return None

    def write_file(self, file_, content):
        directory = os.path.dirname(file_)
        self.logger.debug(f"Write file {file_}")
        if directory:
            os.makedirs(directory, exist_ok=True)
        with open(file_, 'w') as f:
            f.write(content)

    def execute(self, cmd: str, user_confirmation: bool = True) -> Tuple[str, str, int]:
        self.logger.info(f"Executing cmd {cmd}")
        if not user_confirmation:
            return self.do_execute(cmd)
        while True:
            self.console.print("[bold yellow]Are you sure you want to execute the following command?[/bold yellow]")
            self.console.print(f"[bold cyan]{cmd}[/bold cyan]")
            confirmation = self.ask_user("[bold green]Type 'yes' to confirm or 'no' to cancel:[/bold green]")
            if confirmation.lower() == 'yes':
                return self.do_execute(cmd)
            elif confirmation.lower() == 'no':
                self.logger.info("Command execution cancelled by user.")
                self.console.print("[bold red]Command execution cancelled by user.[/bold red]")
                return "", "Command execution cancelled by user.", 1
            else:
                self.console.print("[bold red]Invalid response. Please answer 'yes' or 'no'.[/bold red]")

    # noinspection PyMethodMayBeStatic
    def do_execute(self, cmd):
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout, result.stderr, result.returncode

    def search_files(self, regex: str) -> list[str]:
        self.logger.info(f"Searching files for {regex}")
        rg = Ripgrepy(regex, self.get_root_dir())
        as_dict = rg.files_with_matches().json().run().as_dict
        matches = list()
        for match in as_dict:
            if match["type"] == "match":
                matches.append(match["data"]["path"]["text"])
        return list(set(matches))

    def get_root_dir(self):
        return os.getcwd()

    @staticmethod
    def is_readable(file: str) -> bool:
        return os.path.isfile(file) and os.access(file, os.R_OK)
