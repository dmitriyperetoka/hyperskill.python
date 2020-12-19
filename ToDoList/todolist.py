from datetime import datetime, timedelta

from sqlalchemy import Column, Date, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import NullPool
from sqlalchemy.orm import sessionmaker

today = datetime.today().date()

Base = declarative_base()

default_engine_properties = "sqlite:///todo.db?check_same_thread=False"


class Tasks(Base):
    __tablename__ = "task"
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=today)

    def __repr__(self):
        return self.task


class ToDoList:
    def __init__(self, engine_properties=default_engine_properties):
        self.engine = create_engine(engine_properties, poolclass=NullPool)
        self.session = None

    @staticmethod
    def show_tasks(tasks):
        if tasks:
            for number, task in enumerate(tasks, 1):
                print(f"{number}. {task}")
            print()
        else:
            print("Nothing to do!\n")

    @staticmethod
    def show_tasks_and_deadlines(tasks):
        for number, task in enumerate(tasks, 1):
            deadline = task.deadline.strftime("%d %b").lstrip("0")
            print(f"{number}. {task}. {deadline}")

    def show_today_tasks(self):
        print("\nToday:")
        tasks = self.session.query(Tasks).filter(Tasks.deadline == today).all()
        self.show_tasks(tasks)

    def show_week_tasks(self):
        print()
        for q in range(7):
            the_day = today + timedelta(days=q)
            print(the_day.strftime("%A %d %b:"))
            tasks = self.session.query(
                Tasks
            ).filter(
                Tasks.deadline == the_day
            ).all()
            self.show_tasks(tasks)

    def show_all_tasks(self):
        print("\nAll tasks:")
        tasks = self.session.query(Tasks).order_by(Tasks.deadline).all()

        if tasks:
            self.show_tasks_and_deadlines(tasks)
            print()
        else:
            print("Nothing to do!\n")

    def show_missed_tasks(self):
        print("\nMissed tasks:")
        tasks = self.session.query(
            Tasks
        ).filter(
            Tasks.deadline < today
        ).order_by(
            Tasks.deadline
        ).all()

        if tasks:
            self.show_tasks_and_deadlines(tasks)
            print()
        else:
            print("Nothing is missed!\n")

    def add_task(self):
        print("\nEnter task")
        task = input()
        print(
            "Enter deadline (format: YYYY-MM-DD) "
            "or blank line to set default (today)"
        )
        deadline = input()

        if deadline == "":
            deadline = None
        else:
            deadline = datetime.strptime(deadline, "%Y-%m-%d").date()

        self.session.add(Tasks(task=task, deadline=deadline))
        self.session.commit()
        print("The task has been added!\n")

    def delete_task(self):
        tasks = self.session.query(
            Tasks
        ).order_by(
            Tasks.deadline
        ).all()

        if tasks:
            print("\nChoose the number of the task you want to delete:")
            self.show_tasks_and_deadlines(tasks)
            task_number = int(input())

            if 0 < task_number <= len(tasks):
                self.session.delete(tasks[task_number - 1])
                self.session.commit()
                print("The task has been deleted!\n")
            else:
                print("\nNo such task number!\n")

        else:
            print("\nNothing to delete!\n")

    @property
    def menu(self):
        return {
            "1": (self.show_today_tasks, "Today's tasks"),
            "2": (self.show_week_tasks, "Week's tasks"),
            "3": (self.show_all_tasks, "All tasks"),
            "4": (self.show_missed_tasks, "Missed tasks"),
            "5": (self.add_task, "Add task"),
            "6": (self.delete_task, "Delete task"),
        }

    def show_menu(self):
        for item in self.menu:
            print(f"{item}) {self.menu[item][1]}")
        print("0) Exit\n")

    def run(self):
        self.session = sessionmaker(bind=self.engine).__call__()
        Base.metadata.create_all(bind=self.engine)

        while True:
            self.show_menu()
            command = input()

            if command == "0":
                self.session.close()
                self.session = None
                print("\nBye!")
                break

            if command in self.menu:
                try:
                    self.menu[command][0].__call__()
                except ValueError:
                    print("\nUnexpected input format!\n")
                    continue
            else:
                print("\nUnknown command!\n")


def main():
    todo_list = ToDoList()
    todo_list.run()


if __name__ == "__main__":
    main()
