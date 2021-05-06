from flask import Flask, send_from_directory

import database
import tasks

def setup():
    """Create the app"""
    kanban = Flask(__name__)
    return kanban

app = setup()

@app.route('/')
def index():
    """Gets the main index page"""
    return send_from_directory('static', 'index.html')

@app.route('/api/kanban')
def get_tasks():
    """GET kanban state"""
    return tasks.get_tasks()

@app.route('/api/kanban', methods=["PUT"])
def create_task():
    """PUT for kanban new task"""
    return tasks.create_task()

@app.route('/api/kanban', methods=['POST'])
def order_tasks():
    """POST for kanban lane changes"""
    return tasks.order_tasks()

if __name__ == '__main__':
    app.run(debug=True, port="23456")
