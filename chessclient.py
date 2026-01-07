import http.client
import json
from urllib.parse import quote
import http.server

class ChessClient:
    @staticmethod
    def create_user(username, salt, hashed_password):
        conn = http.client.HTTPSConnection("17mlee.eu.pythonanywhere.com")
        data = {"username": username, "salt": salt, "hashed_password": hashed_password}
        headers = {'Content-Type': 'application/json'}
        conn.request("POST", "/users", body=json.dumps(data), headers=headers)
        response = conn.getresponse()
        data = response.read().decode()
        return json.loads(data)
    @staticmethod
    def get_salt(username):
        conn = http.client.HTTPSConnection("17mlee.eu.pythonanywhere.com")
        params = "?username=" + quote(username)
        conn.request("GET", "/users/salt" + params)
        response = conn.getresponse()
        data = response.read().decode()
        return json.loads(data)
    @staticmethod
    def validate_user(username, hashed_password):
        conn = http.client.HTTPSConnection("17mlee.eu.pythonanywhere.com")
        params = "?username=" + quote(username) + "&hashed_password=" + quote(hashed_password)
        conn.request("GET", "/users/validate" + params)
        response = conn.getresponse()
        data = response.read().decode()
        return json.loads(data)
    @staticmethod
    def get_puzzle (userID, rating_min, rating_max):
        conn = http.client.HTTPSConnection("17mlee.eu.pythonanywhere.com")
        params = "?userID=" + str(userID) + "&rating_max=" + str(rating_max) + "&rating_min=" + str(rating_min)
        conn.request("GET", "/puzzles" + params)
        response = conn.getresponse()
        data = response.read().decode()
        return json.loads(data)
    @staticmethod
    def puzzle_completed(userID, puzzleID):
        conn = http.client.HTTPSConnection("17mlee.eu.pythonanywhere.com")
        data = {"userID": userID, "puzzleID": puzzleID}
        headers = {'Content-Type': 'application/json'}
        conn.request("POST", "/puzzles", body=json.dumps(data), headers=headers)
        response = conn.getresponse()
        data = response.read().decode()
    @staticmethod
    def get_games_name(userID,result,playedas,AI):
        conn = http.client.HTTPSConnection("17mlee.eu.pythonanywhere.com")
        params = "?userID=" + str(userID)
        for i in range(len(result)):
            params += "&result=" + result[i]
        for i in range(len(playedas)):
            params += "&playedas=" + playedas[i]
        for i in range(len(AI)):
            params += "&AI=" + str(AI[i])
        conn.request("GET", "/games/names" + params)
        response = conn.getresponse()
        data = response.read().decode()
        return json.loads(data)
    @staticmethod
    def get_game_moves(gameID):
        conn = http.client.HTTPSConnection("17mlee.eu.pythonanywhere.com")
        params = "?gameID=" + str(gameID)
        conn.request("GET", "/games" + params)
        response = conn.getresponse()
        data = response.read().decode()
        return json.loads(data)
    @staticmethod
    def save_game(userID,name, moves,result,playedas,AI):
        conn = http.client.HTTPSConnection("17mlee.eu.pythonanywhere.com")
        data = {"userID": userID, "name": name, "moves": moves, "result": result, "playedas": playedas, "AI": AI}
        headers = {'Content-Type': 'application/json'}
        conn.request("POST", "/games", body=json.dumps(data), headers=headers)
        response = conn.getresponse()
        data = response.read().decode()