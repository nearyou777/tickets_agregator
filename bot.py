import tls_client
import json
import pandas as pd
import telebot
from time import sleep
from telebot.handler_backends import ContinueHandling
from telebot import types
from thriftytraveler import get_data, add_db
from save_bd import Tickets, NewTickets, Users, SentMessage
# from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import math
from config import all_airports, engine
token = '6985026926:AAGmdugf_OueWb-jkgKlOMVAOpyj5T_CA4Q'
bot = telebot.TeleBot('6985026926:AAGmdugf_OueWb-jkgKlOMVAOpyj5T_CA4Q')
# engine = create_engine('sqlite:///tickets.db', echo=True)

# Создайте engine для работы с базой данных PostgreSQL

#FIXME: CLEAR ALL COMMENTS

airports = []
current_position = 0
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

    total_pages = math.ceil(len(choosed_airports) // step) + 1
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
    #FIXME: 
    bot.send_message(message.chat.id, 'Welcome to my bot. Lets register together!. Press any key to register')
    bot.register_next_step_handler(message, start_message)
@bot.message_handler(commands=['register'])
def start_message(message):


    user_id = message.chat.id
    Session = sessionmaker(bind=engine)
    session = Session()
    user_data  = session.query(Users).filter_by(ID = user_id).first()
    session.close()
    if not user_data:
        bot.send_message(message.chat.id,"Hi let's register you. Please enter your name")
        bot.register_next_step_handler(message, get_name)
    else:
        bot.send_message(message.chat.id,"Hi let's update your personal data. Please enter your name")
        bot.register_next_step_handler(message, get_name)
    session.close()
    
#TODO: 1.Create a function for inviting peoples to a group 
    #2. Checking if user subscribed before allowing any commands 



def get_name(message):
    name = message.text
    user_id = message.chat.id
    # bot.register_next_step_handler()
    Session = sessionmaker(bind=engine)
    session = Session()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Add airports') 
    btn2 = types.KeyboardButton('Remove airports')
    btn3 = types.KeyboardButton('My profile')
    markup.row(btn1, btn2, btn3)
    bot.send_message(message.chat.id, f"Let's choose airports, that you would like to see: ", reply_markup=markup)
    if not session.query(Users).filter_by(ID = user_id).first():
        bot.send_message(message.chat.id, text='Choose airport to add', reply_markup=airport_buttons('add', all_airports))

        session.add(Users(ID=user_id, Name=name, Airports=', '.join(airports)))
        session.commit()
        session.close()
    else:
        user_to_upd = session.query(Users).filter_by(ID = user_id).first()
        user_to_upd.ID = user_id
        user_to_upd.Name = name 
        session.commit()
        session.close()
        bot.send_message(message.chat.id, f"Hello, {name}.Your personal data updated successfully. Let's update airports, that you would like to see: ", reply_markup=markup)
        bot.send_message(message.chat.id, text='Choose airport to add', reply_markup=airport_buttons('add', all_airports))
        # bot.send_message(message.chat.id, text='Choose airport to add', reply_markup=airport_buttons('add', all_airports[97:194]))
        # bot.send_message(message.chat.id, text='Choose airport to add', reply_markup=airport_buttons('add', all_airports[194:]))

def update_data(message):
    markup = airport_buttons()
    user_id = message.chat.id

    # bot.register_next_step_handler()
    Session = sessionmaker(bind=engine)

@bot.message_handler(commands=['search'])
def search_message(message):
    # data = get_data() #thrifty
    
    Session = sessionmaker(bind=engine)
    session = Session()
    user = session.query(Users).filter_by(ID = message.chat.id).first()
    user_airports = user.Airports.split('\n')
    for airport in user_airports:
            data = session.query(NewTickets).filter(NewTickets.DepartureAirports.like(f'%{airport}%')).all()
            user_id = message.chat.id
            for row in data:
                if session.query(SentMessage).filter_by(user_id=user_id, message_id=row.ID).first():
                    continue
                msg = f'''<strong>{row.Title}</strong>
{row.Cabin}
-----------------------
{row.Price}
-----------------------
ORDER BY: {row.Type}'''
                markup = types.InlineKeyboardMarkup()
                btn_cities = types.InlineKeyboardButton('Departure cities', callback_data=f'departure {row.ID}')
                markup.row(btn_cities)
                # Отправляем сообщение
                bot.send_message(user_id, msg, parse_mode='HTML', reply_markup=markup)
                # Сохраняем информацию о сообщении в базе данных
                sent_message = SentMessage(user_id=user_id, message_id=f"new_{row.ID}")
                session.add(sent_message)
                session.commit()
                data.remove(row)
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
    global current_position

    if 'Add airports' in message.text:
        current_position = 0
        bot.send_message(message.chat.id, text='Choose airport to add', reply_markup=airport_buttons('add', all_airports))

    
    elif 'Remove airports' in message.text:

        current_position = 0
        if len(airports) == 0: 
            bot.send_message(message.chat.id, text='Your airports list is empty')   
        else:
            airports = user.Airports.strip().split('\n')
            bot.send_message(message.chat.id, text='Choose airport to remove', reply_markup=airport_buttons('remove', airports))   

    elif 'My profile' in message.text:
        Session = sessionmaker(bind=engine)
        session = Session()
        user = session.query(Users).filter_by(ID = message.chat.id).first()
        session.close()
        if user:
            # print(user.Name)
            # user.Airports = "\n".join(airports)
            # print(user.Airports)
            bot.send_message(message.chat.id, f'<b>Your name: </b>{user.Name}\n<b>Your airports: </b>\n{user.Airports.strip()}', parse_mode='HTML')
        else:
            bot.send_message(message.chat.id, 'You\'re not registred\nType /register to start' )
    elif 'Profile' in message.text:
        Session = sessionmaker(bind=engine)
        session = Session()
        user = session.query(Users).filter_by(ID = message.chat.id).first()
        session.close()
        if user:
            user_airports = "\n".join(user.Airports)
            msg = f'<b>Name:</b> {user.Name}\n<b>Your airports: </b>{user_airports}'
            bot.send_message(message.chat.id, msg, parse_mode='HTML')
        else:
            bot.send_message(message.chat.id, 'You\'re not registred\nType /register to start' )
    
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    global current_position

    Session = sessionmaker(bind=engine)
    session = Session()
    user = session.query(Users).filter_by(ID = call.message.chat.id).first()
    if user:
        airports = user.Airports.split('\n')
        if len(airports) == 0:
            airports = []
    else:
        airports = []
    session.close()
    if 'add' in call.data and '_scrollbtn' not in call.data:

        for airport in all_airports:
            Session = sessionmaker(bind=engine)
            session = Session()
            if call.data == f'add_{airport}':


                user = session.query(Users).filter_by(ID = call.message.chat.id).first()
                if airport in user.Airports:
                    bot.answer_callback_query(call.id, f'Airport {airport} is already in your favourites list')
                else:
                    bot.answer_callback_query(call.id, f'Airport {airport} is added to your favourites')
                    airports.append(airport)
            user.Airports = "\n".join(airports)
            session.commit()
            session.close()
    elif 'remove' in call.data and '_scrollbtn' not in call.data:
        if call.data == 'remove_all':
            Session = sessionmaker(bind=engine)
            session = Session()
            user = session.query(Users).filter_by(ID = call.message.chat.id).first()
            user.Airports = ""
            session.commit()
            session.close()
            bot.answer_callback_query(call.id, f'All airports is removed from your favourites')
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Your airports list is now empty', parse_mode='HTML')
        else:
            for airport in all_airports:
                if call.data == f'remove_{airport}':
                    if airport in airports:
                        airports.remove(airport)
                        bot.answer_callback_query(call.id, f'Airport {airport} is removed from your favourites')
                        markup = airport_buttons('remove', airports)
                        
                        if len(airports) == 1:
                            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Your airports list is now empty', parse_mode='HTML')
                        else:
                            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=markup)
                        current_position = 0
                        break

            Session = sessionmaker(bind=engine)
            session = Session()
            user = session.query(Users).filter_by(ID = call.message.chat.id).first()
            if not user:
                bot.answer_callback_query(call.id, 'You\'re not registred')
                bot.send_message(call.message.chat.id, 'You\'re not registred\nType /register to start')
                session.close()
            else:
                user.Airports = "\n".join(airports)
                session.commit()
                session.close()
            

    elif 'departure' in call.data:
        # print(call.data)
        Session = sessionmaker(bind=engine)
        session = Session()
        # print(call.message.text)
        cities = session.query(Tickets).filter_by(ID = call.data.split()[-1]).first()
        # print(len(cities))
        # print(cities.DepartureCities)
        msg = f'''<b>{call.message.text}\n\nDeparture cities: </b>\n{cities.DepartureCities}'''
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg, parse_mode='HTML')
        bot.answer_callback_query(call.id, 'Fetching departure cities...')
        session.close()
    elif call.data == 'all':
        Session = sessionmaker(bind=engine)
        session = Session()
        user = session.query(Users).filter_by(ID = call.message.chat.id).first()
        if not user:
            bot.answer_callback_query(call.id, 'You\'re not registred')
            bot.send_message(call.message.chat.id, 'You\'re not registred\nType /register to start')
        else:
            user.Airports = "\n".join(all_airports)
            session.commit()
            session.close()
            bot.answer_callback_query(call.id, 'Fetching...')
            bot.send_message(call.message.chat.id, 'You\'ve choosed all airports')
        session.close()
    elif call.data  ==  'end' :
        Session = sessionmaker(bind=engine)
        session = Session()
        user = session.query(Users).filter_by(ID = call.message.chat.id).first()
        session.close()
        if not user:
            bot.send_message(call.message.chat.id, 'You\'re not registred\nType /register to start')
            bot.answer_callback_query(call.id, 'You\'re not registred')

        else:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'<b>Your airports:</b>\n{user.Airports}', parse_mode='HTML')
            bot.answer_callback_query(call.id, 'Fetching your airports...')
        session.close()
    elif 'next' in call.data:
        Session = sessionmaker(bind=engine)
        session = Session()
        prev_page = int(call.data.split('_')[-2]) 
        msg_pos = prev_page * 20
        # msg_pos += 20
        current_position += 20
        # print(current_position, msg_pos)
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
        print(prev_page)
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




