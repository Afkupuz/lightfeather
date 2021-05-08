"""Task controller"""

from datetime import datetime, timezone
from database import db, Task

def create_task(text, col="", sort=""):
    """Create a new task"""
    if col:
        print("not null")
        new_task = Task(body=text, column=col, sort_order=sort)
    else:
        print("itsnull")
        new_task = Task(body=text)
    db.session.add(new_task)
    db.session.commit()
    return new_task.id

def get_tasks():
    """Return sorted list of tasks"""
    return [task.get_json() for task in Task.query.order_by(Task.sort_order.asc()).all()]

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