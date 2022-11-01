#!/usr/bin/python

# This is a simple echo bot using the decorator mechanism.
# It echoes any incoming text messages.

# pip install pyTelegramBotAPI
# pip install python-redmine

from warnings import catch_warnings
import telebot
import os
from addissue import *


API_TOKEN = os.environ['TELEGRAM_TOKEN'] 
RedmineURL = os.environ['REDMINE_URL']

bot = telebot.TeleBot(API_TOKEN)


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Hi there, I am Syspod Service Desk Bot.
I am here to register forwarded messages as new issues. \
""")


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    if message.forward_from:
        if message.forward_from.username:
            IssueID = RedmineNewIssue(message.forward_from.username, message.text[:150], message.text)
            if IssueID != 0:
                IssueURL =  RedmineURL + '/issues/'+ str(IssueID)
                bot.reply_to(message, IssueURL)
                try:
                    bot.send_message(message.forward_from.id, "Создана новая задача \n" + IssueURL + "\n" + message.text)
                except:
                    print('Error sending task link to sender')
            else:
                bot.reply_to(message, "Задача не создана")
        else:
            bot.reply_to(message, "У отправителя сообщения не заполнен username в профиле Telegram")
    else:
        bot.reply_to(message, "Необходимо переслать сообщение от другого пользователя")            


bot.infinity_polling()
