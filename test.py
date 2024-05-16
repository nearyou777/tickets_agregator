
# from sqlalchemy import create_engine, Column, Integer, String
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# from save_bd import Tickets
# from save_bd import Tickets, NewTickets, Users,SentMessage
# engine = create_engine('sqlite:///tickets.db', echo=True)
# # airports = ['zalupa', 'huy', 'pizda']
# # Base = declarative_base()
# # Session = sessionmaker(bind=engine)
# # session = Session()
# # session.add(Users(ID='1234', Name='pidatas', Airports=', '.join(airports)))
# # session.commit()
# # session.close()
# Session = sessionmaker(bind=engine)
# session = Session()


# session.query(Tickets).filter(Tickets.DepartureAirports.like('%Austin (AUS)%')).delete(synchronize_session=False)
# session.query(SentMessage).delete(synchronize_session=False)
# session.commit()
# session.close()


import tls_client
import json
import pandas as pd
import telebot
from time import sleep
from telebot.handler_backends import ContinueHandling
from telebot import types
from thriftytraveler import get_data, add_db
from save_bd import Tickets, NewTickets, Users
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import all_airports
token = '6985026926:AAGmdugf_OueWb-jkgKlOMVAOpyj5T_CA4Q'
bot = telebot.TeleBot('6985026926:AAGmdugf_OueWb-jkgKlOMVAOpyj5T_CA4Q')
engine = create_engine('sqlite:///tickets.db', echo=True)



airports = []

@bot.message_handler(commands=['start'])
def welcome_message(message):
    bot.send_message(message.chat.id, 'Welcome to my bot. Lets register together!. Press any key to register')
    bot.register_next_step_handler(message, start_message)
