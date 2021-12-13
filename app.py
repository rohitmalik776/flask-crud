from flask import Flask, request
from flask.json import JSONDecoder
from sqlalchemy.engine.base import Connection
import markupsafe as Markupsafe
from sqlalchemy import create_engine, Table, MetaData, Column, Integer, String, Boolean, text
from sqlalchemy.orm import declarative_base, sessionmaker
import json

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
@app.route('/api/add/usingUrl/<string:receivedString>/', methods=['GET','POST'])
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
    return "Task '%s' added successfully!" %receivedString

# Add task using form
@app.route('/api/add/usingForm', methods=['POST'])
def addUsingForm():
    session = Session()
    newTask = Task()
    receivedDict = json.loads(request.data)
    newTask.objective = receivedDict['task']
    session.add(newTask)
    session.close()
    return "Task added successfully!"

@app.route('/')
def index():
    return "Hello World!"


# @app.route('/table')
# def table():
#     return f"{}"


app.run(debug=True)
