import unittest
import api


class TestApi(unittest.TestCase):
    def setUp(self):
        self.api = api.ApiServer()

    def test_profiles(self):
        pass

    def test_invalid_uri(self):
        self.assertEqual(404, self.api.get("wrong").status_code)
