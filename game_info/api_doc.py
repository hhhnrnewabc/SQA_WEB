game_info_update_api = """
List all steam user.
--------------------------------------------------------------------------

POST your app `api_token` and data :

    {
        "api_token": "",

        "name": "BOT1",
        "chess": "\u8c61",
        "action": "Move",
        "eaten": "None",
        "fromx": "1",
        "fromy": "1",
        "tox": "3",
        "toy": "3"
    }

If is correct will return:

    
    {
        "game": 1,
        "name": "BOT1",
        "chess": "\u8c61",
        "action": "Move",
        "eaten": "None",
        "fromx": "1",
        "fromy": "1",
        "tox": "3",
        "toy": "3"
    }


"""
