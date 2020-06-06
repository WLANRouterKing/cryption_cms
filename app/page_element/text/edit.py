from wtforms import StringField

from app.backend.forms import Texteditor, PageElementEditorBaseForm


class PageElementEditorForm(PageElementEditorBaseForm):
    headline = StringField("Überschrift")
    text = Texteditor("Text")

    def __init__(self):
        super().__init__()
        self.type = "content"
        self.page = "edit_page_element"
        self.module = "page_element"
