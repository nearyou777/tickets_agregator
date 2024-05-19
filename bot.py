import telebot
from time import sleep
from telebot import types
from config import Tickets,Users, SentMessage
from sqlalchemy.orm import sessionmaker
import math
from config import engine
from dotenv import load_dotenv
import os
import json
from config import all_airports
load_dotenv()
    
#TODO: 1.Create a function for inviting peoples to a group 
    #2. Checking if user subscribed before allowing any commands 

#TODO: 1. Add datetime to tickets sheet. Create autodelete function
bot = telebot.TeleBot(os.getenv('token'))
airports = []
current_position = 0
Session = sessionmaker(bind=engine)


def unkown_user(message):
    bot.send_message(message.chat.id, 'You\'re not registred.')
    sleep(1)
    start_message(message)

def msg_markup(offer_id, position='start'):
    session = Session()
    row = session.query(Tickets).filter(Tickets.ID == offer_id).first()
    markup = types.InlineKeyboardMarkup()
    btn_cities = types.InlineKeyboardButton('Departure cities', callback_data=f'departure {offer_id}')
    deal_summary = types.InlineKeyboardButton('Deal Summary', callback_data=f'summary {offer_id}')
    book_guide = types.InlineKeyboardButton('Booking Guide', callback_data=f'book_guide {offer_id}')
    book_link = types.InlineKeyboardButton('Book Now', url=row.Book)
    if position == 'start':
        markup.row(deal_summary, btn_cities)
        markup.row(book_guide, book_link) 
    elif position == 'departure':
        markup.row(deal_summary, book_guide)
        markup.row(book_link) 
    elif position == 'guide':
        markup.row(deal_summary, btn_cities)
        markup.row(book_link) 
    else: 
        markup.row(btn_cities, book_guide)
        markup.row(book_link) 
    return markup


def airport_buttons(prefix, choosed_airports, current_position=0, step=20, page=1,direction='forward'):
    markup = types.InlineKeyboardMarkup()
    if direction == 'forward':
        start_index = current_position
        end_index = min(current_position + step, len(choosed_airports))
    elif direction == 'backward':
        end_index = current_position + step
        start_index = max(end_index - step, 0)

    start_index = current_position
    end_index = min(current_position + step, len(choosed_airports))

    airports_chunk = [choosed_airports[i:i+2] for i in range(start_index, end_index, 2)]
    for chunk in airports_chunk:
        buttons = [types.InlineKeyboardButton(airport, callback_data=f'{prefix}_{airport}') for airport in chunk]
        markup.row(*buttons)

    total_pages = math.ceil(len(choosed_airports) / step)
    page_buttons = f'Page {page} of {total_pages}'
    current_button  = types.InlineKeyboardButton(page_buttons, callback_data='empty')
    all_btn = types.InlineKeyboardButton(f'{prefix.capitalize()} All airports', callback_data=f'{prefix}_all')

    if end_index < len(choosed_airports):
        next_button = types.InlineKeyboardButton('Next', callback_data=f'{prefix}_next_{page}_scrollbtn')
    else:
        next_button = None
    if page > 1:
        back_button = types.InlineKeyboardButton('Back', callback_data=f'{prefix}_back_{page}_scrollbtn')
    else:
        back_button = None
    if next_button and not back_button:
        markup.add(all_btn)
        markup.row(current_button, next_button)
    elif next_button and back_button:
        markup.add(all_btn)
        markup.row(back_button, current_button, next_button)
    elif not next_button and not back_button:
        markup.row(all_btn, current_button)
    else:
        markup.add(all_btn)
        markup.row(back_button, current_button)
    return markup


@bot.message_handler(commands=['start'])
def welcome_message(message):
    bot.send_message(message.chat.id, 'Welcome to my bot. Lets register together!. Please enter your name')
    sleep(1)
    bot.register_next_step_handler(message, get_name)


