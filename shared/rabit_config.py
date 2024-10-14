import pika
from dotenv import load_dotenv
import os

load_dotenv()
RMQ_ROUTING_KEY = os.getenv('RMQ_ROUTING_KEY')
connection_params = pika.ConnectionParameters(
    host=os.getenv('RMQ_HOST'),
    port=int(os.getenv('RMQ_PORT')),
    credentials=pika.PlainCredentials(username=os.getenv('RMQ_USER'), password=os.getenv('RMQ_PASSWORD')),
    heartbeat=180
)
def get_connection() -> pika.BlockingConnection:
    # return pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq', port=5672, credentials=pika.PlainCredentials('guest', 'guest'), heartbeat=180))
    return pika.BlockingConnection(parameters=connection_params)

if __name__ == '__main__':
    get_connection()
