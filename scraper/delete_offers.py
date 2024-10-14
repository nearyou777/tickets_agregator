import telebot
from time import sleep
from telebot import types
from shared.models import Tickets,Users, SentMessage
import math
from shared.config import engine
from dotenv import load_dotenv
import os
import json
from shared.config import all_airports
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker
load_dotenv()
Session = sessionmaker(bind=engine)

def autodelete():
    with Session() as session:
        # data = session.query(Tickets).filter(Tickets.DateAdded <= Tickets.DateAdded + timedelta(days=30)).delete(synchronize_session=False)

        data = session.query(Tickets).filter(Tickets.DateAdded >= Tickets.DateAdded + timedelta(days=30)).all()
        # data = session.query(Tickets).filter(Tickets.DateAdded < datetime.now()).all()
        for row in data:
            print(row.DateAdded)
            if os.path.isfile(f'/imgs/{row.PictureName}'):
                try:
                    os.remove(f'/imgs/{row.PictureName}')
                except Exception as e:
                    print('zalupa')
        data = session.query(Tickets).filter(Tickets.DateAdded >= Tickets.DateAdded + timedelta(days=30)).delete(synchronize_session=False)
        session.commit()
       

if __name__ == '__main__':
    autodelete()