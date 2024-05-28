import telebot
from time import sleep
from sqlalchemy.orm import sessionmaker
from flask import Flask, request
from dotenv import load_dotenv
import os
from threading import Thread
from config import Tickets,Users, SentMessage, all_airports, engine, isadmin
load_dotenv()
    
Session = sessionmaker(bind=engine)
app = Flask(__name__)
bot = telebot.TeleBot(os.getenv('token'))
WEBHOOK_URL_PATH = "/webhook"

@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
    bot.process_new_updates([update])
    return '', 200

def set_webhook():
    bot.remove_webhook()
    public_url = os.getenv('webhook_url')
    bot.set_webhook(url=public_url + WEBHOOK_URL_PATH)
    print("Webhook is set:", public_url)

@bot.message_handler(commands=['start'])
def welcome_message(message):
    msg = '''🎉 Welcome to Travel Hacker Bot! 🌟 
Thank you for joining us on this exciting journey.
We're thrilled to have you aboard as we explore the world of travel together. Your next adventure starts here! 🌍✈️ '''
    bot.send_message(message.chat.id, msg)
    sleep(1)
    session = Session()
    user = session.query(Users).filter(Users.ID==message.chat.id).first()
    bot.send_message(message.chat.id, '''First things first, what's your name? We love to keep things personal here! 📛''')


set_webhook()   
app.run(host="0.0.0.0", port=8000)