from database import db
from flask import Flask, send_from_directory, jsonify, request

import tasks

def setup(db):
    """Create the app"""
    kanban = Flask(__name__)
    kanban.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kanban.db'
    db.init_app(kanban)
    #Todo: load from file
    return kanban

app = setup(db)

@app.route('/')
def index():
    """Gets the main index page"""
    return send_from_directory('static', 'index.html')

@app.route('/api/kanban')
def get_tasks():
    """GET kanban state"""
    return tasks.get_tasks()

@app.route('/api/kanban', methods=["PUT"])
def create_task(text):
    """PUT for kanban new task"""
    tasks.create_task(text)
    return True

@app.route('/api/kanban', methods=['POST'])
def order_tasks():
    """POST for kanban lane changes"""
    tasks.order_tasks()
    return True

@app.route('/task', methods=['PUT'])
def update_task(task_id, text):
    """Update a task"""
    tasks.update_task(task_id, text)
    return True

@app.route('/task', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task"""
    task.delete_task(task_id)
    return 'Success'

@app.route('/background_process')
def background_process():
	try:
		lang = request.args.get('proglang', 0, type=str)
		if lang.lower() == 'python':
			return jsonify(result='You are wise')
		else:
			return jsonify(result='Try again.')
	except Exception as e:
		return str(e)

if __name__ == '__main__':
    app.run(debug=True, port="23456")
