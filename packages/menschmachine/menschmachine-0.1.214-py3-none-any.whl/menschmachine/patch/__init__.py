import re
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Iterator, Optional, Callable

from bs4 import BeautifulSoup

from menschmachine import log, util


@dataclass
class LineRange:
    start: int
    end: int


class Operation(ABC):
    @abstractmethod
    def apply(self, text: str) -> str:
        raise NotImplementedError


@dataclass
class Remove(Operation):
    line_range: LineRange

    def apply(self, text: str) -> str:
        """
        Remove lines from a string based on the given line range.

        Args:
        text (str): The input string.
        start (int): The starting line number to remove (1-indexed).
        end (int): The ending line number to remove (1-indexed, inclusive).

        Returns:
        str: The modified string with specified lines removed.
        """
        # Split the text into lines
        lines = text.splitlines()

        # Adjust for 0-indexing
        start_index = self.line_range.start - 1
        end_index = self.line_range.end - 1

        # Validate input
        if start_index < 0:
            raise ValueError(f"RemoveOperation: Invalid line range: start line {self.line_range.start} is less than 1")
        if end_index >= len(lines):
            raise ValueError(
                f"RemoveOperation: Invalid line range: end line {self.line_range.end} exceeds file length of {len(lines)} lines")
        if start_index > end_index:
            raise ValueError(
                f"RemoveOperation: Invalid line range: start line {self.line_range.start} is greater than end line {self.line_range.end}")

        # Remove the specified lines
        del lines[start_index:end_index + 1]

        # Join the remaining lines and return
        return '\n'.join(lines)


def has_only_one_line(string):
    # Remove leading and trailing whitespace
    string = string.strip()

    # Check if there are any newline characters in the string
    return '\n' not in string


@dataclass
class Modify(Operation):
    line_number: int
    old_content: str
    new_content: str

    @staticmethod
    def _is_string_at_line(file_content: str, target_string: str, line_number: int) -> bool:
        """
        Check if a given string (potentially multiline) starts at the specified line number in the file content.

        Args:
        file_content (str): The content of the file as a string.
        target_string (str): The string to search for (can be multiline).
        line_number (int): The line number where the string should start (1-indexed).

        Returns:
        bool: True if the target string starts at the specified line number, False otherwise.
        """
        # Split the file content and target string into lines
        file_lines = file_content.splitlines()
        target_lines = target_string.splitlines()

        # Check if the starting line number is valid
        if line_number < 1 or line_number > len(file_lines):
            return False

        # Check if there are enough lines in the file to contain the target string
        if len(file_lines) - line_number + 1 < len(target_lines):
            return False

        # Compare the lines
        for i, target_line in enumerate(target_lines):
            if file_lines[line_number - 1 + i] != target_line:
                return False

        return True

    def apply(self, text: str) -> str:
        # check first if linenumber and old_content matches and can be found, if be strict by linenumber, otherwise do fuzzy search and replace
        if self.old_content is None or len(self.old_content.strip()) == 0:
            # means we are inserting at linenumber
            return self._singleline_replace(text)
        elif has_only_one_line(self.old_content) and self._is_string_at_line(text, self.old_content, self.line_number):
            return self._singleline_replace(text)
        else:
            return self._multiline_replace(text)

    def _singleline_replace(self, text: str) -> str:
        """
        Replace a specific line in a string representing a file with new content.

        Args:
        file_content (str): The original file content as a string.
        line_number (int): The line number to be replaced (1-indexed).
        new_content (str): The new content to replace the existing line.

        Returns:
        str: A new string with the specified line replaced by the new content.
        """
        # Split the file content into lines
        lines = text.splitlines()
        # adjust for zero indexing
        if self.line_number > 0:
            replace_index = self.line_number - 1
        else:
            replace_index = self.line_number

        # Validate input
        if replace_index < 0 or replace_index >= len(lines):
            raise ValueError(f"Invalid line number {self.line_number}/{replace_index}/{len(lines)}")

        # Replace the specified line with the new content
        lines[replace_index] = self.new_content

        # Join the lines and return
        return '\n'.join(lines)

    def _multiline_replace(self, text: str) -> str:
        """
        Replace old_content with new_content in a string representing a file,
        ignoring whitespace differences when searching for old_content.

        Args:
        file_content (str): The original file content as a string.
        old_content (str): The content to be replaced (whitespace insensitive).
        new_content (str): The new content to replace the old content.

        Returns:
        str: A new string with the old content replaced by the new content.
        """

        # first try the simple thing
        if self.old_content.strip() in text.strip():
            return text.strip().replace(self.old_content.strip(), self.new_content)

        # Remove leading whitespace from each line
        main_lines = [line.lstrip() for line in text.splitlines()]
        snippet_lines = [line.lstrip() for line in self.old_content.splitlines()]
        # Join the lines back into strings
        main_stripped = '\n'.join(main_lines)
        snippet_stripped = '\n'.join(snippet_lines)

        # Escape special regex characters in the snippet
        snippet_escaped = re.escape(snippet_stripped)

        # Replace newline characters with a regex pattern that allows for any whitespace
        snippet_pattern = snippet_escaped.replace('\\n', r'\s*\n\s*')

        # Search for the snippet in the main string
        match = re.search(snippet_pattern, main_stripped, re.MULTILINE)

        if match is None:
            log.get_logger().error(f"source: {text}, linenumber: {self.line_number}")
            log.get_logger().error(f"old_content: {self.old_content}")
            log.get_logger().error(f"new_content: {self.new_content}")
            raise ValueError("Content not found")
        else:
            # If found, replace the snippet with the replacement string
            result = re.sub(snippet_pattern, self.new_content, main_stripped, flags=re.MULTILINE)

            # Restore the original indentation
            result_lines = result.splitlines()
            indented_result = []
            indentation = 0
            for i, line in enumerate(result_lines):
                if i < len(main_lines):
                    # Use the indentation from the original main string
                    indentation = len(main_lines[i]) - len(main_lines[i].lstrip())
                    indented_result.append(' ' * indentation + line)
                else:
                    # For any additional lines, use the last known indentation
                    indented_result.append(' ' * indentation + line)

            return '\n'.join(indented_result)


