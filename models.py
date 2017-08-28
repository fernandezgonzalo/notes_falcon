from datetime import datetime as dt
from peewee import *

db = SqliteDatabase('notes.db')


class BaseModel(Model):
    class Meta:
        database = db

class Notebook(BaseModel):
    name = CharField()

    def jsonify(self):
        return {"name": self.name, "id": self.id}


class Note(BaseModel):
    title = CharField()
    body = TextField()
    created = DateTimeField(default=dt.now)
    starred = BooleanField(default=False)
    notebook = ForeignKeyField(Notebook, related_name='notes')

    def jsonify(self):
        return {
            "id": self.id,
            "title": self.title,
            "body": self.body,
            "created": self.created.isoformat(),
            "starred": self.starred,
            "notebook": self.notebook.id
        }

Notebook.create_table(fail_silently=True)
Note.create_table(fail_silently=True)
