import json
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from pika.adapters.blocking_connection import BlockingChannel
from shared.models import Session, Tickets

def send_to_db(item:dict):
    with Session() as session:
        exist = session.query(Tickets).filter_by(ID = item['ID']).first()
        if not exist:
            session.add(Tickets(**item))
            session.commit()


def produce_message(ch:"BlockingChannel", routing_key:str, data:dict):
    ch.queue_declare(queue=routing_key)
    msg = json.dumps(data)
    ch.basic_publish(
        exchange="",
        routing_key=routing_key,
        body=msg
    )


if __name__ == '__main__':
    pass