"""Main controller"""

from database import db, Task
from flask import Flask, send_from_directory, jsonify, request

import tasks
import cipher

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
                tasks.create_task(task["body"], task["column"], task["sort_order"])
        except:
            pass
    return kanban

app = setup(db)

@app.route('/')
def index():
    """Gets the main index page"""
    return send_from_directory('static', 'index.html')

@app.route('/api/kanban', methods=["GET"])
def get_tasks():
    """GET kanban state"""
    print("getting...")
    return jsonify(tasks.get_tasks())

@app.route('/api/kanban', methods=["PUT"])
def create_task():
    """PUT for kanban new task"""
    print("creating...")
    task_id = tasks.create_task(request.form.get('text'))
    return str(task_id)

@app.route('/api/kanban', methods=['POST'])
def order_tasks():
    """POST for kanban lane changes"""
    tasks.order_tasks()
    return "Success"

@app.route('/task', methods=['PUT'])
def update_task():
    """Update a task"""
    print("updating...")
    id = request.form.get('task_id')
    body = request.form.get('body')
    column = request.form.get('column')
    sort_order = request.form.get('sort_order')
    tasks.update_task(id, body, column, sort_order)
    return "Success"

@app.route('/task', methods=['DELETE'])
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
    print(data)
    print("Ciphering...")
    cipher.write_to_file(data)
    print("Ciphering...")
    return 'Success'

if __name__ == '__main__':
    app.run(debug=True, port="23456")
