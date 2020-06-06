from flask import session, flash, current_app, url_for
from flask_wtf import FlaskForm
from datetime import timedelta
from re import search
from app.libs.libs import get_url_for_abs_path
from . import debug_logger
from .backend import backend
from markupsafe import iteritems
from wtforms.csrf.session import SessionCSRF
from app.page_element_config import PAGE_ELEMENTS
import json

from .models import PageElement


class CustomForm(FlaskForm):

    def __init__(self):
        super().__init__()
        self.id = 0
        self.display_tabs = True
        self.filter_label = ["csrf_token", "submit", "Id", "EID"]
        self.tabs = ["content", "meta", "ctrl"]
        self.method = "post"
        self.type = None
        self.module = None
        self.blueprint_name = backend.name
        self.form_id = "{0}-{1}-{2}".format(self.type, self.module, "form")
        self.page = ""
        self.form_object = None

    def init_values(self, object):
        """
        initialisiert diese Form anhand des übergebenen Benutzer Objekts

        Args:
            user: Der Benutzer dessen Daten initialisiert werden sollen

        Returns:
            bool: True wenn alle Daten initialisiert werden konnten andernfalls False

        """
        self.form_object = object
        elements = self.get_all_elements()
        for key in elements:
            if key == "id":
                self.id = int(object.get(key))
            element = elements[key]
            value = object.get(key)
            element.data = value
            
    @property
    def action(self):
        page = "{0}.{1}".format(self.blueprint_name, self.page)
        if int(self.id) > 0:
            return url_for(page, id=self.id)
        return url_for(page)

    def get_all_elements(self):
        elements = dict()
        for field in self:
            elements[field.label.field_id] = field
        return elements

    def get_editor_add_message(self, object):
        label = object.class_label
        message = """{0} erstellen""".format(label)
        flash(message, "info")

    def get_editor_edit_message(self, object):
        label = object.class_label
        message = "{0} bearbeiten".format(label)
        return message

    def get_error_messages(self):
        for key, field in iteritems(self._fields):
            element = field
            if element.errors:
                flash(element.errors, "danger")

    def is_element_seo(self, element_id):
        if search("meta", element_id) is not None:
            return True
        return False

    def is_element_control(self, element_id):
        if search("ctrl", element_id) is not None or search("page_id", element_id) is not None:
            return True
        return False

    def is_element_submit(self, element_id):
        if element_id == "submit":
            return True
        return False

    def get_image_upload_info(self, element):
        width = current_app.config["IMAGE_FORMATS"][self.module][element.label.field_id]["width"]
        height = current_app.config["IMAGE_FORMATS"][self.module][element.label.field_id]["height"]
        max_images = current_app.config["IMAGE_FORMATS"][self.module][element.label.field_id]["max_files"]
        max_size = current_app.config["IMAGE_FORMATS"][self.module][element.label.field_id]["max_size"]
        return "Bilder im Format {0}x{1} max Anzahl: {2} max Größe: {3} MB".format(width, height, str(max_images),
                                                                                   str(max_size))

    def get_document_upload_info(self, element):
        return "Dokumente"

    def get_upload_message(self):
        return "Dateien hier ablegen zum Hochladen"

    def get_fileupload_container_html(self, element):
        image_format = ""
        max_images = 0
        max_size = 0
        if current_app.config["IMAGE_FORMATS"][self.module][element.label.field_id] is not None:
            image_format = element.label.field_id
            max_images = current_app.config["IMAGE_FORMATS"][self.module][element.label.field_id]["max_files"]
            max_size = current_app.config["IMAGE_FORMATS"][self.module][element.label.field_id]["max_size"]
        html = "<div class='fileupload-container form-control'>"
        html += '<input type="hidden" class="image-format" name="image-format" value="{0}">'.format(image_format)
        html += '<input type="hidden" class="max_files" name="max_files" value="{0}">'.format(max_images)
        html += '<input type="hidden" class="max_size" name="max_size" value="{0}">'.format(max_size)
        html += '<span class="label">{0}</span>'.format(element.label)
        html += '<div class="dz-preview">'
        if max_images > 1:
            for image_src in self.form_object.get_list_or_dict(image_format):
                html += '<img src="' + get_url_for_abs_path(image_src) + '" alt=""/>'
        else:
            html += '<img src="' + get_url_for_abs_path(self.form_object.get(image_format)) + '" alt=""/>'
        html += '</div>'
        html += "<div class='dz-message form-control'>"
        html += "<span class='upload-message'>{0}</span>".format(self.get_upload_message())
        html += "</div>"
        if element.type == "ImageUploadField":
            html += "<span class='info'>{0}</span>".format(self.get_image_upload_info(element))
            html += "<span class='extensions'>{0}</span>".format(current_app.config["ALLOWED_IMAGE_EXTENSIONS"])
        elif element.type == "DocumentUploadField":
            html += "<span class='info'>{0}".format(self.get_document_upload_info(element))
            html += "<span class='extensions'>{0}</span>".format(current_app.config["ALLOWED_DOCUMENT_EXTENSIONS"])
        html += "<div class='fallback'>{0}</div>".format(element)
        html += str(element)
        html += "</div>"
        html += "</div>"
        return html

    def get_element_html(self, element):
        html = "<div class='form-group'>"
        element_type = getattr(element.widget, 'type', None)
        element_input_type = getattr(element.widget, 'input_type', None)
        element_label = ""
        element_classes = {"class": ""}

        for exclude_label in self.filter_label:
            if str(element.label.field_id).lower() == str(exclude_label).lower():
                element_label = None

        if element_label is not None:
            element_label = element.label

        if element.type == "Texteditor":
            element_classes["class"] += "texteditor "

        if element_input_type is not None:

            if element.widget.input_type != "checkbox":
                """
                non checkbox form elements
                """
                element_classes["class"] += "form-control "
                element_classes["class"] += "form-control-sm "

            if element.widget.input_type == "checkbox":
                """
                checkbox form element
                """
                html = "<div class='form-group form-check'>"
                element_classes["class"] += "form-check-input "
            elif element.widget.input_type == "submit":
                """
                input type form elements
                """
                element_label = None
                element_classes["class"] += "btn-dark "
            elif element.widget.input_type == "file":
                """
                input file type form elements
                """
                html += self.get_fileupload_container_html(element)
                return html
            elif element.widget.input_type == "textarea":
                element_classes["class"] += "texteditor "

        if element_type is not None:
            if element.widget.type == "DateTimeField":
                """
                datetime widget
                """
                element_classes["class"] += "form-control "
                element_classes["class"] += "form-control-sm "
                element_classes["class"] += "datepicker "

        element.render_kw = element_classes

        if element_input_type is not None:
            if element.widget.input_type == "checkbox":
                html += str(element)
                if element_label is not None:
                    html += str(element_label)
                html += "</div>"
                return html

        if element_label is not None:
            html += str(element_label)
        html += str(element)
        html += "</div>"
        return html

    def get_page_element_overview_html(self):
        html = '<a class="btn-dark button button-add-page-element">Seitenelement hinzufügen</a>'
        html += '<h3>Seitenelemente: </h3>'
        html += '<div id="page-elements"></div>'
        html += '<div id="page-element-overview-dialog" class="page-element-overview dialog hidden">'
        for element_eid in PAGE_ELEMENTS:
            html += '<div class="page-element-item" eid="' + element_eid + '">' + element_eid + '</div>'
        html += '</div>'
        return html

    def render(self, form_object=None):
        submit = ""
        html = ""
        if form_object is not None:
            self.init_values(form_object)
        html = '<form id="{0}" method="{1}" action="{2}" enctype="multipart/form-data">'.format(self.form_id,
                                                                                                self.method,
                                                                                                self.action)

        html += '<input type="hidden" id="type" name="type" value="{0}">'.format(self.type)
        html += '<input type="hidden" id="module" name="module" value="{0}">'.format(self.module)
        if self.display_tabs:
            html += "<ul class='nav nav-tabs'>"
            for tab in self.tabs:
                html += "<li class='nav-item'>"
                html += '<a class="nav-link {0}" data-tab-id="{1}">{2}</a>'.format(tab, tab, str(tab).capitalize())
                html += "</li>"
            html += "</ul>"
            for tab in self.tabs:
                html_tab = dict()
                html_tab[tab] = ""
                html_tab[
                    tab] += '<a class="btn-dark button button-display-tab-content" data-tab="' + tab + '"><span class="oi oi-arrow-thick-top"></span>Inhalt ausblenden</a>'
                for field in iter(self):
                    element = field
                    element_id = element.label.field_id
                    if tab == "content" and not self.is_element_seo(element_id) and not self.is_element_control(
                            element_id) and not self.is_element_submit(element_id):
                        html_tab[tab] += self.get_element_html(element)
                    elif tab == "meta" and self.is_element_seo(element_id):
                        html_tab[tab] += self.get_element_html(element)
                    elif tab == "ctrl" and self.is_element_control(element_id):
                        html_tab[tab] += self.get_element_html(element)
                    elif self.is_element_submit(element_id):
                        submit = self.get_element_html(element)

                if tab == "content" and self.module == "pages":
                    html_tab[tab] += self.get_page_element_overview_html()

                html += '<div id="tab-{0}" data-tab-id="{1}" class="tab container-fluid">'.format(tab, tab)
                html += html_tab[tab]
                html += "</div>"
        else:
            for field in iter(self):
                element = field
                html += self.get_element_html(element)
        html += submit
        html += '</form>'
        return html
