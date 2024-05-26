import telebot
from time import sleep
from telebot import types
from config import Tickets,Users, SentMessage, NewTickets
from sqlalchemy.orm import sessionmaker
import math
from config import engine
from dotenv import load_dotenv
import os
import json
from config import all_airports
from datetime import datetime, timedelta
import pandas as pd
load_dotenv()



def export_tables():
    Session = sessionmaker(bind=engine)
    session = Session()
    for table_name in ['Tickets', 'NewTickets', 'Users']:
        try:
            query = f"SELECT * FROM {table_name}"
            df = pd.read_sql(query, session.bind)

            df.to_csv(f'out/{table_name}.csv', index=False)
        except Exception as e:
            print(e)
        finally:
            session.close()

# Пример использования функции
if __name__ == '__main__':
    export_tables()