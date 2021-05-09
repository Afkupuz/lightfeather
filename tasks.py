"""Task controller"""

from database import db, Task
from datetime import datetime, timezone

#TODO: Add error handing

# Accepts a body and any number of arguments to add into database
def create_task(body, **kwargs):
    """Create a new task"""
    new_task = Task(body=body, **kwargs)
    #TODO: Handle arg overflow
    db.session.add(new_task)
    db.session.commit()
    print("Created!")
    return (new_task.id, new_task.user, new_task.modified)

# Fetches tasks from the database, ordered by sort order and returns as json
def get_tasks():
    """Return sorted list of tasks"""
    print("Gotten!")
    #TODO: Handle sort order so that it populates lists in order
    return [task.get_json() for task in Task.query.order_by(Task.sort_order.asc()).all()]

# Updates a task with new data
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
    print("Updated!")

# Delete a task
def delete_task(task_id):
    """Delete a task"""
    task = Task.query.get(task_id)
    db.session.delete(task)
    db.session.commit()
    print("Deleted!")
