import unittest
import api
import json
import spam
import messages
import load_data
import stats

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
        tokens = [t for t in tok.tokenize_message_body("This is a simple message")]
        self.assertIn('simple', tokens, "Expected the word simple in the list: {0}".format(tokens))

    def test_tokenize_message(self):
        tok = spam.MessageTokenizer()
        msg = {
               'from': '320002',
               'to': '320202',
               'body': "This is a simple message"
               }
        tokens = [t for t in tok.tokenize_message(msg)]
        self.assertIn('simple', tokens, "Expected the word simple in the list: {0}".format(tokens))
        self.assertIn('from*320002', tokens, "Expected from header in list: {0}".format(tokens))

    def test_generate_token_set(self):
        tok = spam.MessageTokenizer()
        msg = {
               'from': '320002',
               'to': '320202',
               'body': "This is a simple message"
               }
        tokens = tok.generate_token_set(msg)
        self.assertIn('simple', tokens, "Expected the word simple in the list: {0}".format(tokens))
        self.assertIn('from*320002', tokens, "Expected from header in list: {0}".format(tokens))

    def test_score_message(self):
        processor = spam.SpamProcessor()
        processor.flag_as_bad("My name is Bruno and I am a lawyer with lots of money to give you")
        processor.flag_as_good("Hello there, my name is James and I am looking for Scot")
        s = processor.score("Do I need to see James?")
        self.assertEqual(s[1], 'Neutral', "Unexpected score for message: {0}".format(s))

    def test_score_message_no_data(self):
        processor = spam.SpamProcessor()
        s = processor.score("Do I need to see James?")
        self.assertEqual(s[1], 'Neutral', "Unexpected score for message: {0}".format(s))
        
    def test_message_collection_no_options(self):
        self.run_message_collection_stats(
                                          [0.02, 0.01, 0.26, 0],
                                          0.05,
                                          []
                                          )
    
    def test_message_collection_pairs(self):
        self.run_message_collection_stats(
                                          [0.02, 0.01, 0.17, 0],
                                          0.05,
                                          ['pairs']
                                          )
    
    def run_message_collection_stats(self, expected_mm_ratios, sample_ratio, tok_options):
        stats_gen = stats.StatsGenerator()
        stats_results = stats_gen.process_message_collection(sample_ratio, tok_options)
        actual_mm_ratios = [
                          stats_results['false_positives'][1],
                          stats_results['false_negatives'][1],
                          stats_results['neutrals'][1],
                          stats_results['unexpected_mismatches'][0]
                          ]
        success = reduce(lambda a, b: a and b, [act <= exp for (act, exp) in zip(actual_mm_ratios, expected_mm_ratios)])
        if success == False:
            self.fail(
                      "Unexpected mismatch sizes: expected = {0}; actual = {1}".
                      format(
                             expected_mm_ratios,
                             actual_mm_ratios
                             ))
            

class TestData(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_load_data(self):
        data = load_data.Data()
        self.assertEqual(0, len(data.neutral_msg), "Expected no neutral messages: {0}".format(data.neutral_msg))
    
    def test_get_next(self):
        data = load_data.Data()
        msg = data.getNext()
        self.assertIsNotNone(msg, "First message should not be None")
    
    def test_get_next_result(self):
        data = load_data.Data()
        msg = data.getNext()
        self.assertIsInstance(msg, basestring, "Message should be a string")
            
if __name__ == '__main__':
    unittest.main()
    