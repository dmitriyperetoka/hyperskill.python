from datetime import datetime, timedelta
from typing import List

from sqlalchemy import Column, Date, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import NullPool
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
default_engine_params = "sqlite:///todo.db?check_same_thread=False"


class Tasks(Base):
    """Model of the main table in the database."""

    __tablename__ = "task"
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today().date())

    def __repr__(self) -> str:
        return self.task


class ToDoList:
    """To-do list with database that can store and manage tasks."""

    def __init__(self, engine_params: str = default_engine_params) -> None:
        self.engine = create_engine(engine_params, poolclass=NullPool)
        self.session = None
        self.menu = {
            "main": {
                "1": (self.print_today_tasks, "Today's tasks"),
                "2": (self.print_week_tasks, "Week's tasks"),
                "3": (self.print_all_tasks, "All tasks"),
                "4": (self.print_missed_tasks, "Missed tasks"),
                "5": (self.add_task, "Add task"),
                "6": (self.delete_task, "Delete task"),
            },
        }
        self.selected_menu_area = "main"

    @staticmethod
    def print_tasks(tasks: List[Tasks]) -> None:
        """Print enumerated list of specified tasks."""
        if tasks:
            for number, task in enumerate(tasks, 1):
                print(f"{number}. {task}")
        else:
            print("Nothing to do!")

    @staticmethod
    def print_tasks_and_deadlines(tasks: List[Tasks]) -> None:
        """Print enumerated list of specified tasks with their
        deadlines.
        """
        for number, task in enumerate(tasks, 1):
            deadline = task.deadline.strftime("%d %b").lstrip("0")
            print(f"{number}. {task}. {deadline}")

    def print_today_tasks(self) -> None:
        """Print tasks which deadlines are the current system date."""
        print("Today:")
        tasks = self.session.query(
            Tasks
        ).filter(
            Tasks.deadline == datetime.today().date()
        ).all()
        self.print_tasks(tasks)

    def print_week_tasks(self) -> None:
        """Print tasks which deadlines are the upcoming seven days
        starting with the current system date grouped by days.
        """
        for q in range(7):
            the_day = datetime.today().date() + timedelta(days=q)
            print(the_day.strftime("%A %d %b:"))
            tasks = self.session.query(
                Tasks
            ).filter(
                Tasks.deadline == the_day
            ).all()
            self.print_tasks(tasks)

            if q < 6:
                print()

    def print_all_tasks(self) -> None:
        """Print all tasks in the database with their deadlines."""
        print("All tasks:")
        tasks = self.session.query(Tasks).order_by(Tasks.deadline).all()

        if tasks:
            self.print_tasks_and_deadlines(tasks)
        else:
            print("Nothing to do!")

    def print_missed_tasks(self) -> None:
        """Print tasks which deadlines are earlier than the current
        system date.
        """
        print("Missed tasks:")
        tasks = self.session.query(
            Tasks
        ).filter(
            Tasks.deadline < datetime.today().date()
        ).order_by(
            Tasks.deadline
        ).all()

        if tasks:
            self.print_tasks_and_deadlines(tasks)
        else:
            print("Nothing is missed!")

    def add_task(self) -> None:
        """Create a task as a new record in the database"""
        print("Enter task:")
        task = input()
        print(
            "Enter deadline (format: YYYY-MM-DD) "
            "or blank line to set default (today):"
        )
        deadline = input()

        if deadline == "":
            deadline = None
        else:
            deadline = datetime.strptime(deadline, "%Y-%m-%d").date()

        self.session.add(Tasks(task=task, deadline=deadline))
        self.session.commit()
        print("The task has been added!")

    def delete_task(self) -> None:
        """Delete specified task from the database."""
        tasks = self.session.query(Tasks).order_by(Tasks.deadline).all()

        if tasks:
            print("Choose the number of the task you want to delete:")
            self.print_tasks_and_deadlines(tasks)
            task_number = int(input())

            if 0 < task_number <= len(tasks):
                self.session.delete(tasks[task_number - 1])
                self.session.commit()
                print("The task has been deleted!")
            else:
                print("No such task number!")

        else:
            print("Nothing to delete!")

    def setup(self) -> None:
        self.session = sessionmaker(bind=self.engine).__call__()
        Base.metadata.create_all(bind=self.engine)

    def print_menu(self) -> None:
        """Print the options of the currently selected menu area."""
        for item in self.menu[self.selected_menu_area]:
            print(f"{item}) {self.menu[self.selected_menu_area][item][1]}")
        print("0) Exit")

    def run(self) -> None:
        """Run the main loop of the program."""
        self.setup()

        while True:
            self.print_menu()
            command = input()
            print()

            if command == "0":
                self.session.close()
                self.session = None
                print("Bye!")
                break
            elif command in self.menu[self.selected_menu_area]:
                try:
                    self.menu[self.selected_menu_area][command][0].__call__()
                except ValueError:
                    print("Unexpected input format!")
            else:
                print("Unknown command!")

            print()


def main() -> None:
    """Initialize the program."""
    todo_list = ToDoList()
    todo_list.run()


if __name__ == "__main__":
    main()
