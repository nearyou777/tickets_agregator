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
from datetime import datetime, timedelta
from config import Tickets, engine
load_dotenv()

Session = sessionmaker(bind=engine)

def autodelete():
    session = Session()
    session.query(Tickets).filter(Tickets.DateAdded >= Tickets.DateAdded + timedelta(days=30)).delete(synchronize_session=False)
    session.commit()
    session.close()


if __name__ == '__main__':
    autodelete()