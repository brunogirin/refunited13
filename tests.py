import unittest
import api
import json
import spam
import messages

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

    def test_generate_username(self):
        result = self.api.get("usernamegenerator", {"givenName":"Hack", "surName":"Day"})
        self.assertEqual(200, result.status_code)
        self.assertRegexpMatches(result.text, "hack")

    def test_create_profile(self):
        generatedUserName = self.api.get("usernamegenerator", {"givenName":"Hack", "surName":"Day"}).text
        j = json.loads(generatedUserName)
        j['givenName'] = "Hack"
        j['surName'] = "Day"
        j['password'] = "h3ckday"
        result = self.api.post("profile", params=j)
        self.assertRegexpMatches(result.text, "profile")
        self.assertEqual(result.status_code, 200)

class TestMessaging(unittest.TestCase):
    def setUp(self):
        self.api  = api.ApiServer()
        self.handler = messages.MessageHandler()

        def createUser(first_name, last_name):
            j = json.loads(self.api.get("usernamegenerator", {"givenName":first_name, "surName":last_name}).text)
            j['givenName'] = first_name
            j['surName'] = last_name
            j['password'] = "h3ckday"
            result = json.loads(self.api.post("profile", params=j).text)
            return result["profile"]["id"]

        self.one = createUser("Hacker", "Daily")
        self.two = createUser("Hacking", "Often")

    def test_users_created(self):
        self.assertGreater(self.one, 0)
        self.assertGreater(self.two, 0)

    def test_sending_message(self):
        messages = self.handler.read_messages(self.two)
        self.handler.send_message(self.one, self.two, "Hello World")
        new_messages = self.handler.read_messages(self.two)
        self.handler.send_message(self.two, self.one, "Hi Computer")
        self.assertEqual(len(messages["threads"]), 0)
        self.assertEqual(len(new_messages["threads"]), 1)
        self.assertEqual(len(self.handler.read_messages(self.one)["threads"]),1)

class TestSpam(unittest.TestCase):
    def setUp(self):
        pass

    def test_tokenize_message_body(self):
        tok = spam.MessageTokenizer()
        c = spam.Corpus()
        tok.tokenize_message_body(c, "This is a simple message")
        self.assertIn('simple', c.data, "Expected the word simple in the map: {0}".format(c.data))
        self.assertEqual(c.data['simple'], 1, "Unexpected value for simple")

    def test_tokenize_message(self):
        tok = spam.MessageTokenizer()
        msg = {
               'from': '320002',
               'to': '320202',
               'body': "This is a simple message"
               }
        c = tok.tokenize_message(msg)
        self.assertIn('simple', c.data, "Expected the word simple in the map: {0}".format(c.data))
        self.assertEqual(c.data['simple'], 1, "Unexpected value for simple")
        self.assertIn('from*320002', c.data, "Expected from header in map: {0}".format(c.data))
        self.assertEqual(c.data['from*320002'], 1, "Unexpected value for from*320002")

    def test_score_message(self):
        processor = spam.SpamProcessor()
        processor.flag_as_bad("My name is Bruno and I am a lawyer with lots of money to give you")
        processor.flag_as_good("Hello there, my name is James and I am looking for Scot")
        s = processor.score("Do I need to see James?")
        self.assertEqual(s[1], 'Neutral', "Unexpected score for message: {0}".format(s))
        
if __name__ == '__main__':
    unittest.main()
    