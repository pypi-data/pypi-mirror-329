from dataclasses import dataclass
from typing import Callable, Any

from menschmachine.llm.types import Agent, ToolProperty
from menschmachine.patch.xml_patch import XML_FORMAT


@dataclass
class FileContentAgent(Agent):
    def __init__(self, callback: Callable[[str, dict], Any]):
        super().__init__(
            name="get_file_content",
            description="Get the content of a file in the repository",
            properties=[
                ToolProperty(
                    name="filepath",
                    description="The complete path of the file as presented in the file_list array",
                    type="string",
                    required=True
                )
            ],
            callback=callback,
        )


# TODO make it a persistent shell during the agent loop
"""
import code

class InteractiveShell:
    def __init__(self):
        self.variables = {}
        self.interpreter = code.InteractiveInterpreter(self.variables)

    def execute(self, command):
        return self.interpreter.runcode(command)

    def get_variable(self, var_name):
        return self.variables.get(var_name)

# Example usage
shell = InteractiveShell()

# Execute commands
shell.execute("x = 5")
shell.execute("y = 10")
shell.execute("result = x + y")
shell.execute("print(f'The result is: {result}')")
"""


@dataclass
class RunShellCommandAgent(Agent):
    def __init__(self, callback: Callable[[str, dict], Any]):
        super().__init__(
            name="run_shell_command",
            description="Run a shell command on behalf of the user and receive the output. The command will be run like this: subprocess.run(command, shell=True, capture_output=True, text=True)",
            properties=[
                ToolProperty(
                    name="command",
                    description="The shell command to run",
                    type="string",
                    required=True
                )
            ],
            callback=callback
        )


@dataclass
class CreateFileAgent(Agent):
    def __init__(self, callback: Callable[[str, dict], Any]):
        super().__init__(
            name="create_file",
            description="Create a new file in the repository, use only for files which do not exist yet. If the file exists, create a patch in the xml format shown to you.",
            properties=[
                ToolProperty(
                    name="filepath",
                    description="The complete path of the file to create",
                ),
                ToolProperty(
                    name="content",
                    description="The content of the new file to create",
                )
            ],
            callback=callback
        )


@dataclass
class SearchFilesAgent(Agent):
    def __init__(self, callback: Callable[[str, dict], Any]):
        super().__init__(
            name="search_files",
            description="Perform a regex search inside the contents of all files in the repository, returning a list of all files which contents match the regex. "
                        "If you want to search for filenames, use the list_files tool.",
            properties=[
                ToolProperty(
                    name="regex",
                    description="The regular expression pattern to search for. Uses Rust regex syntax."
                )
            ],
            callback=callback
        )


@dataclass
class AskFollowUpQuestionAgent(Agent):
    def __init__(self, callback: Callable[[str, dict], Any]):
        super().__init__(
            name="ask_followup_question",
            description="""Ask the user a question to gather additional information needed to complete the task. 
                This tool should be used when you encounter ambiguities, need clarification, or require more details to proceed effectively. 
                It allows for interactive problem-solving by enabling direct communication with the user. 
                Use this tool judiciously to maintain a balance between gathering necessary information and avoiding excessive back-and-forth.",
                """,
            properties=[
                ToolProperty(
                    name="question",
                    description="The question to ask the user. This should be a clear, specific question that addresses the information you need."
                )
            ],
            callback=callback
        )


@dataclass
class PatchAgent(Agent):
    def __init__(self, callback: Callable[[str, dict], str]):
        super().__init__(
            name="patch_file",
            description="Change the contents of an existing file",
            properties=[
                ToolProperty(
                    name="xml_patch",
                    description=f"Provide the suggested changes strictly in the format `{XML_FORMAT}`, one by one. If you have multiple changes, call this tool multiple times. Always use get_file_content after a patch to receive the updated file contents.",
                    type="string",
                    required=True
                )
            ],
            callback=callback
        )


@dataclass
class FileListAgent(Agent):
    def __init__(self, callback: Callable[[str, dict], str]):
        super().__init__(
            name="list_files",
            description="List all files in the repository",
            properties=[],
            callback=callback
        )
