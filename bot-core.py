import os

import telebot
from dotenv import load_dotenv
from telebot.types import BotCommand

load_dotenv()
bot = telebot.TeleBot(token=os.getenv('token'))

commands = [
    BotCommand('start', 'start'),
    BotCommand('help', 'Show description of the commands and general info'),
    BotCommand('fix', 'Improve image quality')
]

bot.set_my_commands(commands)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'Hello world')


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, 'Help')


bot.infinity_polling()
