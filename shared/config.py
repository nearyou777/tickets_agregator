from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, Column, Integer, ForeignKey, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime, timedelta
from shared.models import engine, Users, Session
import json
import logging

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)

def isadmin(user_id:int):
    for admin in [os.getenv('MY_ID'), os.getenv('VITALIY_ID'), os.getenv('MAKS_ID')]:
        if str(user_id) == str(admin):
            return True
    return False
    
def check_subscription(user_id):
    with Session() as session:
        user = session.query(Users).filter(Users.ID==user_id).first()
        return user.SubscriptionDate.date() >= datetime.utcnow().date() or user.BuyedSubscription

def escape_markdown(text):
    """
    Escape characters for proper MarkdownV2 formatting in Telegram.
    """
    escape_chars = r'_*[]()~`>#+-=|{}.!'
    return ''.join(['\\' + char if char in escape_chars else char for char in text])

def format_entities(text, entities):
    current_position = 0
    formatted_message_parts = []

    for entity in entities:
        offset = entity.offset
        length = entity.length
        entity_type = entity.type
        formatted_message_parts.append(escape_markdown(text[current_position:offset]))
        if entity_type == "bold":
            formatted_message_parts.append(f'*{escape_markdown(text[offset:offset+length])}*')
        elif entity_type == "italic":
            formatted_message_parts.append(f'_{escape_markdown(text[offset:offset+length])}_')
        elif entity_type == "code":
            formatted_message_parts.append(f'`{escape_markdown(text[offset:offset+length])}`')
        elif entity_type == "pre":
            formatted_message_parts.append(f'```{escape_markdown(text[offset:offset+length])}```')
        elif entity_type == "text_link":
            url = entity.url
            formatted_message_parts.append(f'[{escape_markdown(text[offset:offset+length])}]({escape_markdown(url)})')
        elif entity_type == "url":
            url = text[offset:offset+length]
            formatted_message_parts.append(f'[{escape_markdown(url)}]({escape_markdown(url)})')
        current_position = offset + length

    if current_position < len(text):
        formatted_message_parts.append(escape_markdown(text[current_position:]))

    return ''.join(formatted_message_parts)


with open('/tickets/shared/airports.json', 'r') as f:
    all_airports = json.load(f)