@dataclass
class Delete(Modify):
    new_content: str = ""


@dataclass
class Add(Operation):
    after_line_number: int
    content: str

    def apply(self, text: str) -> str:
        """
          Insert new content at a specified line number in a string representing a file.

          Args:
          file_content (str): The original file content as a string.
          new_content (str): The new content to be inserted.
          line_number (int): The line number where the new content should be inserted (1-indexed).

          Returns:
          str: A new string with the new content inserted at the specified line number.
          """
        # Split the file content into lines
        lines = text.splitlines()

        insert_index = self.after_line_number

        # Validate input
        if insert_index < 0 or insert_index > len(lines):
            raise ValueError(f"Invalid line number: {insert_index}/{len(lines)}")

        # Insert the new content
        lines.insert(insert_index, self.content)
        return "\n".join(lines)


@dataclass
class Change:
    file_path: str
    intention: str
    operations: List[Operation] = field(default_factory=list)

    def apply(self, source: str) -> str:
        s = source
        for operation in self.operations:
            s = operation.apply(s)
        return s


@dataclass
class AppliedChanges:
    intention: str
    source: str
    filename: str


@dataclass
class Patch:
    changes: List[Change] = field(default_factory=list)

    def add_delete(self, line_number: int, content: str, file_path: str, intention: str):
        delete = Delete(line_number=line_number, old_content=content)
        change = Change(file_path=file_path, intention=intention)
        change.operations.append(delete)
        self.changes.append(change)

    def add_remove(self, start: int, end: int, file_path: str, intention: str):
        remove = Remove(line_range=LineRange(start, end))
        change = Change(file_path=file_path, intention=intention)
        change.operations.append(remove)
        self.changes.append(change)

    def add_modify(self, line_number: int, old_content: str, new_content: str, file_path: str, intention: str):
        modify = Modify(line_number=line_number, old_content=old_content, new_content=new_content)
        change = Change(file_path=file_path, intention=intention)
        change.operations.append(modify)
        self.changes.append(change)

    def add_add(self, after_line_number: int, content: str, file_path: str, intention: str):
        add = Add(after_line_number=after_line_number, content=content)
        change = Change(file_path=file_path, intention=intention)
        change.operations.append(add)
        self.changes.append(change)

    @staticmethod
    def from_dirty_xml(param: str):
        xml = Patch.xml_from_string(param)
        if xml.find("body"):
            patch = xml.find("body").find("patch")
        else:
            patch = xml
        return Patch.from_xml_object(patch)

    @staticmethod
    def xml_from_string(param: str) -> ET.XML:
        return util.xml_from_string(param)

    @staticmethod
    def from_xml(xml_string):
        try:
            root = ET.fromstring(xml_string)
            return Patch.from_xml_object(root)
        except:
            return Patch.from_dirty_xml(xml_string)

    @staticmethod
    def from_xml_object(root: ET.Element):
        patch = Patch()
        changes = root.find('changes')
        if changes is None and root.find("patch") is not None:
            return Patch.from_xml_object(root.find('patch'))
        if root.find("file_path") is not None:  # single change patch
            changes = [root]
        for change in changes:
            patch_change = Patch.parse_change(change)
            patch.changes.append(patch_change)
        return patch

    @staticmethod
    def parse_change(change):
        file_path = change.find('file_path').text
        intention = change.find('intention').text
        patch_change = Change(file_path=file_path, intention=intention)
        for child in change:
            operation = None
            if child.tag == "remove":
                operation = Patch.get_remove_op(child)
            elif child.tag == "modify":
                operation = Patch.get_modify_op(child)
            elif child.tag == "add":
                operation = Patch.get_add_op(child)
            if operation:
                patch_change.operations.append(operation)
            else:  # LLM generated some xml without explicitly specifying the operations, let's test what makes sense:
                if change.find("content") is not None:  # assuming add
                    operation = Patch.get_add_op(change)
                elif change.find("line_range") is not None:  # assuming delete
                    operation = Patch.get_remove_op(change)
                elif change.find("old_content") is not None and change.find(
                        "new_content") is not None:  # assuming modify
                    operation = Patch.get_modify_op(change)
                if operation is not None:
                    patch_change.operations.append(operation)
                    break  # there can be only one, because of no modify/remove/add tag
        return patch_change

    @staticmethod
    def get_remove_op(child):
        line_range = child.find('line_range')
        start = int(line_range.find('start').text)
        end = int(line_range.find('end').text)
        return Remove(line_range=LineRange(start, end))

    @staticmethod
    def get_add_op(child):
        after_line_number = int(child.find('after_line_number').text)
        content = child.find('content').text.strip()
        return Add(after_line_number=after_line_number, content=content)

    @staticmethod
    def get_modify_op(child):
        try:
            line_number = int(child.find('line_number').text)
        except ValueError:
            line_number = -1
        old_content = child.find('old_content').text
        new_content = child.find('new_content').text
        return Modify(line_number=line_number, old_content=old_content, new_content=new_content)

    def apply(self, get_file_content: Callable[[str], str | None]) -> Iterator[AppliedChanges]:
        for change in self.changes:
            path = change.file_path
            source = get_file_content(path)
            if source is None:
                log.get_logger().error(f"No sources for file {path} found")
                yield AppliedChanges(filename=path, source="", intention=change.intention)
            else:
                yield AppliedChanges(filename=path, source=change.apply(source), intention=change.intention)

    def apply_merged(self, get_file_content: Callable[[str], str | None]) -> Iterator[AppliedChanges]:
        changes_by_file = dict()
        for change in self.changes:
            path = change.file_path
            if path not in changes_by_file:
                changes_by_file[path] = list()
            changes_by_file[path].append(change)
        for k in changes_by_file.keys():
            changes = changes_by_file[k]
            source = get_file_content(k)
            if source is None:
                log.get_logger().debug(f"No sources for file {k} found")
                continue
            intentions = list()
            for change in changes:
                source = change.apply(source)
                intentions.append(change.intention)
            yield AppliedChanges(filename=k, source=source, intention=". ".join(intentions))


