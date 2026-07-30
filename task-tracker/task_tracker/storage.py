import json

class Storage:
    """Controls the saving and loading of tasks"""

    def save_tasks_quantity(self, a):
        with open('tasks_quantity.json', 'w') as f:
            json.dump(a.tasks_quantity, f)

    def save_all_tasks(self, a):
        tasks = [a.to_dict_task(task) for task in a.all_tasks]
        with open('tasks.json', 'w') as f:
            json.dump(tasks, f)

    def load_tasks_quantity(self, a):
        try:
            with open('tasks_quantity.json', 'r') as f:
                a.tasks_quantity = json.load(f)
        except FileNotFoundError:
            try:
                with open('tasks.json', 'r') as f:
                    tasks = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                tasks = []
            a.tasks_quantity = len(tasks)
            with open('tasks_quantity.json', 'w') as f:
                json.dump(a.tasks_quantity, f)

    def load_tasks(self, a):
        try:
            with open('tasks.json', 'r') as f:
                tasks = json.load(f)
                for data in tasks:
                    task = a.from_dict_task(data)
                    a.all_tasks.append(task)
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def save(self, a):
        self.save_all_tasks(a)
        self.save_tasks_quantity(a)

    def save_task(self, task, a):
        try:
            with open('tasks.json', 'r') as f:
                tasks = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            tasks = []
        tasks.append(a.to_dict_task(task))
        with open('tasks.json', 'w') as f:
            json.dump(tasks, f)
        self.save_tasks_quantity(a)

    def load_all(self, a):
        self.load_tasks(a)
        self.load_tasks_quantity(a)
