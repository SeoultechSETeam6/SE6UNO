from multi_game_client import MultiPlay

game_client = MultiPlay([False, False, True, False, False], 'you', None)
game_client.connect()
while True:
    game_client.send_msg()