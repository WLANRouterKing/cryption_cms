from wtforms import HiddenField, StringField, SelectField, TextField, FieldList, SubmitField

from app.backend.forms import Texteditor
from app.forms import CustomForm


class PageElementEditorForm(CustomForm):
    id = HiddenField()
    eid = HiddenField()
    headline = StringField("Überschrift")
    text = Texteditor("Text")
    submit = SubmitField("News Meldung speichern")

    def __init__(self):
        super().__init__()
        self.type = "content"
        self.page = "edit_page_element"
        self.module = "page_element"
