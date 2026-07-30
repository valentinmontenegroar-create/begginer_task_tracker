
try:
    from task_tracker.logics import TaskTracker
except ModuleNotFoundError:
    from logics import TaskTracker

if __name__ == "__main__":
    task_tracker = TaskTracker()
    task_tracker.initiate()


