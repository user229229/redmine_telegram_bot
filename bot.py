#!/usr/bin/python

# This is a simple echo bot using the decorator mechanism.
# It echoes any incoming text messages.

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
    IssueID = RedmineNewIssue(message.forward_from.username, message.text, message.text)
    if IssueID != 0:
        IssueURL =  RedmineURL + '/issues/'+ str(IssueID)
        bot.reply_to(message, IssueURL)
    else:
        bot.reply_to(message, "-")


bot.infinity_polling()
