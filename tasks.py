"""Task controller"""

from database import db, Task
from datetime import datetime, timezone

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

def update_task(task_id, body="", column="", sort_order=""):
    """Update a task"""
    task = Task.query.get(task_id)
    print("madeit: "+body+column+sort_order)
    if body:
        task.body = body
    if column:
        task.column = column
    if sort_order:
        task.sort_order = sort_order
    db.session.commit()

def delete_task(task_id):
    """Delete a task"""
    task = Task.query.get(task_id)
    db.session.delete(task)
    db.session.commit()

def order_tasks():
    """Reposition tasks"""
    #Todo