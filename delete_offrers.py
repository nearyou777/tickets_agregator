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
load_dotenv()
Session = sessionmaker(bind=engine)

def autodelete():
    with Session() as session:
        session.query(Tickets).filter(Tickets.DateAdded >= Tickets.DateAdded + timedelta(days=30)).delete(synchronize_session=False)
        session.commit()


if __name__ == '__main__':
    autodelete()