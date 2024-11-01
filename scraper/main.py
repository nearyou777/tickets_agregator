from time import sleep
from shared.rabit_config import get_connection,RMQ_ROUTING_KEY
from pomelo import add_pomelo
from thriftytraveler import add_thrifty
from going import add_going
from delete_offers import autodelete
from send_messages import produce_message, send_to_db


def process_data(data):
    for item in data:
        send_to_db(item)
        with get_connection() as connection:
            with connection.channel() as channel:
                produce_message(channel, RMQ_ROUTING_KEY, data=item)


def scrape_data():
    while True:
        try:
            data = add_thrifty()
        except Exception as e:
            print(f"Error in add_thrifty: {e}")
            data = None

        if not data:
            try:
                data = add_pomelo()
            except Exception as e:
                print(f"Error in add_pomelo: {e}")
                data = None

            if not data:
                try:
                    data = add_going()
                except Exception as e:
                    print(f"Error in add_going: {e}")
                    data = None

            if not data:
                autodelete()
                with get_connection() as connection:
                    with connection.channel() as channel:
                        produce_message(channel, RMQ_ROUTING_KEY, data={'Type': 'technical message'})
                sleep(180)

        if data:
            process_data(data)


def main():
    sleep(15)
    with get_connection() as connection:
        with connection.channel() as channel:
            produce_message(channel, RMQ_ROUTING_KEY, data={'Type': 'technical message'})
    scrape_data()



if __name__ == '__main__':
    main()      