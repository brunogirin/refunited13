import api as a
import json

class Users:
    def __init__(self, first_name, last_name, password="hackd3y"):
        api = a.ApiServer()
        j = json.loads(api.get("usernamegenerator", {"givenName":first_name, "surName":last_name}).text)
        self.first_name, self.last_name = first_name, last_name
        j['givenName'] = first_name
        j['surName'] = last_name
        j['password'] = "h3ckday"
        self.password = "h3ckday"
        result = json.loads(api.post("profile", params=j).text)
        self.id = result["profile"]["id"]