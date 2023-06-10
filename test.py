import unittest
import warnings
from api import app
from base64 import b64encode



class MyAppTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.app = app.test_client()

        warnings.simplefilter("ignore", category=DeprecationWarning)

    def test_index_page(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "<p>Hello, World!</p>")

    def test_getstudents(self):
        response = self.app.get("/students")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Wyatty" in response.data.decode())

    def test_getstudents_by_id(self):
        response = self.app.get("/students/1")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Maico" in response.data.decode())


if __name__ == "__main__":
    unittest.main()