from flask.ext.testing import LiveServerTestCase
from selenium import webdriver

import unittest
import application

class EndToEndTest(LiveServerTestCase):
    def setUp(self):
        application.init_db()
        self.driver = webdriver.Firefox()

    def tearDown(self):
        self.driver.close()

    def create_app(self):
        app = application.application
        app.config["Testing"] = True
        app.config["LIVESERVER_PORT"] = 8943
        return app

    def test_displays_a_welcome_page(self):
        self.driver.get(self.get_server_url())

        self.assertIn(
                "Todo",
                self.driver.find_element_by_tag_name("body").text)

    def test_adds_and_displays_a_card(self):
        self.driver.get(self.get_server_url())

        todo_text = "This is a todo"

        self.driver.find_element_by_id("id_todo").send_keys(todo_text)
        self.driver.find_element_by_id("id_add").click()

        self.driver.get(self.get_server_url())

        self.assertIn(
                todo_text,
                self.driver.find_element_by_tag_name("body").text)

        self.driver.find_element_by_id("id_delete").click()

        self.assertNotIn(
                todo_text,
                self.driver.find_element_by_tag_name("body").text)
