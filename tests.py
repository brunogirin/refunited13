import unittest
import api

import requests
from requests.auth import HTTPDigestAuth

class TestRaw(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_raw_get(self):
        r = requests.get(
                         'http://api.ru.istykker.dk/profile/320002',
                         headers={
                                  'Content-Type': 'application/json',
                                  'Content-Length': '0'},
                         auth=HTTPDigestAuth(
                                             'hackathon',
                                             api.API_PASSWORD)
                         )
        self.assertEqual(r.status_code, 200, "Unexpected status code")
        
class TestApi(unittest.TestCase):
    def setUp(self):
        self.api = api.ApiServer()

    def test_single_profile(self):
        r = self.api.get('profile/320002')
        self.assertEqual(r.status_code, 200, "Unexpected status code")
        
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

if __name__ == '__main__':
    unittest.main()
    