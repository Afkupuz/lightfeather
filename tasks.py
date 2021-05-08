"""Task controller"""

from database import db, Task
from datetime import datetime, timezone

def create_task(text, **kwargs):
    """Create a new task"""
    new_task = Task(body=text, **kwargs)
    db.session.add(new_task)
    db.session.commit()
    return (new_task.id, new_task.user, new_task.modified)

def get_tasks():
    """Return sorted list of tasks"""
    return [task.get_json() for task in Task.query.order_by(Task.sort_order.asc()).all()]

def update_task(task_id, body="", column="", sort_order="", user=""):
    """Update a task"""
    task = Task.query.get(task_id)
    print("madeit: "+body+column+sort_order)
    modified = False
    if body:
        modified = True
        task.body = body
    if column:
        modified = True
        task.column = column
    if sort_order:
        modified = True
        task.sort_order = sort_order
    if user:
        modified = True
        task.user = user
    if modified:
        task.modified = datetime.utcnow()
    db.session.commit()

def delete_task(task_id):
    """Delete a task"""
    task = Task.query.get(task_id)
    db.session.delete(task)
    db.session.commit()

def order_tasks():
    """Reposition tasks"""
    #Todo