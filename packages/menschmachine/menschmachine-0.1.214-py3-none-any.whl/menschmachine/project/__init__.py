import json
from typing import List, Dict, Any
from xml.etree import ElementTree

from menschmachine.patch import Patch


class Task:
    def __init__(self, name: str,
                 description: str = None,
                 estimation_in_minutes: int = None,
                 estimation_in_hours: int = None):
        self.name = name
        self.description = description
        self.estimation_in_hours = estimation_in_hours
        self.estimation_in_minutes = estimation_in_minutes

    def __repr__(self):
        return f"Task(name='{self.name}')"


class Step:
    def __init__(self, name: str, tasks: List[Task]):
        self.name = name
        self.tasks = tasks

    def __repr__(self):
        return f"Step(name='{self.name}', tasks={len(self.tasks)})"

    def add_task(self, task):
        self.tasks.append(task)


class Project:
    def __init__(self, name: str, steps: List[Step]):
        self.name = name
        self.steps = steps

    def __repr__(self):
        return f"Project(name='{self.name}', steps={len(self.steps)})"

    def add_step(self, step):
        self.steps.append(step)

    def to_xml(self) -> str:
        root = ElementTree.Element("project")
        name = ElementTree.SubElement(root, "name")
        name.text = self.name
        steps_elem = ElementTree.SubElement(root, "steps")
        for s in self.steps:
            step_elem = ElementTree.SubElement(steps_elem, "step")
            name = ElementTree.SubElement(step_elem, "name")
            name.text = s.name
            tasks_elem = ElementTree.SubElement(step_elem, "tasks")
            for t in s.tasks:
                task_elem = ElementTree.SubElement(tasks_elem, "task")
                task_name = ElementTree.SubElement(task_elem, "name")
                task_name.text = t.name
                if t.description:
                    task_desc = ElementTree.SubElement(task_elem, "description")
                    task_desc.text = t.description
                if t.estimation_in_minutes:
                    task_m = ElementTree.SubElement(task_elem, "estimation_in_minutes")
                    task_m.text = str(t.estimation_in_minutes)
                if t.estimation_in_hours:
                    task_h = ElementTree.SubElement(task_elem, "estimation_in_hours")
                    task_h.text = str(t.estimation_in_hours)
        return ElementTree.tostring(root, encoding="unicode")

    @classmethod
    def merge(cls, name: str, projects: list['Project']) -> 'Project':
        merged = Project(name=name, steps=[])
        for p in projects:
            for step in p.steps:
                merged.add_step(step)
        return merged


def parse_json(json_data: Dict[str, Any], name_elem: str = "project") -> Project:
    project_name = json_data[name_elem]
    steps = []

    for step_data in json_data['steps']:
        tasks = [Task(task['name'], task['description']) for task in step_data['tasks']]
        step = Step(step_data['name'], tasks)
        steps.append(step)

    return Project(project_name, steps)


# Function to load JSON from file
def load_json_from_file(file_path: str) -> Dict[str, Any]:
    with open(file_path, 'r') as file:
        return json.load(file)


def json_from_file(file_path: str) -> Project:
    json_data = load_json_from_file(file_path)
    return parse_json(json_data)


def parse_xml(xml_string: str) -> Project:
    root = Patch.xml_from_string(xml_string)

    project_name = root.find('name').text
    project = Project(project_name, list())

    for step_elem in root.find('steps').findall('step'):
        step_name = step_elem.find('name').text
        step = Step(step_name, list())

        for task_elem in step_elem.find('tasks').findall('task'):
            task_name = task_elem.find('name').text
            task_description = None
            hours = None
            minutes = None
            description_elem = task_elem.find('description')
            if description_elem is not None:
                task_description = description_elem.text
            hours_elem = task_elem.find('estimation_in_hours')
            if hours_elem is not None:
                hours = int(hours_elem.text)
            minutes_elem = task_elem.find('estimation_in_minutes')
            if minutes_elem is not None:
                minutes = int(minutes_elem.text)
            task = Task(task_name, description=task_description, estimation_in_hours=hours,
                        estimation_in_minutes=minutes)
            step.add_task(task)

        project.add_step(step)

    return project


def xml_from_file(file_path: str) -> Project:
    with open(file_path, 'r') as file:
        return parse_xml(file.read())


class StepCallback:
    def after_apply(self, affected_files: list[str]) -> str:
        pass

    def after_review(self, affected_files: list[str], task_name: str, task_nr: int, total_nr_of_tasks: int) -> None:
        pass
