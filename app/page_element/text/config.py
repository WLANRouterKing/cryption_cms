from wtforms import StringField

from app.backend.forms import Texteditor

page_element_config = dict()
page_element_config["headline"] = ["Überschrift", StringField("Überschrift")]
page_element_config["text"] = ["Text", Texteditor("Text")]
