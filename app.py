from flask import Flask
from sqlalchemy.engine.base import Connection
from werkzeug.utils import escape
from sqlalchemy import create_engine, Table, MetaData, Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base

# Instance of Flask
app = Flask(__name__)

# DB connection
engine = create_engine("sqlite+pysqlite:///database.db",
                       echo=True, future=True)

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

    def __repr__(self):
        return f'id: {self.id}; objective: {self.objective}'


Base.metadata.create_all(engine)

# Here ends the creation (and mounting, probably) of a database


@app.route('/')
def index():
    return "Hello World!"


# @app.route('/table')
# def table():
#     return f"{}"


app.run(debug=True)