@bot.message_handler(commands=['post'])
def get_post_msg(message):
    #TODO: Create admin profiles
    Session = sessionmaker(bind=engine)
    session = Session()
    user = session.query(Users).filter_by(ID = message.chat.id).first()
    if user:
        bot.send_message(message.chat.id, f'Hi {user.Name}. Enter a post below that you would like to share')
        bot.register_next_step_handler(message, share_post)


def share_post(message):
    Session = sessionmaker(bind=engine)
    session = Session()
    admin = session.query(Users).filter_by(ID=message.chat.id).first()
    
    if "entities" in message.json:
        text = message.json["text"]
        entities = message.json["entities"]
        
        current_position = 0
        formatted_message_parts = []

        for entity in entities:
            offset = entity["offset"]
            length = entity["length"]
            entity_type = entity["type"]

            formatted_message_parts.append(text[current_position:offset])

            if entity_type == "bold":
                formatted_message_parts.append(f'*{text[offset:offset+length]}*')
            elif entity_type == "italic":
                formatted_message_parts.append(f'_{text[offset:offset+length]}_')
            current_position = offset + length
        
        if current_position < len(text):
            formatted_message_parts.append(text[current_position:])
        
        formatted_message = ''.join(formatted_message_parts)

    else:
        formatted_message = message.json["text"]
    
    for user in session.query(Users).all():
        bot.send_message(user.ID, formatted_message.strip(), parse_mode="Markdown")
        sleep(1)
    
    session.close()

@bot.message_handler(commands=['register'])
def start_message(message):
    user_id = message.chat.id
    Session = sessionmaker(bind=engine)
    session = Session()
    user_data  = session.query(Users).filter_by(ID = user_id).first()
    session.close()
    if not user_data:
        bot.send_message(message.chat.id,"Hi let's register you. Please enter your name")
        sleep(1)
        bot.register_next_step_handler(message, get_name)
    else:
        bot.send_message(message.chat.id,"Hi let's update your personal data. Please enter your name")
        sleep(1)
        bot.register_next_step_handler(message, get_name)
    session.close()


def get_name(message):
    name = message.text
    if '/' in name:
        unkown_user(message)
        return
    user_id = message.chat.id
    Session = sessionmaker(bind=engine)
    session = Session()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Add airports') 
    btn2 = types.KeyboardButton('Remove airports')
    btn3 = types.KeyboardButton('My profile')
    markup.row(btn1, btn2, btn3)
    bot.send_message(message.chat.id, f'Hi {name}. You\'re almost done.\nLet\'s choose airports, that you would like to see: ', reply_markup=markup)
    sleep(1)
    if not session.query(Users).filter_by(ID = user_id).first():
        bot.send_message(message.chat.id, text='Choose airport to add', reply_markup=airport_buttons('add', all_airports))
        sleep(1)
        session.add(Users(ID=user_id, Name=name, Airports=', '.join(airports)))
        session.commit()
        session.close()
    else:
        user_to_upd = session.query(Users).filter_by(ID = user_id).first()
        user_to_upd.ID = user_id
        user_to_upd.Name = name 
        session.commit()
        session.close()
        bot.send_message(message.chat.id, f"Hello, {name}.Your personal data updated successfully. Let's update airports, that you would like to see: ")
        sleep(1)
        bot.send_message(message.chat.id, text='Choose airport to add', reply_markup=airport_buttons('add', all_airports))
    sleep(0.5)


@bot.message_handler(commands=['search'])
def search_message(message):    
    Session = sessionmaker(bind=engine)
    session = Session()
    user = session.query(Users).filter_by(ID = message.chat.id).first()
    if user:
        user_airports = user.Airports.split('\n')
        for airport in user_airports:
                data = session.query(Tickets).filter(Tickets.DepartureAirports.like(f'%{airport}%')).all()
                
                user_id = message.chat.id
                for row in data:
                    if session.query(SentMessage).filter_by(user_id=user_id, message_id=f'old_{row.ID}').first():
                        continue
                    msg = f'''<strong>{row.Title}</strong>
{row.Cabin}
-----------------------
{row.Price}
-----------------------
ORDER BY: {row.Type}'''

                    markup = msg_markup(row.ID, 'start')
                    base_path = os.getcwd()
                    photo_path = os.path.join(base_path, f'imgs/{row.PictureName}')
                    with open(photo_path, 'rb') as photo:
                        bot.send_photo(user_id, photo=photo)
                    bot.send_message(user_id, msg, parse_mode='HTML', reply_markup=markup)
                    sleep(1)
                    sent_message = SentMessage(user_id=user_id, message_id=f"old_{row.ID}")
                    session.add(sent_message)
                    session.commit()
                    data.remove(row)
    else:
        unkown_user(message)
    session.close()


