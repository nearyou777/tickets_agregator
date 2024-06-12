import telebot
from time import sleep
from telebot import types
import math
from dotenv import load_dotenv
import os
import json
from models import Users, Tickets, SentMessage, Session
from datetime import datetime, timedelta
from telebot.apihelper import ApiException
from export_data import export_tables
from config import check_subscription, isadmin, escape_markdown, format_entities, all_airports
from buttons import msg_markup, channel_mark, airport_buttons, current_pos
load_dotenv()
import logging

# Определение логгера
logger = logging.getLogger(__name__)
#TODO:PROMOCODES
#TODO:EMAIL VALIDATION
#TODO: short user_airport list
bot = telebot.TeleBot(os.getenv('token'))
airports = []



def check_channel_subscription(message):
    try:
        member = bot.get_chat_member(chat_id=os.getenv('channel_updates_id'), user_id=int(message.chat.id))
        if member.status in ['member', 'administrator', 'creator', 'owner']:
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False


def unkown_user(message):
    bot.send_message(message.chat.id, 'You\'re not registred. 📛')
    sleep(1)
    welcome_message(message)

@bot.message_handler(commands=['profile'])
def get_user_info(message):
    with Session() as session:
        user = session.query(Users).filter_by(ID = message.chat.id).first()
        if user:
            user_airports = user.Airports.strip()
            if len(user.Airports.split('\n')) == len(all_airports):
                user_airports = 'All available ✈️'
            elif len(user.Airports) == 0:
                user_airports = 'You didn\'t choose any airport. 🛫' 
            bot.send_message(message.chat.id, f'👤 <b>Your name: </b>{user.Name}\n\n<b>Your contact email:</b> {user.Email}\n\n<b>📅 Subscription end date: </b>{user.SubscriptionDate.date()}\n\n<b>✈️ Your airports: </b>\n{user_airports}', parse_mode='HTML')
            sleep(1)
            try:
                session.commit()
            except Exception as e:
                logger.error(f"Error occurred: {e}")

        else:
            unkown_user(message)
            return
    

@bot.message_handler(commands=['add_airports'])
def add_airports(message):
    bot.send_message(message.chat.id, text='Choose airport to add ✈️', reply_markup=airport_buttons('add', all_airports))
    sleep(1)


@bot.message_handler(commands=['remove_airports'])
def remove_airports(message):
    with Session() as session:
        user = session.query(Users).filter_by(ID = message.chat.id).first()
        if user:
            user_airports = user.Airports.strip()
            if len(user_airports) == 0:
                user_airports = []
            else:
                user_airports = user_airports.split('\n')
        else:
            user_airports = []
            session.close()
            unkown_user(message)
            return
        
        if len(user_airports) == 0: 
            bot.send_message(message.chat.id, text='🌍 Your airports list is empty. Please add airports to continue. 🛫') 
        else:
            user_airports = user.Airports.strip().split('\n')
            bot.send_message(message.chat.id, text='🛬 Choose airport to remove:', reply_markup=airport_buttons('remove', user_airports))   
        sleep(1) 
        try:
            session.commit()
        except Exception as e:
            logger.error(f"Error occurred: {e}")



@bot.message_handler(commands=['start'])
def welcome_message(message):
    msg = '''🎉 Welcome to Travel Hacker Bot! 🌟 
Thank you for joining us on this exciting journey.
We're thrilled to have you aboard as we explore the world of travel together. Your next adventure starts here! 🌍✈️ '''
    with Session() as session:
        user = session.query(Users).filter_by(ID = message.chat.id).first()
        if not user:
            bot.send_message(message.chat.id, msg)
            sleep(1)
        bot.send_message(message.chat.id, '''First things first, what's your name? We love to keep things personal here! 📛''')
        try:
            session.commit()
        except Exception as e:
            logger.error(f"Error occurred: {e}")
        bot.register_next_step_handler(message, get_mail)


def get_mail(message):
    name = message.text.strip()
    if '/' in name:
        unkown_user(message)
        return
    msg = f'''Great to meet you, {name}! 🌟 
Now, could you please share your email address with us?
We'll use this to keep you updated with the latest flight deals and connect you to our exclusive course on Skool.com. 📧'''
    bot.send_message(message.chat.id, msg)
    sleep(0.5)
    bot.register_next_step_handler(message, channel_subscribe, name)

