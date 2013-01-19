import unittest
import api


class TestApi(unittest.TestCase):
    def setUp(self):
        self.api = api.ApiServer()

    def test_profiles(self):
        pass

    def test_invalid_uri(self):
        self.assertEqual(404, self.api.get("wrong").status_code)

    def test_view_messages(self):
        pass

    def test_send_message(self):
        pass

    def test_search(self):
        self.assertNotRegexpMatches(self.api.get("search", {"name":"james"}).text, "HTTP Digest")


class TestSpam(unittest.TestCase):
    def setUp(self):
        pass

    def test_something(self):
        pass
