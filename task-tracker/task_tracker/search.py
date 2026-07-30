class Search:
    """Search tasks by id or name"""
    def __init__(self):
        pass

    def search_task_id(self, task_id, logics):
        if task_id == "q":
            return None

        try:
            task_id = int(task_id)
        except ValueError:
            print("Invalid ID")
            return None

        for task in logics.all_tasks:
            if task.id == task_id:
                logics.interface.print_task(task)
                return task

        print("Invalid ID")
        return None

    def search_task(self, logics):
        while True:
            choice = input('Search by task ID (1), Search by task name (2), Return (3)\n:')
            if choice == '1':
                task = self.search_task_id(logics.interface.type_id(), logics)
                logics.interface.update_or_delete_task(task, logics)
            elif choice == '2':
                task = self.search_task_name(logics.interface.type_name(), logics)
                logics.interface.update_or_delete_task(task, logics)
            elif choice == '3':
                break
            else:
                print("Invalid option")

    def search_task_name(self, name, logics):
        if name == "q":
            return None

        for task in logics.all_tasks:
            if task.name == name:
                logics.interface.print_task(task)
                return task

        print("No task with that name")
        return None
