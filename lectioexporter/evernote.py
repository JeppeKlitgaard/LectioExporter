import evernote.edam.type.ttypes as Types
from .config import EVERNOTE_DEV_TOKEN_FILE

CONTENT_TEMPLATE = ("<?xml version=\"1.0\" encoding=\"UTF-8\"?>"

                    "<!DOCTYPE en-note SYSTEM "
                    "\"http://xml.evernote.com/pub/enml2.dtd\">"

                    "<en-note>{content}</en-note>")


def get_evernote_token():
    with open(EVERNOTE_DEV_TOKEN_FILE, "r") as f:
        return f.read()


def make_note(auth_token, note_store, note_title, note_content,
              parent_notebook_guid=None):
    content = CONTENT_TEMPLATE.format(content=note_content)

    our_note = Types.Note()
    our_note.title = note_title
    our_note.content = content

    if parent_notebook_guid is not None:
        our_note.notebookGuid = parent_notebook_guid

    note = note_store.createNote(auth_token, our_note)

    return note
