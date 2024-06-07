import os
import json
from time import sleep
from threading import Thread
from flask import Flask, request
import telebot
from telebot import types
from telebot.apihelper import ApiException
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from bot import msg_markup, check_subscription, bot
from thriftytraveler import get_data, add_db
from models import Tickets, NewTickets, Users, SentMessage, Session
from config import engine
from delete_offrers import autodelete
from pomelo import add_pomelo
load_dotenv()


app = Flask(__name__)
WEBHOOK_URL_PATH = "/webhook"
#TODO: SEGMENTATIONS 


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
    value = add_db()
    if not value:
        value = add_pomelo()
        if not value:
            autodelete()
    return value

def send_message():
    while True:
        if get_data():
            with Session() as session:
                users = session.query(Users).all()
                for user in users:
                    user_airports = user.Airports.split('\n')
                    user_id = user.ID
                    if not check_subscription(user.ID):
                        continue
                    for airport in user_airports:
                        airport = f"({airport.split('(')[-1]}"
                        data = session.query(NewTickets).filter(NewTickets.DepartureAirports.like(f'%{airport}%')).all()
                        for row in data:
                            if session.query(SentMessage).filter_by(user_id=user_id, message_id=f"new_{row.ID}").first():
                                continue
                            msg = f'''✈️<b>{row.Title}</b>✈️
    {row.Cabin}
    -----------------------
    {row.Price} (was {row.OriginalPrice})
    -----------------------
    {row.Dates}
    -----------------------
    ORDER BY: {row.Type}'''
                            try:
                                base_path = os.getcwd()
                                photo_path = os.path.join(base_path, f'imgs/{row.PictureName}')
                                if row.PictureName:
                                    with open(photo_path, 'rb') as photo:
                                        bot.send_photo(user_id, photo=photo)
                                bot.send_message(user_id, msg, parse_mode='HTML', reply_markup=msg_markup(row.ID))
                                sleep(1)
                            except ApiException as e:
                                if e.error_code == 403 and "bot was blocked by the user" in e.result_json["description"]:
                                    print(f"User {user_id} blocked the bot.")
                                    user = session.query(Users).filter(Users.ID == user_id).first()
                                    user.ActiveUser = False
                                    break
                                else:
                                    sleep(50)
                            sent_message = SentMessage(user_id=user_id, message_id=f"new_{row.ID}")
                            session.add(sent_message)
                            session.commit()
                            data.remove(row)
            sleep(60)


def handle_channel_message(message):
    with Session() as session:
        users = session.query(Users).all()
        for user in users:
            try:
                if message.content_type == 'text':
                    bot.send_message(user.ID, message.text)
                elif message.content_type == 'photo':
                    photo_id = message.photo[-1].file_id
                    bot.send_photo(user.ID, photo_id, caption=message.caption)
                elif message.content_type == 'video':
                    video_id = message.video.file_id
                    bot.send_video(user.ID, video_id, caption=message.caption)
                elif message.content_type == 'document':
                    document_id = message.document.file_id
                    bot.send_document(user.ID, document_id, caption=message.caption)
                elif message.content_type == 'audio':
                    audio_id = message.audio.file_id
                    bot.send_audio(user.ID, audio_id, caption=message.caption)
                elif message.content_type == 'voice':
                    voice_id = message.voice.file_id
                    bot.send_voice(user.ID, voice_id, caption=message.caption)
                elif message.content_type == 'sticker':
                    sticker_id = message.sticker.file_id
                    bot.send_sticker(user.ID, sticker_id)
                elif message.content_type == 'animation':
                    animation_id = message.animation.file_id
                    bot.send_animation(user.ID, animation_id, caption=message.caption)
                elif message.content_type == 'video_note':
                    video_note_id = message.video_note.file_id
                    bot.send_video_note(user.ID, video_note_id)
                else:
                    print(f"Unsupported message type: {message.content_type}")
            except ApiException as e:
                if e.error_code == 403 and "bot was blocked by the user" in e.result_json["description"]:
                    print(f"User {user.ID} blocked the bot.")
                    user_db = session.query(Users).filter(Users.ID == user.ID).first()
                    user_db.ActiveUser = False
                    session.commit()
                else:
                    print(f"Error sending message to user {user.ID}: {e}")
                    sleep(50)


@bot.channel_post_handler(content_types=['text', 'photo', 'audio', 'voice', 'sticker', 'animation', 'video_note', 'document'])
def monitor_channel_posts(message):
    if str(message.chat.id) == os.getenv('channel_updates_id'):
        return
    handle_channel_message(message)


if __name__ == '__main__':
    set_webhook() 
    Thread(target=send_message).start()  
    app.run(host="0.0.0.0", port=8000)
