# models.py
from sqlalchemy import create_engine, Column, Integer, ForeignKey, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()
engine = create_engine(os.getenv('connection_string'), echo=True, pool_size=20, max_overflow=20, pool_timeout=30,  pool_recycle=3600)

Base = declarative_base()

class Tickets(Base):
    __tablename__ = 'tickets'
    #FIXME:
    Primary_Key  = Column(Integer, primary_key=True)
    ID = Column(String(100))
    Title  = Column(String(500))
    Type = Column(String(200))
    Cabin = Column(String(500))
    Price = Column(String(50))
    OriginalPrice = Column(String(50))
    Dates = Column(String(200))
    Book = Column(String(1000))
    DepartureCities = Column(String(10000))
    DepartureAirports = Column(String(10000))
    BookGuide = Column(String(10000))
    Summary = Column(String(10000))
    PictureName = Column(String(100))
    DateAdded = Column(DateTime, default=datetime.utcnow().date)


class NewTickets(Base):
    __tablename__ = 'new_tickets'
    #FIXME:
    Primary_Key  = Column(Integer, primary_key=True)
    ID = Column(String(100))
    Title  = Column(String(500))
    Type = Column(String(200))
    Cabin = Column(String(500))
    Price = Column(String(50))
    OriginalPrice = Column(String(50))
    Dates = Column(String(200))
    Book = Column(String(1000))
    DepartureCities = Column(String(10000))
    DepartureAirports = Column(String(10000))
    BookGuide = Column(String(10000))
    Summary = Column(String(10000))
    PictureName = Column(String(100))


class SentMessage(Base):
    __tablename__ = 'sent_messages'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.ID'))
    message_id = Column(String(200))
    user = relationship("Users", back_populates="sent_messages")


class Users(Base):
    __tablename__ = 'users'
    ID = Column(Integer, primary_key=True)
    Name = Column(String(200))
    Email = Column(String(200))
    Airports = Column(String(10000))
    LogInDate = Column(DateTime, default=datetime.utcnow().date)
    SubscriptionDate = Column(DateTime, default=(datetime.utcnow() + timedelta(days=7)).date)
    BuyedSubscription = Column(Boolean, default=False)
    IsActiveUser = Column(Boolean, default=True)
    sent_messages = relationship("SentMessage", back_populates="user")
Base.metadata.create_all(engine)



Session = sessionmaker(bind=engine)
session = Session()

session.query(NewTickets).delete()
session.commit()
session.close()