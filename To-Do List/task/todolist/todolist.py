import random
import re
from datetime import datetime, timedelta

from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()


class Table(Base):
    __tablename__ = 'Tasks'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


messages = {1: 'The task has been added!\n___________________________________________________________',
            2: 'The task has been deleted!\n___________________________________________________________, ',
            8: 'Nothing is missed!\n___________________________________________________________',
            0: random.choice(['No tasks!\n___________________________________________________________',
                              'Nothing to do!\n___________________________________________________________'])}


def check(data_from_table):
    if len(data_from_table):
        output(data_from_table)
    else:
        print(messages.get(0))
    return bool(len(data_from_table))


def output(data_from_table):
    print('____________________________________________________________')
    for i in range(len(data_from_table)):
        print(f"Task №{i + 1}: {data_from_table[i].task}\n"
              f"Deadline: {data_from_table[i].deadline.strftime('%d %B %Y')}\n"
              f"__________________________________________________________")


today = datetime.today().date()

print("    _________\n      TO-DO\n    ---------\n      Menu\n    ---------")
choice = int(input("add task -> ...1\ndelete task -> ...2\ntoday's tasks -> ...3\nweek's tasks -> ...4\n"
                   "tasks for a specific date -> ...5\nall tasks -> ...6\nleft until deadline date -> ...7\n"
                   "missed tasks -> ...8\nexit -> ...0\n\nyour choice -> ..."))
while choice != 0:
    if choice == 1:
        new_task = Table(task=input('Enter task -> '), deadline=datetime.strptime(input('Enter deadline -> '), '%d %m %Y'))
        session.add(new_task)
        session.commit()
        print(messages.get(1))
    elif choice == 2:
        data = session.query(Table).order_by(Table.deadline).all()
        if check(data):
            session.delete(data[int(input('Choose the number of the task you want to delete ..\nYour choice -> ')) - 1])
            session.commit()
            print(messages.get(2))
    elif choice == 3:
        data = session.query(Table).filter(Table.deadline == today).all()
        check(data)
    elif choice == 4:
        for day in range(7):
            day_of_week = today + timedelta(days=day)
            data = session.query(Table).filter(Table.deadline == day_of_week).all()
            print(f"\n{day_of_week.strftime('%A')}")
            check(data)
    elif choice == 5:
        deadline = datetime.strptime(input('Enter deadline -> '), '%d %m %Y').date()
        data = session.query(Table).filter(Table.deadline == deadline).all()
        check(data)
    elif choice == 6:
        data = session.query(Table).order_by(Table.deadline).all()
        check(data)
    elif choice == 7:
        data = session.query(Table).filter(Table.deadline >= today).all()
        if check(data):
            diff_dates = abs((today - data[int(input('Choose the number of the task ..\nYour choice -> ')) - 1].deadline).days)
            print(f'You have {diff_dates} day(s)\n')
    elif choice == 8:
        data = session.query(Table).filter(Table.deadline < today).all()
        check(data)
    print("    _________\n      TO-DO\n    ---------\n      Menu\n    ---------")
    choice = int(input("add task -> ...1\ndelete task -> ...2\ntoday's tasks -> ...3\nweek's tasks -> ...4\n"
                       "tasks for a specific date -> ...5\nall tasks -> ...6\nleft until deadline date -> ...7\n"
                       "missed tasks -> ...8\nexit -> ...0\n\nyour choice -> ..."))
print('Bye!')
