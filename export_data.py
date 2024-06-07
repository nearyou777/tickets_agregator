import telebot
from time import sleep
from dotenv import load_dotenv
from models import Session
import pandas as pd
load_dotenv()



def export_tables():
    with Session() as session:
        for table_name in ['Tickets', 'NewTickets', 'Users']:
            try:
                query = f"SELECT * FROM {table_name}"
                df = pd.read_sql(query, session.bind)

                df.to_csv(f'out/{table_name}.csv', index=False)
            except Exception as e:
                print(e)


# Пример использования функции
if __name__ == '__main__':
    export_tables()