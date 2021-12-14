from flask import Flask, request
from flask.json import JSONDecoder
from sqlalchemy.engine.base import Connection
import markupsafe as Markupsafe
from sqlalchemy import create_engine, Table, MetaData, Column, Integer, String, Boolean, text
from sqlalchemy.orm import declarative_base, sessionmaker
import json
import sys

import os

# Instance of Flask
app = Flask(__name__)

# DB connection
engine = create_engine("sqlite+pysqlite:///database.db",
                       echo=False, future=True)

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

# Implement post api
# Add task using the url itself


@app.route('/api/add/usingUrl/<string:receivedString>/', methods=['GET', 'POST'])
def addUsingUrl(receivedString):
    try:
        session = Session()
        newTask = Task()
        newTask.objective = Markupsafe.escape(receivedString)
        session.add(newTask)
        session.commit()

    except:
        session.close()
        return "Couldn't add task!, check syntax", 406

    finally:
        session.close()
    return "Task '%s' added successfully!" % receivedString

# Add task using form


@app.route('/api/add/usingJson', methods=['POST'])
def addUsingJson():
    try:
        session = Session()
        newTask = Task()
        receivedDict = json.loads(request.data)
        newTask.objective = receivedDict['task']
        session.add(newTask)
        session.commit()
        session.close()
        return "Task added successfully!"
    except:
        return "Wrong format of data, pass formData, {'task':'task'}", 406

# Get all tasks


@app.route('/api/getTasks')
def getTasks():
    session = Session()
    resultDict = {}
    try:
        for task in session.query(Task).order_by(Task.id).all():
            resultDict[task.id] = task.objective
    except:
        return 'Error occured', 400
    finally:
        session.close()
        return resultDict


@app.route('/api/deleteById/<int:task_id>/', methods=['DELETE'])
def deleteById(task_id):
    task_id = int(task_id)
    session = Session()
    currentTask = session.query(Task).where(Task.id == task_id).first()
    session.delete(currentTask)
    session.commit()
    session.close()
    return "Task Deleted successfully!"


@app.route('/api/update/', methods=['PUT'])
def updateById():
    try:
        receivedData = json.loads(request.data)
        session = Session()
        session.query(Task).filter(Task.id == int(receivedData['id'])).update(
            {Task.objective: str(receivedData['task'])}, synchronize_session=False)
        session.commit()
        session.close()
        return "Updated task successfully"
    except:
        session.close()
        print(sys.exc_info(),)
        return "Failed to update task", 406


@app.route('/')
def index():
    return "Hello World!"


app.run(debug=True)
