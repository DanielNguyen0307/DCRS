import telebot

Token = '940492551:AAGc5DkHX3wmlAVrgFda1GA2VDFilpn8uHs'
Bot = telebot.TeleBot(Token)
Bot.config['api_key'] = Token
group_id = -384701139
Bot.send_message(group_id, 'Hello anh Tin')

