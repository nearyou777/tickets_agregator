from telebot import types
from models import Tickets
from config import Session
import math
import os
from dotenv import load_dotenv
import logging

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
load_dotenv()


def current_pos(position):
    for i in range(position,0,-1):
        if i % 20 == 0:
            return i
    return 0


def msg_markup(offer_id, position='start'):
    with Session() as session:
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


def channel_mark():
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Our Channel', url=os.getenv('channel_url'))
    btn2 = types.InlineKeyboardButton('I\'m subscribed✅', callback_data=f'subscribed')
    markup.add(btn1)
    markup.add(btn2)
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
        buttons = [types.InlineKeyboardButton(airport, callback_data=f'{prefix}_{airport}_{page}') for airport in chunk]
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

def create_deal_msg(row:Tickets):
    if row.OriginalPrice != 0:
        if row.Type == 'Cash':
            try:
                original_price = int(row.OriginalPrice.split('-')[0].replace('+', '').replace('$', '').replace('Under', '').replace('s', '').replace('From', '').replace('For', '').replace(',', '').strip())
                price = int(row.Price.split('-')[0].replace('+', '').replace('$', '').replace('Under', '').replace('s', '').replace('From', '').replace('For', '').replace(',', '').strip())
                print(original_price, price)
                discount = (100*(original_price - price)) // original_price
            except:
                discount = 'Huge'
            msg = f'''✈️<b>{row.Title}</b>✈️
<b>{discount}% OFF🔥🔥🔥</b>
-----------------------
{row.Cabin}
-----------------------
{row.Price} (was {row.OriginalPrice})
-----------------------
{row.Dates}
-----------------------
ORDER BY: {row.Type}'''
        else:
            discount = None
            msg = f'''✈️<b>{row.Title}</b>✈️
-----------------------
{row.Cabin}
-----------------------
{row.Price} (was {row.OriginalPrice})
-----------------------
{row.Dates}
-----------------------
ORDER BY: {row.Type}'''
    else:
        msg = f'''✈️<b>{row.Title}</b>✈️
-----------------------
{row.Cabin}
-----------------------
{row.Price}
-----------------------
{row.Dates}
-----------------------
ORDER BY: {row.Type}'''
    return msg


def main():
    pass

if __name__ == '__main__':
    main()