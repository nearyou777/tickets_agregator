import telebot
from time import sleep
from telebot import types
from config import Tickets,Users, SentMessage, all_airports, engine, isadmin
from sqlalchemy.orm import sessionmaker
import math
from dotenv import load_dotenv
import os
import json
from datetime import datetime, timedelta
from telebot.apihelper import ApiException
from export_data import export_tables
import html2text
load_dotenv()
from bot import bot
from bs4 import BeautifulSoup
import pyshorteners
my_id = os.getenv('my_id')
import html2text
import requests

url = 'https://d3mdkiyq6mk8lq.cloudfront.net/images/deals/01HZ00TZEQNSK2YXFA3RNN3N7C.avif'
with open('test.avif', 'wb') as f:
    f.write(requests.get(url).content)
    # bot.send_photo(my_id, f)
# url = 'https://www.google.com/travel/flights/search?tfs=CBwQAhpGEgoyMDI0LTA5LTA0Mg1TVEFSX0FMTElBTkNFMgdTS1lURUFNMghPTkVXT1JMRGoHCAESA0xBWHINCAISCS9tLzAyMndyMxpGEgoyMDI0LTA5LTExMg1TVEFSX0FMTElBTkNFMgdTS1lURUFNMghPTkVXT1JMRGoNCAISCS9tLzAyMndyM3IHCAESA0xBWEABSAFwAYIBCwj___________8BmAEB&hl=en-US&gl=US&curr=USD'
# short_url = pyshorteners.Shortener().tinyurl.short(url)

# from telegram

# html_content = """
# <p>This trip requires booking 2 round-trip flights with options from any of the departure cities listed above to Dublin and from Dublin to the Isle of Man.<br><br>Your trip will look something like this:</p>
# <ul>
#     <li>Departure city from above to Dublin, Ireland via multiple airline options from $394 round-trip</li>
#     <li>Dublin, Ireland to Isle of Man via Aer Lingus from $146 nonstop</li>
# </ul>
# <p><strong>Total: $540-$685+</strong></p>
# """

# text_maker = html2text.HTML2Text()
# text_maker.ignore_links = True
# text_maker.ignore_images = True

# markdown_content = text_maker.handle(html_content)
# with open('test.json') as f:
#     item = json.load(f)['data'][0]["booking_instructions_override"][0]['headline']
#     text_maker = html2text.HTML2Text()
#     text_maker.ignore_links = True
#     text_maker.ignore_images = True

#     data = text_maker.handle(item).replace('*', '-').replace('--', '*')
#     # data = text_maker.handle(item)
#     # print(data)
#     bot.send_message(my_id, f"{data}", parse_mode='Markdown')
# a = 'abc'
# print(a + 'd')
# Session = sessionmaker(bind=engine)
# session = Session()
# data = session.query(Tickets).filter(Tickets.DepartureAirports.like(f'%(SFO)%')).all()
# print(len(data))