def channel_subscribe(message, name):#saving data here
    # print(f'\n\n\n\n\n USER HERE')
    user_id = message.chat.id
    mail = message.text.strip()
    with Session() as session:
        flag = False
        if not session.query(Users).filter_by(ID = user_id).first():  
            session.add(Users(ID=user_id, Name=name,Email=mail, Airports='')) 
            session.commit()
        else:
            user_to_upd = session.query(Users).filter_by(ID = user_id).first()
            user_to_upd.ID = user_id
            user_to_upd.Name = name 
            user_to_upd.Email = mail
            user_to_upd.Airports = ''
            session.commit()
            flag = True
        member = check_channel_subscription(message)

        msg = '''Awesome!😊
    Now, let’s make sure you’re in our exclusive channel
    This step is crucial to continue! 📢''' 
        if not member:
            bot.send_message(message.chat.id, msg, reply_markup=channel_mark())
            while not member:
                member = check_channel_subscription(message)
        else:
            get_airports(message, flag)
        try:
            session.commit()
        except Exception as e:
            logger.error(f"Error occurred: {e}")

def get_airports(message, flag:bool):
    msg = f'''Thank you for subscribing!✅ 🎉 You’re awesome! 
Now, let’s customize your flight alerts. 🛫'''
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Add airports 🛫') 
    btn2 = types.KeyboardButton('Remove airports 🛬')
    btn3 = types.KeyboardButton('My profile 👤')
    markup.row(btn1,btn2,btn3)
    if not flag:
        bot.send_message(message.chat.id, msg, reply_markup=markup)
        sleep(1)
    else:
        msg = f'''Thanks for still subscribing our group!✅ 🎉 You’re awesome! 
Now, let’s customize your flight alerts. 🛫'''
        bot.send_message(message.chat.id, msg, reply_markup=markup)
    add_airports(message)


@bot.message_handler(commands=['renew'])
def get_user_id(message):
    try:
        user_id = int(message.text.replace('/renew', '').strip())
    except:
        bot.send_message(message.chat.id, 'Wrong user id')
    if isadmin(message.chat.id):
        bot.send_message(message.chat.id, '🔄 Enter a number of days for which you want to renew your subscription 🔄')
        bot.register_next_step_handler(message, renew_subs, user_id)
    else:
        bot.send_message(message.chat.id, 'You\'re not allowed to use that command ❌')


def renew_subs(message, user_id):
    days = int(message.text.strip())
    with Session() as session:
        user = session.query(Users).filter_by(ID = user_id).first()
        if user:
            user.SubscriptionDate = (user.SubscriptionDate + timedelta(days=days)).date()
            session.commit()
            bot.send_message(message.chat.id, f'✅ Successfully renewed subscription for {user.Name}! User can continue using the bot. 🚀')
        else:
            bot.send_message(message.chat.id, '❌ Incorrect user ID. Please use the command again.')
        try:
            session.commit()
        except Exception as e:
            logger.error(f"Error occurred: {e}")

@bot.message_handler(commands=['post'])
def get_post_msg(message):
    if isadmin(message.chat.id):
        with Session() as session:
            user = session.query(Users).filter_by(ID = message.chat.id).first()
            ids_to_share = message.text.replace('/post', '').strip()
            if len(ids_to_share) == 0:
                ids_to_share = None
            if user:
                bot.send_message(message.chat.id, f'Hi {user.Name}. Enter a post below that you would like to share')
                bot.register_next_step_handler(message, share_post, ids_to_share)
        try:
            session.commit()
        except Exception as e:
            logger.error(f"Error occurred: {e}")
    else:
        bot.send_message(message.chat.id, 'You\'re now allowed to use this command ❌')

