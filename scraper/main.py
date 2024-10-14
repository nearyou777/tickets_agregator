import json
from typing import TYPE_CHECKING
import pika.channel
from time import sleep
from shared.rabit_config import get_connection,RMQ_ROUTING_KEY
if TYPE_CHECKING:
    from pika.adapters.blocking_connection import BlockingChannel


def produce_message(ch:"BlockingChannel", routing_key:str, data:dict):
    queue = ch.queue_declare(queue=routing_key)
    msg = json.dumps(data)
    ch.basic_publish(
        exchange="",
        routing_key=routing_key,
        body=msg
    )


def main():
    # while True:
    #     pass
    sleep(15)
    # print('connected')
    # conn = get_connection()
    data = {
        'ID': 123,
        'Title': 'Special Offer',
        'Type': 'Flight',
        'Cabin': 'Economy',
        'Price': 250.0,
        'OriginalPrice': 300.0,
        'Dates': '2024-12-10',
        'Book': 'https://booking.example.com',
        'DepartureCities': 'New York',
        'DepartureAirports': 'JFK',
        'BookGuide': 'Direct booking available',
        'Summary': 'This is a special offer for economy flights.',
        'PictureName': 'special_offer.png'
    }
    with get_connection() as connection:
        with connection.channel() as channel:
            produce_message(channel,RMQ_ROUTING_KEY, data)
    # with get_connection() as conn:
    #     with conn.channel() as channel:
    #         produce_message(channel)
    # print('connected')
    while True:
        pass
if __name__ == '__main__':
    main()