@bot.message_handler(content_types=['text'])
def on_click(message:types.Message):
    Session = sessionmaker(bind=engine)
    session = Session()
    user = session.query(Users).filter_by(ID = message.chat.id).first()
    if user:
        airports = user.Airports.strip()
        if len(airports) == 0:
            airports = []
        else:
            airports = airports.split('\n')
    else:
        airports = []
    session.close()

    if 'Add airports' in message.text:
        bot.send_message(message.chat.id, text='Choose airport to add', reply_markup=airport_buttons('add', all_airports))
        sleep(1)
    
    elif 'Remove airports' in message.text:
        if not user:
            unkown_user()
            return
        else:
            if len(airports) == 0: 
                bot.send_message(message.chat.id, text='Your airports list is empty') 
            else:
                airports = user.Airports.strip().split('\n')
                bot.send_message(message.chat.id, text='Choose airport to remove', reply_markup=airport_buttons('remove', airports))   
            sleep(1) 

    elif 'My profile' in message.text:
        Session = sessionmaker(bind=engine)
        session = Session()
        user = session.query(Users).filter_by(ID = message.chat.id).first()
        session.close()
        if user:
            user_airports = user.Airports.strip()

            if len(user.Airports.split('\n')) == 222:
                user_airports = 'All available'
            if len(user.Airports) == 0:
                user_airports = 'You didn\'t choosed any airport' 
            bot.send_message(message.chat.id, f'<b>Your name: </b>{user.Name}\n\n<b>Your airports: </b>\n{user_airports}', parse_mode='HTML')
        else:
            unkown_user(message)
            return
        sleep(1)
    

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    Session = sessionmaker(bind=engine)
    session = Session()
    user = session.query(Users).filter_by(ID = call.message.chat.id).first()
    if user:
        airports = user.Airports.strip()
        if len(airports) == 0:
            airports = []
        else:
            airports = airports.split('\n')
    else:
        airports = []
    session.close()

    if 'add' in call.data and '_scrollbtn' not in call.data :
        Session = sessionmaker(bind=engine)
        session = Session()
        user = session.query(Users).filter_by(ID = call.message.chat.id).first()
        if not user:
            unkown_user()
        else:
            if call.data == 'add_all':
                user.Airports = "\n".join(all_airports)
                session.commit()
                bot.answer_callback_query(call.id, 'Fetching...')
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='You\'ve choosed all airports', parse_mode='HTML')
            else:
                for airport in all_airports:
                    if call.data == f'add_{airport}':
                        user = session.query(Users).filter_by(ID = call.message.chat.id).first()
                        if airport in user.Airports:
                            bot.answer_callback_query(call.id, f'Airport {airport} is already in your favourites list')
                        else:
                            bot.answer_callback_query(call.id, f'Airport {airport} is added to your favourites')
                            airports.append(airport)
                    user.Airports = "\n".join(airports)
                    session.commit()
        session.commit()
        session.close()


    elif 'remove' in call.data and '_scrollbtn' not in call.data:
        Session = sessionmaker(bind=engine)
        session = Session()
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
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Your airports list is now empty', parse_mode='HTML')
            else:
                for airport in airports:
                    if call.data == f'remove_{airport}':
                        if airport in airports:
                            airports.remove(airport)
                            bot.answer_callback_query(call.id, f'Airport {airport} is removed from your favourites')
                            markup = airport_buttons('remove', airports)
                            
                            if len(airports) < 1:
                                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Your airports list is now empty', parse_mode='HTML')
                            else:
                                bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=markup)
                            current_position = 0
                            user.Airports = "\n".join(airports)
                            session.commit()
                            break
        else:
            airports = []
            unkown_user()
        session.close()


    elif 'departure' in call.data:
        Session = sessionmaker(bind=engine)
        session = Session()
       
        row = session.query(Tickets).filter(Tickets.ID == call.data.split()[-1]).first()
        msg = f'''<strong>{row.Title}</strong>
{row.Cabin}
-----------------------
{row.Price}
-----------------------
ORDER BY: {row.Type}

<b>Departure cities: </b>

{row.DepartureCities}'''        
        markup = msg_markup(row.ID, 'departure')
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg, parse_mode='HTML', reply_markup=markup)
        bot.answer_callback_query(call.id, 'Fetching...')
        session.close()

    elif 'book_guide' in call.data:
        Session = sessionmaker(bind=engine)
        session = Session()
        row = session.query(Tickets).filter(Tickets.ID == call.data.split()[-1]).first()
        msg = f'''<strong>{row.Title}</strong>
{row.Cabin}
-----------------------
{row.Price}
-----------------------
ORDER BY: {row.Type}

<b>Booking guide:</b>

{row.BookGuide}'''        
        markup = msg_markup(row.ID, 'guide')
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg, parse_mode='HTML', reply_markup=markup)
        bot.answer_callback_query(call.id, 'Fetching...')
        session.close()

    elif 'summary' in call.data:
        Session = sessionmaker(bind=engine)
        session = Session()
        row = session.query(Tickets).filter(Tickets.ID == call.data.split()[-1]).first()
        msg = f'''<strong>{row.Title}</strong>
{row.Cabin}
-----------------------
{row.Price}
-----------------------
ORDER BY: {row.Type}

<b>Deal Summary:</b>

{row.Summary}'''        
        markup = msg_markup(row.ID, 'summary')
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg, parse_mode='HTML', reply_markup=markup)
        bot.answer_callback_query(call.id, 'Fetching...')
        session.close()

    elif call.data  ==  'end' :
        Session = sessionmaker(bind=engine)
        session = Session()
        user = session.query(Users).filter_by(ID = call.message.chat.id).first()
        if not user:
            unkown_user()
        else:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'<b>Your airports:</b>\n{user.Airports}', parse_mode='HTML')
            bot.answer_callback_query(call.id, 'Fetching your airports...')
        session.close()


    elif 'next' in call.data:
        Session = sessionmaker(bind=engine)
        session = Session()
        prev_page = int(call.data.split('_')[-2]) 
        msg_pos = prev_page * 20
        current_position += 20

        prefix = call.data.split('_')[0]
        page = int(call.data.split('_')[-2]) + 1
        
        user = session.query(Users).filter_by(ID = call.message.chat.id).first()
        airports = user.Airports.split('\n')
        if prefix == 'add':
            new_markup = airport_buttons(prefix, all_airports, msg_pos, page=page, direction='forward')
        else:
            new_markup = airport_buttons(prefix, airports, msg_pos, page=page, direction='forward')
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=new_markup)
        session.close()

    elif 'back' in call.data:
        Session = sessionmaker(bind=engine)
        session = Session()
        prev_page = int(call.data.split('_')[-2])  -1
        msg_pos = (prev_page * 20) - 20
        current_position -= 20
        user = session.query(Users).filter_by(ID = call.message.chat.id).first()
        airports = user.Airports.split('\n')
        prefix = call.data.split('_')[0]
        page = int(call.data.split('_')[-2]) - 1
        if prefix == 'add':
            new_markup = airport_buttons(prefix, all_airports, msg_pos, page=page, direction='backward')
        else:
            new_markup = airport_buttons(prefix, airports,msg_pos, page=page, direction='backward')
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=new_markup)
        session.close()


if __name__ == '__main__': 
    bot.remove_webhook()      
    bot.infinity_polling(skip_pending=True)