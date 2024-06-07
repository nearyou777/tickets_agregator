import telebot
from time import sleep
from telebot import types
from models import Tickets,Users, SentMessage
import math
from config import engine
from dotenv import load_dotenv
import os
import json
from config import all_airports
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker
from bot import bot
load_dotenv()
Session = sessionmaker(bind=engine)

def autodelete():
    with Session() as session:
        data = session.query(Tickets).filter(Tickets.DateAdded >= Tickets.DateAdded + timedelta(days=30)).all()
        for row in data:
            if os.path.isfile(f'/imgs/{row.PictureName}'):
                try:
                    os.remove(f'/imgs/{row.PictureName}')
                except Exception as e:
                    bot.send_message(os.getenv('my_id'), f'Error while deleting file\n{e}')
        data = session.query(Tickets).filter(Tickets.DateAdded >= Tickets.DateAdded + timedelta(days=30)).delete(synchronize_session=False)
        session.commit()
       

if __name__ == '__main__':
    autodelete()