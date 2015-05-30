from flask import Flask
from flask.ext.testing import LiveServerTestCase
from selenium import webdriver

import unittest
import flashcards

class EndToEndTest(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()

    def tearDown(self):
        self.driver.close()

    def create_app(self):
        app = flashcards.app
        app.config["Testing"] = True
        app.config["LIVESERVER_PORT"] = 8943
        return app

    def test_displays_a_welcome_page(self):
        self.driver.get(self.get_server_url())

        self.assertIn(
                "Welcome", self.driver.find_element_by_tag_name("body").text)
