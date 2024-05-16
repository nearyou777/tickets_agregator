from sqlalchemy import create_engine, Column, Integer, ForeignKey, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from config import engine
# engine = create_engine('sqlite:///tickets.db', echo=True)

Base = declarative_base()

class Tickets(Base):
    __tablename__ = f'tickets'
    Primary_Key  = Column(Integer, primary_key=True)
    ID = Column(String(100))
    Title  = Column(String(500))
    Type = Column(String(200))
    Cabin = Column(String(500))
    Price = Column(String(50))
    Book = Column(String(1000))
    DepartureCities = Column(String(10000))
    DepartureAirports = Column(String(10000))


class NewTickets(Base):
    __tablename__ = f'new_tickets'
    Primary_Key  = Column(Integer, primary_key=True)
    ID = Column(String(100))
    Title  = Column(String(500))
    Type = Column(String(200))
    Cabin = Column(String(500))
    Price = Column(String(50))
    Book = Column(String(1000))
    DepartureCities = Column(String(10000))
    DepartureAirports = Column(String(10000))



# class Users(Base):
#     __tablename__ = 'users'
#     ID = Column(String(50), primary_key=True)
#     Name = Column(String(200))
#     Airports = Column(String(1000))

# Определяем модель для таблицы SentMessages
class SentMessage(Base):
    __tablename__ = 'sent_messages'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.ID'))
    message_id = Column(String(200))
    user = relationship("Users", back_populates="sent_messages")

# Определяем модель для таблицы Users
class Users(Base):
    __tablename__ = 'users'
    # id = Column(Integer, primary_key=True)
    ID = Column(Integer, primary_key=True)
    Name = Column(String(200))
    Airports = Column(String(10000))
    sent_messages = relationship("SentMessage", back_populates="user")
Base.metadata.create_all(engine)

# # Определяем модель для таблицы SentMessages
# class SentMessage(Base):
#     __tablename__ = 'sent_messages'
#     id = Column(Integer, primary_key=True)
#     user_id = Column(Integer, ForeignKey('users.id'))
#     message_id = Column(Integer)
#     user = relationship("Users", back_populates="sent_messages")

# # Определяем модель для таблицы Users
# class Users(Base):
#     __tablename__ = 'users'
#     id = Column(Integer, primary_key=True)
#     user_id = Column(String(50))
#     name = Column(String(200))
#     airports = Column(String(1000))
#     sent_messages = relationship("SentMessage", back_populates="user")
Session = sessionmaker(bind=engine)
session = Session()

session.query(NewTickets).delete()
session.commit()
session.close()
