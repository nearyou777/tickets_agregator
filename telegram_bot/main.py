
from flask import Flask, request
import telebot
from telebot.apihelper import ApiException
from time import sleep
import os
from typing import TYPE_CHECKING
from threading import Thread
import json
from bot import msg_markup, bot
from shared.config import check_subscription
from shared.models import Users, SentMessage, Session
import logging
from flask.logging import default_handler
from sqlalchemy import select
from buttons import create_deal_msg
from shared.rabit_config import get_connection, RMQ_ROUTING_KEY
if TYPE_CHECKING:
    from pika.adapters.blocking_connection import BlockingChannel
    from pika.spec import BasicProperties, Basic

app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
app.logger.removeHandler(default_handler)
WEBHOOK_URL_PATH = "/webhook"


@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
    bot.process_new_updates([update])
    return '', 200

def set_webhook():
    bot.remove_webhook()
    public_url = os.getenv('WEBHOOK_URL')
    bot.set_webhook(url=public_url + WEBHOOK_URL_PATH)
    print("Webhook is set:", public_url)




def send_message(row:dict):
    with Session() as session:
        users = session.query(Users).all()
        for user in users:
            user_airports = user.Airports.split('\n')
            user_id = user.ID
            if not check_subscription(user_id):
                continue
            # sent_airports = []
            # sent_msg_ids_query = select(SentMessage.message_id).where(SentMessage.user_id == user_id)
            # sent_msg_ids = session.execute(sent_msg_ids_query).scalars().all()
            session.commit()
            for airport in user_airports:
                airport = f"({airport.split('(')[-1]}"
                # sent_msg_ids = select(SentMessage.message_id).where(SentMessage.user_id == user_id)
                # new_tickets = session.query(NewTickets).filter(
                #     ~NewTickets.ID.in_(sent_msg_ids),
                #     NewTickets.DepartureAirports.like(f'%{airport}%')
                # ).all()
            
                # Query to select message_id
                sent_msg_ids_query = select(SentMessage.message_id).where(SentMessage.user_id == user_id)

                # Execute the query and retrieve the message IDs
                sent_msg_ids = session.execute(sent_msg_ids_query).scalars().all()

                # Convert the list of message IDs to a set for faster lookups
                sent_msg_ids_set = set(sent_msg_ids)

                session.commit()

                # Your other logic here...
                # Check if row['ID'] is in sent_msg_ids_set instead of sent_msg_ids
                if row['ID'] in sent_msg_ids_set:
                    continue
                msg = create_deal_msg(row)
                try:
                    base_path = os.getcwd()
                    photo_path = os.path.join(base_path, f'imgs/{row["PictureName"]}')
                    if row['PictureName']:
                        try:
                            with open(photo_path, 'rb') as photo:
                                    bot.send_photo(user_id, photo=photo)
                        except:
                            pass
                    try:
                        bot.send_message(user_id, msg, parse_mode='HTML', reply_markup=msg_markup(row['ID']))
                        sleep(1)
                    except:
                        pass
                except ApiException as e:
                    if e.error_code == 403 and "bot was blocked by the user" in e.result_json["description"]:
                        print(f"User {user_id} blocked the bot.")
                        user = session.query(Users).filter(Users.ID == user_id).first()
                        session.commit()
                        user.ActiveUser = False
                        break
                    else:
                        sleep(50)
                # sent_airports.append(row['ID'])
                # bot.send_message(user_id, str(sent_airports))
                sent_message = SentMessage(user_id=user_id, message_id=row['ID'])
                session.add(sent_message)
                session.commit()



def handle_channel_message(message):
    with Session() as session:
        users = session.query(Users).all()
        session.commit()
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


def process_new_message(ch:"BlockingChannel",
                         method:"Basic.Deliver",
                           properties:"BasicProperties",
                             body:bytes, ):
    
    
    msg = json.loads(body.decode('utf-8'))
    if not msg['Type'] == 'technical message':
        send_message(msg)
    ch.basic_ack(delivery_tag=method.delivery_tag)


def consume_message(ch:"BlockingChannel", routing_key:str):
    ch.basic_consume(
        queue=routing_key,
        on_message_callback=process_new_message,
    )
    ch.start_consuming()

def run_consumer():
    with get_connection() as connection:
        with connection.channel() as channel:
            consume_message(channel, RMQ_ROUTING_KEY)

    
@bot.channel_post_handler(content_types=['text', 'photo', 'audio', 'voice', 'sticker', 'animation', 'video_note', 'document'])
def monitor_channel_posts(message):
    if str(message.chat.id) == os.getenv('CHANNEL_UPDATES_ID'):
        return
    handle_channel_message(message)

def main():
    set_webhook() 
    # sleep(55)
    # Thread(target=run_consumer).start()  
    app.run(host="0.0.0.0", port=8000)


if __name__ == '__main__':
    main()