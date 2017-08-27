import falcon

from graceful.serializers import BaseSerializer
from graceful.fields import IntField, RawField, StringField, BoolField
from graceful.parameters import StringParam
from graceful.resources.generic import (
    RetrieveAPI,
    PaginatedListAPI,
    ListCreateAPI
)

from models import Notebook, Note

api = application = falcon.API()

class NotebookSerializer(BaseSerializer):
    id = IntField("notebook identification number", read_only=True)
    name = StringField("notebook name")


class NoteSerializer(BaseSerializer):
    id = IntField('Note identification', read_only=True)
    title = StringField('Title')
    body = StringField('Body')
    created = RawField('created', read_only=True)
    starred = BoolField('starred')
    notebook = IntField('notebook', read_only=True)

class NoteSerializerCreate(BaseSerializer):
    pass

class NoteItem(RetrieveAPI):
    serializer = NoteSerializer()

    def get_note(self, note_id):
        return Note.get(Note.id == note_id)

    def retrieve(self, params, meta, **kwargs):
        note_id = kwargs['note_id']
        return self.get_note(note_id)


class NoteList(ListCreateAPI):
    serializer = NoteSerializer()

    def list(self, params, meta, **kwargs):
        notebook_id = int(kwargs.get('notebook_id'))
        print(notebook_id)
        notebook = Notebook.get(Notebook.id == notebook_id)
        print(notebook._data)
        print(notebook.notes)
        return [note.jsonify() for note in notebook.notes]

    def create(self, params, meta, validated, **kwargs):
        print(params)
        print(meta)
        print(validated)
        print(kwargs)
        notebook_id = int(kwargs.get('notebook_id'))
        note = Note()
        note.title = validated.get('title')
        note.body = validated.get('body')
        note.starred = False
        note.notebook = Notebook.get(Notebook.id == notebook_id).id
        note.save()
        print(notebook_id)
        return note.jsonify()



class NotebookItem(RetrieveAPI):
    """
    Single cat identified by its id
    """
    serializer = NotebookSerializer()

    def get_notebook(self, notebook_id):
        return Notebook.get(Notebook.id == notebook_id)


    def retrieve(self, params, meta, **kwargs):
        notebook_id = kwargs['notebook_id']
        return self.get_notebook(notebook_id)


class NotebookList(ListCreateAPI):
    serializer = NotebookSerializer()
    
    def list(self, params, meta, **kwargs):
        return [nk for nk in Notebook]
    
    def create(self, params, meta, validated, **kwargs):
        print('params: {}'.format(params))
        print('meta: {}'.format(meta))
        print('validated: {}'.format(validated))
        print('kwargs: {}'.format(kwargs))   
        nb = Notebook()
        nb.name = validated.get('name')
        nb.save()
        return nb

api.add_route("/v1/notebook/{notebook_id}/", NotebookItem())
api.add_route("/v1/notebook/", NotebookList())
api.add_route("/v1/notebook/{notebook_id}/note/{note_id}", NoteItem())
api.add_route("/v1/notebook/{notebook_id}/note/", NoteList())
