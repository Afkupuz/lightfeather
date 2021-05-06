"""Task controller"""

from datetime import datetime, timezone
from database import db, Task

def create_task(text):
    """Create a new task"""
    db.session.add(Task(body=text))
    db.session.commit()

def get_tasks():
    """Return sorted list of tasks"""
    tasks = []
    for task in Task.query.order_by(Task.sort_order.asc()).all():
        tasks.append(task.get_json)
    return tasks

def update_task(task_id, text):
    """Update a task"""
    task = Task.query.get(task_id)
    task.body = text
    db.session.commit()

def delete_task(task_id):
    """Delete a task"""
    task = Task.query.get(task_id)
    db.session.delete(task)
    db.session.commit()

def order_tasks():
    """Reposition tasks"""
    #Todo