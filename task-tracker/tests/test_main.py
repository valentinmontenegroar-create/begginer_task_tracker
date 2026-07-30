import sys
import unittest
from pathlib import Path
from unittest.mock import Mock, patch


PROJECTS_DIR = Path(__file__).resolve().parents[1]
if str(PROJECTS_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECTS_DIR))

from task_tracker.task import Task
from task_tracker.logics import TaskTracker


def make_task(name="Task", description="Description", status="Not done", task_id=1):
    task = Task()
    task.name = name
    task.description = description
    task.status = status
    task.id = task_id
    return task


class TestTaskTracker(unittest.TestCase):
    def test_to_dict_task_serializes_task_fields(self):
        tracker = TaskTracker()
        task = make_task("Write tests", "Cover main.py", "In progress", 7)

        self.assertEqual(
            tracker.to_dict_task(task),
            {
                "name": "Write tests",
                "description": "Cover main.py",
                "status": "In progress",
                "id": 7,
            },
        )

    def test_from_dict_task_builds_task(self):
        task = TaskTracker.from_dict_task(
            {
                "name": "Load task",
                "description": "From json",
                "status": "Done",
                "id": 3,
            }
        )

        self.assertEqual(task.name, "Load task")
        self.assertEqual(task.description, "From json")
        self.assertEqual(task.status, "Done")
        self.assertEqual(task.id, 3)

    def test_id_gen_increments_quantity_and_assigns_id(self):
        tracker = TaskTracker()
        tracker.tasks_quantity = 4
        task = make_task(task_id=None)

        self.assertEqual(tracker.id_gen(task), 5)
        self.assertEqual(tracker.tasks_quantity, 5)
        self.assertEqual(task.id, 5)

    def test_new_task_status_sets_selected_status(self):
        tracker = TaskTracker()
        task = make_task(status=None)

        with patch("builtins.input", return_value="2"):
            tracker.new_task_status(task)

        self.assertEqual(task.status, "In progress")

    def test_update_task_changes_status_and_saves(self):
        tracker = TaskTracker()
        tracker.storage = Mock()
        task = make_task(status="Not done")

        with patch("builtins.input", return_value="3"), patch("builtins.print"):
            tracker.update_task(task)

        self.assertEqual(task.status, "Done")
        tracker.storage.save.assert_called_once_with(tracker)

    def test_delete_task_removes_task_and_saves_when_confirmed(self):
        tracker = TaskTracker()
        tracker.storage = Mock()
        task = make_task()
        tracker.all_tasks = [task]

        with patch("builtins.input", return_value="y"), patch("builtins.print"):
            tracker.delete_task(task)

        self.assertEqual(tracker.all_tasks, [])
        tracker.storage.save.assert_called_once_with(tracker)

    def test_list_by_status_prints_only_matching_tasks(self):
        tracker = TaskTracker()
        tracker.all_tasks = [
            make_task("One", "First", "Done", 1),
            make_task("Two", "Second", "Not done", 2),
        ]

        with patch("builtins.print") as mock_print:
            tracker.list_by_status("Done")

        mock_print.assert_called_once_with("One | First | Done | ID: 1")


if __name__ == "__main__":
    unittest.main()
