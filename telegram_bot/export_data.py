import telebot
from time import sleep
from dotenv import load_dotenv
from shared.models import Session
import pandas as pd
import logging

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
load_dotenv()



def export_tables():
    with Session() as session:
        for table_name in ['Tickets', 'NewTickets', 'Users']:
            try:
                query = f"SELECT * FROM {table_name}"
                df = pd.read_sql(query, session.bind)
                session.commit()
                df.to_csv(f'out/{table_name}.csv', index=False)
            except Exception as e:
                print(e)


if __name__ == '__main__':
    export_tables()