def share_post(message, ids_text):
    with Session() as session:
        share_ids = []
        if ids_text:
            for id in ids_text.split(','):
                try:
                    share_ids.append(int(id))
                except ValueError:
                    continue
        if len(share_ids) == 0:
            share_ids = [user.ID for user in session.query(Users).all()]
        if message.content_type == 'text':
            if message.entities:
                formatted_message = format_entities(message.text, message.entities)
            else:
                formatted_message = escape_markdown(message.text)
        else:
            formatted_message = None
        caption = message.caption
        if caption and message.caption_entities:
            formatted_caption = format_entities(caption, message.caption_entities)
        else:
            formatted_caption = escape_markdown(caption) if caption else None

        for user_id in share_ids:
            try:
                if message.content_type == 'text':
                    bot.send_message(user_id, formatted_message.strip(), parse_mode="MarkdownV2")
                elif message.content_type == 'photo':
                    photo_id = message.photo[-1].file_id
                    bot.send_photo(user_id, photo_id, caption=formatted_caption, parse_mode="MarkdownV2")
                elif message.content_type == 'video':
                    video_id = message.video.file_id
                    bot.send_video(user_id, video_id, caption=formatted_caption, parse_mode="MarkdownV2")
                elif message.content_type == 'document':
                    document_id = message.document.file_id
                    bot.send_document(user_id, document_id, caption=formatted_caption, parse_mode="MarkdownV2")
                elif message.content_type == 'audio':
                    audio_id = message.audio.file_id
                    bot.send_audio(user_id, audio_id, caption=formatted_caption, parse_mode="MarkdownV2")
                elif message.content_type == 'voice':
                    voice_id = message.voice.file_id
                    bot.send_voice(user_id, voice_id, caption=formatted_caption, parse_mode="MarkdownV2")
                elif message.content_type == 'sticker':
                    sticker_id = message.sticker.file_id
                    bot.send_sticker(user_id, sticker_id)
                elif message.content_type == 'animation':
                    animation_id = message.animation.file_id
                    bot.send_animation(user_id, animation_id, caption=formatted_caption, parse_mode="MarkdownV2")
                elif message.content_type == 'video_note':
                    video_note_id = message.video_note.file_id
                    bot.send_video_note(user_id, video_note_id)
                elif message.content_type == 'location':
                    bot.send_location(user_id, message.location.latitude, message.location.longitude)
                elif message.content_type == 'contact':
                    bot.send_contact(user_id, message.contact.phone_number, message.contact.first_name, message.contact.last_name)
                elif message.content_type == 'poll':
                    bot.send_poll(user_id, question=message.poll.question, options=[option.text for option in message.poll.options], is_anonymous=message.poll.is_anonymous, type=message.poll.type, allows_multiple_answers=message.poll.allows_multiple_answers)
                else:
                    print(f"Unsupported message type: {message.content_type}")
            except ApiException as e:
                if e.error_code == 403 and "bot was blocked by the user" in e.result_json["description"]:
                    user_db = session.query(Users).filter(Users.ID == user_id).first()
                    if user_db:
                        user_db.ActiveUser = False
                        session.commit()
                else:
                    sleep(1)
        try:
            session.commit()
        except Exception as e:
            logger.error(f"Error occurred: {e}")

@bot.message_handler(commands=['search'])
def search_message(message):    
    with Session() as session:
        user = session.query(Users).filter_by(ID = message.chat.id).first()
        session.commit()
        if user:
            if not check_subscription(message.chat.id):
                bot.send_message(message.chat.id, '⚠️ Your subscription has expired. Please contact the admin to renew it or purchase a subscription directly in the bot. 🛒')
                return
            if not check_channel_subscription(message):
                bot.send_message(message.chat.id, f'Hi, {user.Name}, you\'re not subscribed to our newsletter channel.\nYou can do it immediately using link bellow', reply_markup=channel_mark())
                return 
            bot.send_message(message.chat.id, 'Working on your query...')
            found = False
            user_airports = user.Airports.split('\n')
            for airport in user_airports:
                    airport = f"({airport.split('(')[-1]}"
                    data = session.query(Tickets, SentMessage).outerjoin(
                        SentMessage, (Tickets.ID == SentMessage.message_id) & (SentMessage.user_id == message.chat.id)
                    ).filter(
                        Tickets.DepartureAirports.like(f'%{airport}%')
                    ).all()
                    session.commit()
                    # counter = 0
                    # if len(data) > 0:
                    #     counter += 1 
                    user_id = message.chat.id
                    for row, old_msg in data:
                        msg = f'''✈️<b>{row.Title}</b>✈️
-----------------------
{row.Cabin}
-----------------------
{row.Price} (was {row.OriginalPrice})
-----------------------
{row.Dates}
-----------------------
ORDER BY: {row.Type}'''
                        if old_msg:
                            continue
                        markup = msg_markup(row.ID, 'start')
                        base_path = os.getcwd()
                        photo_path = os.path.join(base_path, f'imgs/{row.PictureName}')
                        with open(photo_path, 'rb') as photo:
                            try:
                                bot.send_photo(user_id, photo=photo)
                            except:
                                pass
                        try:
                            bot.send_message(user_id, msg, parse_mode='HTML', reply_markup=markup)
                        except:
                            pass
                        found = True
                        # bot.send_message(user_id, msg, parse_mode='Markdown')
                        sleep(1)
                        sent_message = SentMessage(user_id=user_id, message_id=row.ID)
                        session.add(sent_message)
                        session.commit()
            if not found:
                bot.send_message(message.chat.id, '😞 Sorry. Currently no tickets found for any of your saved airports. Please try again later or update your airport preferences. ⚠️')
        else:
            unkown_user(message)


