import telebot
from time import sleep
from telebot import types
from sqlalchemy.orm import sessionmaker
import math
from dotenv import load_dotenv
import os
import json
from config import all_airports
from models import Session
from datetime import datetime, timedelta
import pandas as pd
load_dotenv()



def export_tables():
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