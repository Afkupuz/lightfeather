"""SQLAlchemy database"""
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime, timezone

db = SQLAlchemy()

class Task(db.Model):
    """SQLAlchemy task model"""
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(120))
    column = db.Column(db.String(120), default="backlog")
    sort_order = db.Column(db.Integer, default=0)

    def get_json(self):
        """Return a JSON representation of task"""
        return {
            'id': self.id,
            'body': self.body,
            'column': self.column,
            'sort_order': self.sort_order,
        }