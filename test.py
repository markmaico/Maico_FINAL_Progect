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
	hdr = {
            "Authorization": "Basic " + b64encode(b"username:psswrd").decode()
        }
        response = self.app.get("/", headers = hdr)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "<p>Hello, World!</p>")

    def test_getstudents(self):
	hdr = {
            "Authorization": "Basic " + b64encode(b"username:psswrd").decode()
        }
        response = self.app.get("/students", headers = hdr)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Wyatty" in response.data.decode())

    def test_getstudents_by_id(self):
	hdr = {
            "Authorization": "Basic " + b64encode(b"username:psswrd").decode()
        }
        response = self.app.get("/students/1", headers = hdr)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Maico" in response.data.decode())


if __name__ == "__main__":
    unittest.main()