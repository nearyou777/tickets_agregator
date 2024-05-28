
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# from save_bd import Tickets
# from dotenv import load_dotenv
from config import Tickets, NewTickets, Users,SentMessage, engine
import os
from datetime import datetime, timedelta
# print((datetime.utcnow() + timedelta(days=7)).date())
# load_dotenv()
# engine = os.getenv('engine')
# engine = create_engine('sqlite:///tickets.db', echo=True)
# airports = ['zalupa', 'huy', 'pizda']
# Base = declarative_base()
# Session = sessionmaker(bind=engine)
# session = Session()
# user = session.query(Users).first()
# print(user.SubscriptionDate.date() > datetime.utcnow().date())
print(len("🤖 We find top flight deals globally, including economy, business, and first class, with cash or points. Hotels, cruises coming soon!"))
# user = session.query(Users).first()
# print(user.LogInDate.date() == datetime.utcnow().date())
# user = session.query(Users).filter(Users.IsActiveUser).first()
# print(user.Name)
# session.add(Users(ID='1234', Name='pidatas', Airports=', '.join(airports)))
# session.commit()
# session.close()
# Session = sessionmaker(bind=engine)
# session = Session()


# session.query(Tickets).filter(Tickets.DepartureAirports.like('%New York%')).delete(synchronize_session=False)
# session.query(SentMessage).delete(synchronize_session=False)
# session.commit()
# session.close()

# print((datetime.utcnow() + timedelta(days=7)).date())