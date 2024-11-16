from sqlalchemy import create_engine, Column, Integer, ForeignKey, String, DateTime, Boolean, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import logging
from sqlalchemy.ext.mutable import MutableList
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import uuid
load_dotenv()

db_connection_string = os.getenv('DB_CONNECTION_STRING')

engine = create_engine(db_connection_string, echo=False, pool_size=20, max_overflow=20, pool_timeout=30, pool_recycle=3600)

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

Base = declarative_base()

class Tickets(Base):
    __tablename__ = 'tickets'
    ID = Column(String(500), primary_key=True, default=lambda: str(uuid.uuid4()))
    Title = Column(String(500))
    Type = Column(String(200))
    Cabin = Column(String(500))
    Price = Column(String(50))
    OriginalPrice = Column(String(50))
    Dates = Column(String(1000))
    Book = Column(String(5000))
    DepartureCities = Column(String(10000))
    DepartureAirports = Column(String(10000))
    BookGuide = Column(String(10000))
    Summary = Column(String(10000))
    PictureName = Column(String(100))
    DateAdded = Column(DateTime, default=datetime.utcnow)

class Users(Base):
    __tablename__ = 'users'
    ID = Column(BigInteger, primary_key=True)
    Name = Column(String(200))
    Email = Column(String(200))
    Airports = Column(String(10000))
    LogInDate = Column(DateTime, default=datetime.utcnow)
    SubscriptionDate = Column(DateTime, default=(datetime.utcnow() + timedelta(days=7)))
    BuyedSubscription = Column(Boolean, default=False)
    IsActiveUser = Column(Boolean, default=True)
    filtered_offers = Column(String(50), default='Both')
    wishlists = relationship("Wishlist", back_populates="user")  
    sent_messages = relationship("SentMessage", back_populates="user")
    wishlists = relationship("Wishlist", back_populates="user")

class SentMessage(Base):
    __tablename__ = 'sent_messages'
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, ForeignKey('users.ID'))
    message_id = Column(String(200))
    user = relationship("Users", back_populates="sent_messages")

class Wishlist(Base):
    __tablename__ = 'wishlists'
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, ForeignKey('users.ID'))
    destination_country = Column(String(1000)) 

    # min_price = Column(String(50))  # Минимальная цена
    # max_price = Column(String(50))  # Максимальная цена
    # date_from = Column(DateTime)  # Дата начала поиска
    # date_to = Column(DateTime)  # Дата окончания поиска
    
    user = relationship("Users", back_populates="wishlists")
    wishlist_offers = relationship("WishlistOffers", back_populates="wishlist")

class WishlistOffers(Base):
    __tablename__ = 'wishlist_offers'
    id = Column(Integer, primary_key=True)
    wishlist_id = Column(Integer, ForeignKey('wishlists.id'))
    ticket_id = Column(String(1000), ForeignKey('tickets.ID'))
    # found_date = Column(DateTime, default=datetime.utcnow)
    
    # Связь с вишлистом и тикетами
    wishlist = relationship("Wishlist", back_populates="wishlist_offers")
    ticket = relationship("Tickets")


class AdminUser(Base, UserMixin):  # Наследуемся от UserMixin
    __tablename__ = 'admin_users'
    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True)
    password = Column(String(255))  
    is_superuser = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True) 

    def get_id(self):
        return str(self.id)

    # Логика для проверки аутентификации
    @property
    def is_authenticated(self):
        return self.is_active  # или любое другое условие для аутентификации

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
