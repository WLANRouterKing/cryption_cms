from .config import page_element_config
from ...backend.forms import PageElementEditorBaseForm

for key in page_element_config:
    setattr(PageElementEditorBaseForm, key, page_element_config[key][1])
page_element_editor_form = PageElementEditorBaseForm()
