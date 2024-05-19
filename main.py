import telebot
from flask import Flask, request
from bot import bot, msg_markup
from thriftytraveler import add_db
from time import sleep
from threading import Thread
from telebot import types
from thriftytraveler import get_data, add_db
from config import Tickets, NewTickets, Users, SentMessage
from sqlalchemy.orm import sessionmaker
from config import engine
import os
from dotenv import load_dotenv
from telebot.apihelper import ApiException

load_dotenv()

app = Flask(__name__)

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

def get_data():
    #TODO: Add all scraping scripts & scraping logic 
    return add_db()


Session = sessionmaker(bind=engine)

def send_message():
    while True:
        if get_data():
            session = Session()
            users = session.query(Users).all()
            for user in users:
                user_airports = user.Airports.split('\n')
                user_id = user.ID
                for airport in user_airports:
                    data = session.query(NewTickets).filter(NewTickets.DepartureAirports.like(f'%{airport}%')).all()
                    for row in data:
                        if session.query(SentMessage).filter_by(user_id=user_id, message_id=f"new_{row.ID}").first():
                            continue
                        msg = f'''<strong>{row.Title}</strong>
{row.Cabin}
-----------------------
{row.Price}
-----------------------
ORDER BY: {row.Type}'''

                        try:
                            base_path = os.getcwd()
                            photo_path = os.path.join(base_path, f'imgs/{row.PictureName}')
                            if row.PictureName:
                                with open(photo_path, 'rb') as photo:
                                    bot.send_photo(user_id, photo=photo)
                            bot.send_message(user_id, msg, parse_mode='HTML', reply_markup=msg_markup(row.ID))
                        except ApiException as e:
                            if e.error_code == 403 and "bot was blocked by the user" in e.result_json["description"]:
                                print(f"User {user_id} blocked the bot.")
                                session.query(Users).filter(Users.ID == user_id).delete()
                                break
                            else:
                                sleep(50)
                        sent_message = SentMessage(user_id=user_id, message_id=f"new_{row.ID}")
                        session.add(sent_message)
                        session.commit()
                        data.remove(row)
            session.close()
        sleep(60)

if __name__ == '__main__':
    set_webhook()
    Thread(target=send_message).start()
    app.run(host="127.0.0.1", port=5000)