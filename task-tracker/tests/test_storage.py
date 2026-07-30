import json
import os
import sys
import tempfile
import unittest
from pathlib import Path


PROJECTS_DIR = Path(__file__).resolve().parents[1]
if str(PROJECTS_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECTS_DIR))

from task_tracker.task import Task
from task_tracker.logics import TaskTracker
from task_tracker.storage import Storage


def make_task(name="Task", description="Description", status="Not done", task_id=1):
    task = Task()
    task.name = name
    task.description = description
    task.status = status
    task.id = task_id
    return task


class StorageTestCase(unittest.TestCase):
    def setUp(self):
        self.previous_cwd = os.getcwd()
        self.temp_dir = tempfile.TemporaryDirectory()
        os.chdir(self.temp_dir.name)
        self.storage = Storage()

    def tearDown(self):
        os.chdir(self.previous_cwd)
        self.temp_dir.cleanup()


class TestStorage(StorageTestCase):
    def test_save_all_tasks_writes_serialized_tasks(self):
        tracker = TaskTracker()
        tracker.all_tasks = [make_task("Write tests", "For storage", "Done", 1)]

        self.storage.save_all_tasks(tracker)

        with open("../task_tracker/tasks.json", "r") as f:
            self.assertEqual(
                json.load(f),
                [
                    {
                        "name": "Write tests",
                        "description": "For storage",
                        "status": "Done",
                        "id": 1,
                    }
                ],
            )

    def test_save_tasks_quantity_writes_quantity(self):
        tracker = TaskTracker()
        tracker.tasks_quantity = 8

        self.storage.save_tasks_quantity(tracker)

        with open("../task_tracker/tasks_quantity.json", "r") as f:
            self.assertEqual(json.load(f), 8)

    def test_load_tasks_populates_tracker_from_json(self):
        with open("../task_tracker/tasks.json", "w") as f:
            json.dump(
                [
                    {
                        "name": "Loaded",
                        "description": "From file",
                        "status": "In progress",
                        "id": 4,
                    }
                ],
                f,
            )
        tracker = TaskTracker()

        self.storage.load_tasks(tracker)

        self.assertEqual(len(tracker.all_tasks), 1)
        self.assertEqual(tracker.all_tasks[0].name, "Loaded")
        self.assertEqual(tracker.all_tasks[0].description, "From file")
        self.assertEqual(tracker.all_tasks[0].status, "In progress")
        self.assertEqual(tracker.all_tasks[0].id, 4)

    def test_load_tasks_ignores_empty_json_file(self):
        Path("../task_tracker/tasks.json").write_text("")
        tracker = TaskTracker()

        self.storage.load_tasks(tracker)

        self.assertEqual(tracker.all_tasks, [])

    def test_load_tasks_quantity_reads_existing_quantity(self):
        with open("../task_tracker/tasks_quantity.json", "w") as f:
            json.dump(5, f)
        tracker = TaskTracker()

        self.storage.load_tasks_quantity(tracker)

        self.assertEqual(tracker.tasks_quantity, 5)

    def test_load_tasks_quantity_creates_quantity_from_tasks_when_missing(self):
        with open("../task_tracker/tasks.json", "w") as f:
            json.dump(
                [
                    {
                        "name": "First",
                        "description": "One",
                        "status": "Done",
                        "id": 1,
                    },
                    {
                        "name": "Second",
                        "description": "Two",
                        "status": "Not done",
                        "id": 2,
                    },
                ],
                f,
            )
        tracker = TaskTracker()

        self.storage.load_tasks_quantity(tracker)

        self.assertEqual(tracker.tasks_quantity, 2)
        with open("../task_tracker/tasks_quantity.json", "r") as f:
            self.assertEqual(json.load(f), 2)

    def test_save_task_appends_to_existing_tasks_file(self):
        with open("../task_tracker/tasks.json", "w") as f:
            json.dump(
                [
                    {
                        "name": "Existing",
                        "description": "Already saved",
                        "status": "Done",
                        "id": 1,
                    }
                ],
                f,
            )
        tracker = TaskTracker()
        new_task = make_task("New", "Added later", "Not done", 2)

        self.storage.save_task(new_task, tracker)

        with open("../task_tracker/tasks.json", "r") as f:
            tasks = json.load(f)
        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[1]["name"], "New")
        self.assertEqual(tasks[1]["id"], 2)

    def test_save_writes_tasks_and_quantity(self):
        tracker = TaskTracker()
        tracker.all_tasks = [make_task("Saved", "All data", "Done", 1)]
        tracker.tasks_quantity = 1

        self.storage.save(tracker)

        self.assertTrue(Path("../task_tracker/tasks.json").exists())
        self.assertTrue(Path("../task_tracker/tasks_quantity.json").exists())


if __name__ == "__main__":
    unittest.main()
