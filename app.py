from flask import Flask
from sqlalchemy.engine.base import Connection
from werkzeug.utils import escape
from sqlalchemy import create_engine, Table, MetaData, Column, Integer, String, Boolean, text
from sqlalchemy.orm import declarative_base, sessionmaker

# Instance of Flask
app = Flask(__name__)

# DB connection
engine = create_engine("sqlite+pysqlite:///database.db",
                       echo=False, future=True)

# This is a trivial way to setup tables and metadata
# metaData = MetaData()

# taskTable = Table('tasks', metaData,
#                   Column("id", Integer, primary_key=True, autoincrement=True),
#                   Column("task", String(100))
#                   )


# This is using Declarative Base
Base = declarative_base()

# Creating classes, mapped with DB


class Task(Base):
    __tablename__ = 'task'

    id = Column(Integer, primary_key=True, autoincrement=True)
    objective = Column(String(100))

    def __init__(self, objective=''):
        self.objective = objective

    def __repr__(self):
        return f'id: {self.id}; objective: {self.objective}'


Base.metadata.create_all(engine)

# Here ends the creation (and mounting, probably) of a database

# Accessing the database
Session = sessionmaker(bind=engine)

# current_session = Session()
# clear previous enteries
# for task in current_session.query(Task).all():
#     print(task)
#     current_session.delete(task)
# current_session.execute(text('DELETE FROM task'))
# # make a new task
# task1 = Task()
# task1.objective = "Hey, this is a task"
# task2 = Task()
# task2.objective = "Heyyyyy, another task mate"
# task3 = Task("Third task that we have")

# current_session.add(task1)
# current_session.add(task2)
# current_session.add(task3)
# current_session.commit()


@app.route('/add<get>', methods=['POST', 'GET'])
def addTask():
    return 'We\'ll implement Creation here'


@app.route('/')
def index():
    return "Hello World!"


# @app.route('/table')
# def table():
#     return f"{}"


app.run(debug=True)