@bot.message_handler(commands=['register'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Add airports') 
    btn2 = types.KeyboardButton('Remove airports')
    btn3 = types.KeyboardButton('My airports')
    # btn4 =  types.KeyboardButton('Profile')
    markup.row(btn1, btn2, btn3)
    # markup.row(btn3, btn4)
    user_id = message.chat.id
    Session = sessionmaker(bind=engine)
    session = Session()
    user_data  = session.query(Users).filter_by(ID = user_id).first()
    session.close()
    if not user_data:
        bot.send_message(message.chat.id,"Hi let's register you. Please enter your name", reply_markup=markup)
        bot.register_next_step_handler(message, get_name)
    else:
        bot.send_message(message.chat.id,"Hi let's update your personal data. Please enter your name", reply_markup=markup)
        bot.register_next_step_handler(message, get_name)
    
def airport_buttons(prefix: str, all_airports:list):
    markup = types.InlineKeyboardMarkup()
    max_buttons_per_row = 3  # Максимальное количество кнопок на одной строке

    for i in range(0, len(all_airports), max_buttons_per_row):
        row_airports = all_airports[i:i+max_buttons_per_row]
        buttons = [types.InlineKeyboardButton(airport, callback_data=f'{prefix}_{airport}') for airport in row_airports]
        markup.row(*buttons)
    if 'remove' in prefix:
        btn1 = types.InlineKeyboardButton('Remove all airports', callback_data='remove_all')
    else :
        btn1 = types.InlineKeyboardButton('Add all airports', callback_data='all')
    btn2 = types.InlineKeyboardButton('That\'s all', callback_data='end')
    markup.row(btn1, btn2)


    return markup



def get_name(message):
    name = message.text
    # print(f'\n\n\n\n\n\n\n{name}\n\n\n\n\n\n\n')
    user_id = message.chat.id
    # bot.register_next_step_handler()
    Session = sessionmaker(bind=engine)
    session = Session()
    if not session.query(Users).filter_by(ID = user_id).first():

        bot.send_message(message.chat.id, f"Hello, {name}. Let's choose airports, that you would like to see: ")
        bot.send_message(message.chat.id, text='Choose airport to add', reply_markup=airport_buttons('add', all_airports[:97]))
        bot.send_message(message.chat.id, text='Choose airport to add', reply_markup=airport_buttons('add', all_airports[97:194]))
        bot.send_message(message.chat.id, text='Choose airport to add', reply_markup=airport_buttons('add', all_airports[194:]))
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
        bot.send_message(message.chat.id, text='Choose airport to add', reply_markup=airport_buttons('add', all_airports[:97]))
        bot.send_message(message.chat.id, text='Choose airport to add', reply_markup=airport_buttons('add', all_airports[97:194]))
        bot.send_message(message.chat.id, text='Choose airport to add', reply_markup=airport_buttons('add', all_airports[194:]))

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
        data = session.query(Tickets).filter(Tickets.DepartureAirports.like(f'%{airport}%')).all()
        for row in data:
            msg = f'''<strong>{row.Title}</strong>
{row.Cabin}
-----------------------
{row.Price}
-----------------------
ORDER BY: {row.Type}'''
            markup = types.InlineKeyboardMarkup()

            btn_cities = types.InlineKeyboardButton('Departure cities', callback_data=f'departure {row.ID}')
            markup.row(btn_cities)

            # msg_content = f"<b>{row['Title']}</b> \n{row['Cabin']}\n{row['Price']}"
            bot.send_message(message.chat.id, msg, parse_mode='HTML', reply_markup=markup)
    session.close()
@bot.message_handler(content_types=['text'])
def on_click(message:types.Message):
    Session = sessionmaker(bind=engine)
    session = Session()
    user = session.query(Users).filter_by(ID = message.chat.id).first()
    if user:
        airports = user.Airports.split('\n')
        if len(airports) == 0:
            airports = []
    else:
        airports = []
    session.close()
    # if '/' in message.text:
    #     bot.send_message(message.chat.id, 'You should register before using commands. Please enter your name: ')
    #     bot.register_next_step_handler(message, get_name)
    if 'Add airports' in message.text:
        bot.send_message(message.chat.id, text='Choose airport to add', reply_markup=airport_buttons('add', all_airports[:97]))
        bot.send_message(message.chat.id, text='Choose airport to add', reply_markup=airport_buttons('add', all_airports[97:194]))
        bot.send_message(message.chat.id, text='Choose airport to add', reply_markup=airport_buttons('add', all_airports[194:]))
    
    elif 'Remove airports' in message.text:
        if len(airports) < 97:
            markup = airport_buttons('remove', airports)
            bot.send_message(message.chat.id, text='Choose airport to remove', reply_markup=markup)
        elif len(airports) < 194:
            markup = airport_buttons('remove', airports[:97])
            bot.send_message(message.chat.id, text='Choose airport to remove', reply_markup=markup)

            markup = airport_buttons('remove', airports[97:])
            bot.send_message(message.chat.id, text='Choose airport to remove', reply_markup=markup)
        elif len(airports) > 194:
            markup = airport_buttons('remove', airports[:97])
            bot.send_message(message.chat.id, text='Choose airport to remove', reply_markup=markup)

            markup = airport_buttons('remove', airports[97:194])
            bot.send_message(message.chat.id, text='Choose airport to remove', reply_markup=markup)

            markup = airport_buttons('remove', airports[194: ])
            bot.send_message(message.chat.id, text='Choose airport to remove', reply_markup=markup)
    elif 'My airports' in message.text:
        Session = sessionmaker(bind=engine)
        session = Session()
        user = session.query(Users).filter_by(ID = message.chat.id).first()
        session.close()
        if user:
            print(user.Name)
            # user.Airports = "\n".join(airports)
            print(user.Airports)
            bot.send_message(message.chat.id, f'<b>Your airports: </b>\n{user.Airports.strip()}', parse_mode='HTML')
        else:
            bot.send_message(message.chat.id, 'You\'re not registred\nType /register to start' )
    elif 'Profile' in message.text:
        Session = sessionmaker(bind=engine)
        session = Session()
        user = session.query(Users).filter_by(ID = message.chat.id).first()
        session.close()
        if user:
            # print(user.Name)
            # # user.Airports = "\n".join(airports)
            # print(user.Airports)
            msg = f'<b>Name:</b> {user.Name}\n<b>Your airports: </b>{"\n".join(user.Airports)}'
            bot.send_message(message.chat.id, msg, parse_mode='HTML')
        else:
            bot.send_message(message.chat.id, 'You\'re not registred\nType /register to start' )
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
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
    if 'add' in call.data:
        for airport in all_airports:
            if call.data == f'add_{airport}':

                Session = sessionmaker(bind=engine)
                session = Session()
                user = session.query(Users).filter_by(ID = call.message.chat.id).first()
                if airport in user.Airports:
                    bot.answer_callback_query(call.id, f'Airport {airport} is already in your favourites list')
                else:
                    bot.answer_callback_query(call.id, f'Airport {airport} is added to your favourites')
                    # print(call.message.chat.id)
                    airports.append(airport)
            user.Airports = "\n".join(airports)
            session.commit()
            session.close()
    elif 'remove' in call.data:
        if call.data == 'remove_all':
            Session = sessionmaker(bind=engine)
            session = Session()
            user = session.query(Users).filter_by(ID = call.message.chat.id).first()
            user.Airports = ""
            session.commit()
            session.close()
            bot.answer_callback_query(call.id, f'All airports is removed from your favourites')
        else:
            for airport in all_airports:
                if call.data == f'remove_{airport}':
                    if airport in airports:
                        airports.remove(airport)
                        bot.answer_callback_query(call.id, f'Airport {airport} is removed from your favourites')
                        markup = airport_buttons('remove', airports)
                        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=markup)

                # else:
                #     bot.answer_callback_query(call.id, f'Airport {airport} is not in your favourites')
            Session = sessionmaker(bind=engine)
            session = Session()
            user = session.query(Users).filter_by(ID = call.message.chat.id).first()
            if not user:
                bot.answer_callback_query(call.id, 'You\'re not registred')
                bot.send_message(call.message.chat.id, 'You\'re not registred\nType /register to start')
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
    elif call.data  ==  'end' :
        Session = sessionmaker(bind=engine)
        session = Session()
        user = session.query(Users).filter_by(ID = call.message.chat.id).first()
        session.close()
        if not user:
            bot.send_message(call.message.chat.id, 'You\'re not registred\nType /register to start')
            bot.answer_callback_query(call.id, 'You\'re not registred')
            # bot.register_next_step_handler(call.message, start_message)
        # airports_to_show = "\n".join(airports)
        else:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'<b>Your airports:</b>\n{user.Airports}', parse_mode='HTML')
            bot.answer_callback_query(call.id, 'Fetching your airports...')

if __name__ == '__main__':       
    bot.infinity_polling(skip_pending=True)




