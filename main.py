"""Main controller"""

from database import db, Task
from flask_socketio import SocketIO, emit
from flask import Flask, render_template, url_for, copy_current_request_context, send_from_directory, jsonify, request
from time import sleep
from threading import Thread, Event

import tasks
import cipher
import random

def setup(db):
    """Create the app"""
    kanban = Flask(__name__)
    kanban.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kanban.db'
    kanban.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(kanban)
    kanban.app_context().push()
    db.create_all()
    if db.session.query(Task).first() is None:
        try:
            pre_data = cipher.read_from_file()
            for task in pre_data:
                tasks.create_task(
                    body=task["body"],
                    column=task["column"],
                    sort_order=task["sort_order"],
                    user=task["user"],
                    modified=task["modified"])
        except:
            pass
    return kanban

#Build the app
app = setup(db)
#Turn the flask app into a socketio app
socketio = SocketIO(app, async_mode=None, logger=True, engineio_logger=True)

#Event generator Thread
thread = Thread()
thread_stop_event = Event()

# Async job function
def randomTaskGenerator():
    """Generate random sayings for random people"""
    with app.app_context():
        print("Making random comments")
        people = ["Arthur", "Marvin", "Ford", "Deep Thought"]
        sayings = ["Don't Panic.", "Space is big.", "Where's your towel?", "42", "I don't know why I bother..."]
        while not thread_stop_event.isSet():
            person = people[random.randint(0,3)]
            saying = sayings[random.randint(0,4)]
            print(person + " says '" + saying +"'")
            task_id, user, date = tasks.create_task(body=saying, user=person)
            socketio.emit('new_event', {"id": task_id, "user": user, "body":saying}, namespace='/test')
            socketio.sleep(5)

# Main index load
@app.route('/')
def index():
    """Gets the main index page"""
    return send_from_directory('static', 'index.html')

# Endpoints that do stuff below
@app.route('/api/kanban', methods=["GET"])
def get_tasks():
    """GET kanban state"""
    print("getting...")
    return jsonify(tasks.get_tasks())

@app.route('/api/kanban', methods=["PUT"])
def create_task():
    """PUT for kanban new task"""
    print("creating...")
    task_id, user, date = tasks.create_task(body=request.form.get('text'), user=request.form.get('user'))
    new_task = {"id": task_id, "user": user, "date": date}
    return new_task

@app.route('/api/kanban', methods=['POST'])
def update_task():
    """Update a task"""
    print("updating...")
    id = request.form.get('task_id')
    body = request.form.get('body')
    column = request.form.get('column')
    sort_order = request.form.get('sort_order')
    tasks.update_task(id, body, column, sort_order)
    return "Success"

@app.route('/api/kanban', methods=['DELETE'])
def delete_task():
    """Delete a task"""
    print("Deleting...")
    tasks.delete_task(request.form.get('task_id'))
    return 'Success'

@app.route('/cipher', methods=['GET'])
def save_cipher():
    """Saves current state in cipher"""
    print("Ciphering...")
    data = tasks.get_tasks()
    cipher.write_to_file(data)
    return 'Success'

@socketio.on('connect', namespace='/test')
def test_connect():
    #Need visibility of the global thread object
    global thread
    print('Client connected')

    #Start the random number generator thread only if the thread has not been started before.
    if not thread.isAlive():
        print("Starting Thread")
        thread = socketio.start_background_task(randomTaskGenerator)

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')


#Run the app
if __name__ == '__main__':
    socketio.run(app, debug=True, host="0.0.0.0", port="23456")
