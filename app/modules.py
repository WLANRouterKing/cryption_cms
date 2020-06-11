from app.models import Database


class News(Database):

    def __init__(self):
        super().__init__()
        self.table_name = "news"
        self.class_label = "News-Meldung"
        self.edit_node = "edit_" + self.table_name
        self.delete_node = "delete_" + self.table_name

    def get_eid_custom(self):
        return self.get("eid_custom")

    def get_ctrl_datetime(self):
        return self.get("ctrl_datetime")

    def get_meta_description(self):
        return self.get("meta_description")

    def get_meta_title(self):
        return self.get("meta_title")

    def get_meta_image(self):
        return self.get("meta_image")

    def get_main_image(self):
        return self.get("main_image")

    def get_teaser_image(self):
        return self.get("teaser_image")

    def get_news_images(self):
        return self.get("news_images")

    def set_eid_custom(self, value):
        self.set("eid_custom", value)

    def set_ctrl_datetime(self, value):
        self.set("ctrl_datetime", value)

    def set_meta_description(self, value):
        self.set("meta_description", value)

    def set_meta_title(self, value):
        self.set("meta_title", value)

    def set_meta_image(self, value):
        self.set("meta_image", value)

    def set_main_image(self, value):
        self.set("main_image", value)

    def set_teaser_image(self, value):
        self.set("teaser_image", value)

    def set_news_images(self, value):
        self.set("news_images", value)