@dataclass
class Answer:
    description: str
    patch: Optional[Patch] = None

    def apply(self, get_file_content: Callable[[str], str | None]) -> Iterator[AppliedChanges]:
        if self.patch is not None:
            return self.patch.apply(get_file_content)

    def apply_merged(self, get_file_content: Callable[[str], str | None]) -> Iterator[AppliedChanges]:
        if self.patch is not None:
            return self.patch.apply_merged(get_file_content)

    @staticmethod
    def from_dirty_xml(param: str):
        xml_start = param.index("<")
        xml_end = param.rfind(">")
        xml_string = param[xml_start:xml_end + 1]
        soup = BeautifulSoup(xml_string, "xml")
        xml = ET.fromstring(str(soup))
        if xml.find("body"):
            answer = xml.find("body").find("answer")
        else:
            answer = xml
        return Answer._from_xml_object(answer)

    @staticmethod
    def from_xml(xml_string):
        try:
            root = ET.fromstring(xml_string)
            return Answer._from_xml_object(root)
        except:
            try:
                return Answer.from_dirty_xml(xml_string)
            except ValueError:
                return Answer(description=xml_string)

    @staticmethod
    def _from_xml_object(root):
        desc = None
        try:
            desc = root.find('description').text
        except:
            pass
        answer = Answer(description=desc)
        patch = root.find("patch")
        if patch is not None:
            answer.patch = Patch.from_xml_object(patch)
        return answer
