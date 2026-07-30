try:
    from task_tracker.task import Task
except ModuleNotFoundError:
    from task import Task

class Interface:
    """Manage user's inputs: create new task, assign status to new task, list tasks by status, update tasks,
    delete tasks, list all tasks"""

    def __init__(self):
        pass

    def create_new_task(self):
        new_task = Task()
        new_task.name = input("Task Name: ")
        new_task.description = input("Task Description: ")
        return new_task

    def new_task_assign_status(self, new_task):
        status = {'1': 'Not done', '2': 'In progress', '3': 'Done'}
        choice = input("Task Status: Not done (1), In progress (2), Done (3)\n:")
        return status.get(choice)

    def choice_update_task(self):
        choice = input('Not done (1), In progress (2), Done (3)\n:')
        return choice

    def choice_update_or_delete_task(self):
        choice = input('Update (1), Delete (2), Return (3)\n:')
        return choice

    def update_or_delete_task(self, task, logics):
        if task is None:
            return
        while True:
            choice = input('\nUpdate (1), Delete (2), Return (3)\n:')
            if choice == "1":
                logics.update_task(task, self.choice_update_task())
                return
            elif choice == "2":
                self.choice_delete_or_no(logics, task)
                return
            elif choice == "3":
                return
            else:
                print("Invalid option")

    def choice_delete_or_no(self, logics, task):
        while True:
            choice = input("\nDelete task? (y/n)\n:")
            if choice == "y":
                logics.delete_task(task)
                return
            elif choice == "n":
                return
            else:
                print("Invalid option")

    def choice_list_tasks_options(self):
        while True:
            choice = input("\nAll (1), Not done (2), In progress (3), Done (4), Return (5)\n:")
            if choice in {"1", "2", "3", "4", "5"}:
                return choice
            else:
                print("Invalid option")

    def type_id(self):
        # for searching in search.py
        id = input('Task ID (q to return): ')
        return id

    def choice_initiate(self):
        choice = input("\nAdd task (a), See task (s), List tasks (l), Exit (e)\n:")
        return choice

    def type_name(self):
        # for searching in search.py
        name = input('Task Name (q to return): ')
        return name

    def print_task(self, task):
        created_date = task.created_at.strftime("%Y/%m/%d") if task.created_at else "No date"
        print(f"\n{task.name} | {task.description} | {task.status} | Created at: {created_date} | ID: {task.id}")

    def list_tasks_options(self, logics, choice=None):
        while True:
            if choice is None:
                choice = self.choice_list_tasks_options()
            if choice == "1":
                self.list_all_tasks(logics)
                return
            elif choice == "2":
                self.list_by_status('Not done', logics)
                return
            elif choice == "3":
                self.list_by_status('In progress', logics)
                return
            elif choice == "4":
                self.list_by_status('Done', logics)
                return
            elif choice == "5":
                return
            else:
                print("Invalid option")
                choice = None

    def list_all_tasks(self, logics):
        for task in logics.all_tasks:
            self.print_task(task)

    def list_by_status(self, status, logics):
        for task in logics.all_tasks:
            if task.status == status:
                self.print_task(task)
