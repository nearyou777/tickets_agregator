import logging
from time import sleep
from shared.rabit_config import get_connection, RMQ_ROUTING_KEY
from pomelo import add_pomelo
from thriftytraveler import add_thrifty
from going import add_going
from delete_offers import autodelete
from send_messages import produce_message, send_to_db
from email_scrapper import add_email

# Configure logging for both file and console
logging.basicConfig(level=logging.INFO)  # Ensure root logger is set to DEBUG
logger = logging.getLogger("scrape_data")

# Handlers
file_handler = logging.FileHandler("shared/scrape_data.log", mode='w')
stream_handler = logging.StreamHandler()

# Formatters
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

logger.propagate = True  # Optional: allows logs to propagate to root logger

def process_data(data):
    """
    Process and send data to the database and RabbitMQ.
    """
    for item in data:
        send_to_db(item)
        with get_connection() as connection:
            with connection.channel() as channel:
                produce_message(channel, RMQ_ROUTING_KEY, data=item)
                logger.info("Message sent to RabbitMQ with data: %s", item)

def scrape_data():
    """
    Main function to scrape data from various sources and process it.
    """
    logger.info("Scrape data function started")  # Test logging
    while True:
        try:
            data = add_thrifty()
            logger.info("Successfully scraped data from Thrifty Traveler")
        except Exception as e:
            logger.error("Error in add_thrifty: %s", e)
            data = None

        if not data:
            try:
                data = add_pomelo()
                logger.info("Successfully scraped data from Pomelo")
            except Exception as e:
                logger.error("Error in add_pomelo: %s", e)
                data = None

            if not data:
                try:
                    logger.info("Successfully scraped data from Going")
                except Exception as e:
                    logger.error("Error in add_going: %s", e)
                    data = None

            # if not data:
            #     try:
            #         data = add_email()
            #         logger.info("Successfully processed emails")
            #     except Exception as e:
            #         logger.error("Error in email processing: %s", e)
            #         data = None

            if not data:
                logger.info("No data found, triggering autodelete")
                autodelete()
                with get_connection() as connection:
                    with connection.channel() as channel:
                        produce_message(channel, RMQ_ROUTING_KEY, data={'Type': 'technical message'})
                        logger.info("Sent technical message to RabbitMQ")
                sleep(180)

        if data:
            logger.info("Data retrieved successfully, processing data")
            process_data(data)

def main():
    """
    Main entry point of the application.
    """
    logger.info("Service started, waiting for 25 seconds")
    sleep(25)
    
    with get_connection() as connection:
        with connection.channel() as channel:
            produce_message(channel, RMQ_ROUTING_KEY, data={'Type': 'technical message'})
            logger.info("Sent initial technical message to RabbitMQ")

    scrape_data()

if __name__ == '__main__':
    main()