@bot.message_handler(commands=['export'])
def get_csv(message):
    if isadmin(message.chat.id):
        export_tables()
        for table_name in ['Tickets', 'NewTickets', 'Users']:
            try:
                with open(f'out/{table_name}.csv', 'rb') as f:
                    bot.send_document(message.chat.id, document=f)
            except:
                continue
    else:
        bot.send_message(message.chat.id, 'You\'re not allowed to use that command ❌')


@bot.message_handler(content_types=['text'])
def on_click(message:types.Message):

    if 'Add airports' in message.text:
        add_airports(message)
    elif 'Remove airports' in message.text:
        remove_airports(message)
    elif 'My profile' in message.text:
        get_user_info(message)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    with Session() as session:
        user = session.query(Users).filter_by(ID = call.message.chat.id).first()
        if user:
            airports = user.Airports.strip()
            if len(airports) == 0:
                airports = []
            else:
                airports = airports.split('\n')
        else:
            airports = []
        try:
            session.commit()
        except Exception as e:
            logger.error(f"Error occurred: {e}")

    if 'add' in call.data and '_scrollbtn' not in call.data :
        with Session() as session:
            user = session.query(Users).filter_by(ID = call.message.chat.id).first()
            if not user:
                unkown_user(call.message)
            else:
                if call.data == 'add_all':
                    user.Airports = "\n".join(all_airports)
                    session.commit()
                    bot.answer_callback_query(call.id, 'Fetching...')
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='You\'ve choosed all airports', parse_mode='HTML')
                else:
                    for airport in all_airports:
                        if f'add_{airport}' in call.data:
                            user = session.query(Users).filter_by(ID = call.message.chat.id).first()
                            if airport in user.Airports:
                                bot.answer_callback_query(call.id, f'Airport {airport} is already in your favourites list')
                            else:
                                bot.answer_callback_query(call.id, f'Airport {airport} is added to your favourites')
                                airports.append(airport)
                        user.Airports = "\n".join(airports)
                        session.commit()
            try:
                session.commit()
            except Exception as e:
                logger.error(f"Error occurred: {e}")

    elif 'remove' in call.data and '_scrollbtn' not in call.data:
        with Session() as session:
            user = session.query(Users).filter_by(ID = call.message.chat.id).first()
            if user:
                airports = user.Airports.strip()
                if len(airports) == 0:
                    airports = []
                else:
                    airports = airports.split('\n')
                if call.data == 'remove_all':
                    user = session.query(Users).filter_by(ID = call.message.chat.id).first()
                    user.Airports = ""
                    session.commit()
                    session.close()
                    bot.answer_callback_query(call.id, f'All airports is removed from your favourites')
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Your airports list is now empty. 🚫 No airports selected. 🛫', parse_mode='HTML')
                else:
                    for airport in airports:
                        if  f'remove_{airport}' in call.data:
                            if airport in airports:
                                current_page = int(call.data.split('_')[-1]) 

                                current_pos  = (current_page - 1) * 20
                                print(str(len(airports) / 20).split('.')[1][0])
                                print(str(len(airports) / 20))
                                if str(len(airports) / 20).split('.')[1][0] == '0':
                                    current_pos -= 20
                                    current_page -= 1
                                airports.remove(airport)
                                bot.answer_callback_query(call.id, f'Airport {airport} is removed from your favourites')
                                
                                if len(airports) < 1:
                                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Your airports list is now empty. 🚫 No airports selected. 🛫', parse_mode='HTML')
                                    add_airports(call.message)
                                else:
                                    markup = airport_buttons('remove', airports, current_position=current_pos, page=current_page)
                                    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=markup)
                                user.Airports = "\n".join(airports)
                                session.commit()
                                break
            else:
                airports = []
                unkown_user(call.message)
            try:
                session.commit()
            except Exception as e:
                logger.error(f"Error occurred: {e}")

    elif 'departure' in call.data:
        with Session() as session:
            row = session.query(Tickets).filter(Tickets.ID == call.data.split()[-1]).first()
            msg = f'''✈️<b>{row.Title}</b>✈️
    {row.Cabin}
    -----------------------
    {row.Price} (was {row.OriginalPrice})
    -----------------------
    {row.Dates}
    -----------------------
    ORDER BY: {row.Type}
    -----------------------
    <b>Departure cities:</b>

    {row.DepartureCities}'''   
            markup = msg_markup(row.ID, 'departure')
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg, parse_mode='HTML', reply_markup=markup)
            bot.answer_callback_query(call.id, 'Fetching...')
            try:
                session.commit()
            except Exception as e:
                logger.error(f"Error occurred: {e}")
                
    elif 'book_guide' in call.data:
        with Session() as session:
            row = session.query(Tickets).filter(Tickets.ID == call.data.split()[-1]).first()
            msg = f'''✈️<b>{row.Title}</b>✈️
    {row.Cabin}
    -----------------------
    {row.Price} (was {row.OriginalPrice})
    -----------------------
    {row.Dates}
    -----------------------
    ORDER BY: {row.Type}
    -----------------------
    <b>Booking guide:</b>

    {row.BookGuide}'''        
            markup = msg_markup(row.ID, 'guide')
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg, parse_mode='HTML', reply_markup=markup)
            bot.answer_callback_query(call.id, 'Fetching...')
            try:
                session.commit()
            except Exception as e:
                logger.error(f"Error occurred: {e}")
    elif 'summary' in call.data:
        with Session() as session:
            row = session.query(Tickets).filter(Tickets.ID == call.data.split()[-1]).first()
            msg = f'''✈️<b>{row.Title}</b>✈️
    {row.Cabin}
    -----------------------
    {row.Price} (was {row.OriginalPrice})
    -----------------------
    {row.Dates}
    -----------------------
    ORDER BY: {row.Type}
    -----------------------
    <b>Deal Summary:</b>

    {row.Summary}'''        
            markup = msg_markup(row.ID, 'summary')
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg, parse_mode='HTML', reply_markup=markup)
            bot.answer_callback_query(call.id, 'Fetching...')
            try:
                session.commit()
            except Exception as e:
                logger.error(f"Error occurred: {e}")

    elif call.data  ==  'end' :
        with Session() as session:
            user = session.query(Users).filter_by(ID = call.message.chat.id).first()
            if not user:
                session.close()
                unkown_user(call.message)
            else:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'<b>Your airports:</b> 🛫\n{user.Airports}', parse_mode='HTML')
                bot.answer_callback_query(call.id, 'Fetching your airports...')
            try:
                session.commit()
            except Exception as e:
                logger.error(f"Error occurred: {e}")

    elif 'next' in call.data:
        with Session() as session:
            prev_page = int(call.data.split('_')[-2]) 
            msg_pos = prev_page * 20

            prefix = call.data.split('_')[0]
            page = int(call.data.split('_')[-2]) + 1
            
            user = session.query(Users).filter_by(ID = call.message.chat.id).first()
            if not user:
                session.close()
                unkown_user(call.message)
                return
            airports = user.Airports.split('\n')
            if prefix == 'add':
                new_markup = airport_buttons(prefix, all_airports, msg_pos, page=page, direction='forward')
            else:
                new_markup = airport_buttons(prefix, airports, msg_pos, page=page, direction='forward')
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=new_markup)
            try:
                session.commit()
            except Exception as e:
                logger.error(f"Error occurred: {e}")

    elif 'back' in call.data:
        with Session() as session:
            prev_page = int(call.data.split('_')[-2])  -1
            msg_pos = (prev_page * 20) - 20
            user = session.query(Users).filter_by(ID = call.message.chat.id).first()
            airports = user.Airports.split('\n')
            prefix = call.data.split('_')[0]
            page = int(call.data.split('_')[-2]) - 1
            if prefix == 'add':
                new_markup = airport_buttons(prefix, all_airports, msg_pos, page=page, direction='backward')
            else:
                new_markup = airport_buttons(prefix, airports,msg_pos, page=page, direction='backward')
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=new_markup)
            try:
                session.commit()
            except Exception as e:
                logger.error(f"Error occurred: {e}")

    if call.data == 'subscribed':
        member = check_channel_subscription(call.message)
        if member:
            bot.answer_callback_query(call.id, 'Successfully ✅')
            bot.delete_message(call.message.chat.id, call.message.id)
            get_airports(call.message, flag=True)
        else:
            bot.answer_callback_query(call.id, '''Hmm, it looks like you haven't subscribed yet. Please subscribe to continue getting personalized flight alerts. We can't wait to get you started! 🚀''', show_alert=True)


if __name__ == '__main__': 
    bot.remove_webhook()      
    bot.infinity_polling(skip_pending=True)