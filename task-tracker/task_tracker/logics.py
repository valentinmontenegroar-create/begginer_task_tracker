import datetime

try:
    from task_tracker.task import Task
    from task_tracker.storage import Storage
    from task_tracker.interface import Interface
    from task_tracker.search import Search
except ModuleNotFoundError:
    from task import Task
    from storage import Storage
    from interface import Interface
    from search import Search


class TaskTracker:
    """Adds, updates, deletes tasks, serializes the data and initiates the program"""
    def __init__(self):
        self.all_tasks = []
        self.tasks_quantity = 0
        self.storage = Storage()
        self.interface = Interface()
        self.search = Search()

    def new_task_append(self, new_task):
        self.new_task_status(new_task)
        self.all_tasks.append(new_task)
        new_task.id = self.id_gen(new_task)
        new_task.created_at = datetime.datetime.now()
        print(f"\nTask added successfully (ID: {new_task.id})")
        self.storage.save_task(new_task, self)

    def new_task_status(self, new_task):
        while True:
            status = {'1': 'Not done', '2': 'In progress', '3': 'Done'}
            choice = input("Task Status: Not done (1), In progress (2), Done (3)\n:")
            if choice in status:
                setattr(new_task, 'status', status[choice])
                return
            else:
                print("Invalid option")

    def to_dict_task(self, task):
        # converts task in to a dict to storage it in tasks.json
        return {'name': task.name, 'description': task.description, 'status': task.status, 'id': task.id,
                'created_at': task.created_at.isoformat() if task.created_at else None,
                'updated_at': task.updated_at.isoformat() if task.updated_at else None}

    @classmethod
    def from_dict_task(cls, data):
        # converts task from tasks.json
        task = Task()
        task.name = data['name']
        task.description = data['description']
        task.status = data['status']
        task.id = (data['id'])
        task.created_at = datetime.datetime.fromisoformat(data['created_at']) if data['created_at'] else None
        task.updated_at = datetime.datetime.fromisoformat(data['updated_at']) if data['updated_at'] else None
        return task

    def id_gen(self, new_task):
        # gives to a new task unique id
        self.tasks_quantity += 1
        new_task.id = self.tasks_quantity
        return new_task.id

    def update_task(self, task, choice=None):
        while True:
            options = {'1': 'Not done', '2': 'In progress', '3': 'Done'}
            if choice is None:
                choice = self.interface.choice_update_task()
            if choice in options:
                setattr(task, 'status', options[choice])
                print(f"\nTask updated successfully (ID: {task.id})\n")
                task.updated_at = datetime.datetime.now()
                self.storage.save(self)
                return
            else:
                print("Invalid option")
                choice = None

    def delete_task(self, task):
        self.all_tasks.remove(task)
        print(f"\nTask deleted successfully (ID: {task.id})\n")
        self.storage.save(self)

    def initiate(self, choice=None):
        self.storage.load_all(self)
        while True:
            if choice is None:
                choice = self.interface.choice_initiate()
            if choice == "a":
                self.new_task_append(self.interface.create_new_task())
            elif choice == "s":
                self.search.search_task(self)
            elif choice == "l":
                self.interface.list_tasks_options(self)
            elif choice == "e":
                self.storage.save(self)
                break
            else:
                print("Invalid option")
            choice = None
