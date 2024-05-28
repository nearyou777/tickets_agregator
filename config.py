from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, Column, Integer, ForeignKey, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime, timedelta
load_dotenv()
engine = create_engine(os.getenv('connection_string'), echo=True)


Base = declarative_base()

class Tickets(Base):
    __tablename__ = f'tickets'
    Primary_Key  = Column(Integer, primary_key=True)
    ID = Column(String(100))
    Title  = Column(String(500))
    Type = Column(String(200))
    Cabin = Column(String(500))
    Price = Column(String(50))
    Book = Column(String(5000))
    DepartureCities = Column(String(10000))
    DepartureAirports = Column(String(10000))
    BookGuide = Column(String(10000))
    Summary = Column(String(10000))
    PictureName = Column(String(100))
    DateAdded = Column(DateTime, default=datetime.utcnow().date)


class NewTickets(Base):
    __tablename__ = f'new_tickets'
    Primary_Key  = Column(Integer, primary_key=True)
    ID = Column(String(100))
    Title  = Column(String(500))
    Type = Column(String(200))
    Cabin = Column(String(500))
    Price = Column(String(50))
    Book = Column(String(5000))
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

# class Channel(Base):
#     __tablename__ = 'channel'
#     ID = Column(Integer, primary_key=True)
#     # LastUpdate = Column(Str)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

session.query(NewTickets).delete()
session.commit()
session.close()

def isadmin(user_id:int):
    for admin in [os.getenv('my_id'), os.getenv('vitaliy_id'), os.getenv('maks_id')]:
        if str(user_id) == str(admin):
            return True
    return False

all_airports = [
    "Aberdeen (ABR)",
    "Abilene (ABI)",
    "Akron (CAK)",
    "Albany (ALB)",
    "Albuquerque (ABQ)",
    "Allentown (ABE)",
    "Anchorage (ANC)",
    "Appleton (ATW)",
    "Arcata–Eureka (ACV)",
    "Augusta (AGS)",
    "Austin (AUS)",
    "Asheville (AVL)",
    "Atlanta (ATL)",
    "Bakersfield (BFL)",
    "Baltimore (BWI)",
    "Bangor (BGR)",
    "Baton Rouge (BTR)",
    "Bemidji (BJI)",
    "Billings (BIL)",
    "Birmingham (BHM)",
    "Bismarck (BIS)",
    "Bloomington (BMI)",
    "Boise (BOI)",
    "Boston (BOS)",
    "Bozeman (BZN)",
    "Brainerd (BRD)",
    "Bristol (TRI)",
    "Buffalo (BUF)",
    "Burbank (BUR)",
    "Burlington (BTV)",
    "Butte (BTM)",
    "Calgary (YYC)",
    "Cedar Rapids (CID)",
    "Charleston (CHS)",
    "Charleston (CRW)",
    "Charlotte (CLT)",
    "Charlottesville (CHO)",
    "Chattanooga (CHA)",
    "Chicago (ORD)",
    "Chicago (MDW)",
    "Cincinnati (CVG)",
    "Cleveland (CLE)",
    "Colorado Springs (COS)",
    "Columbia (CAE)",
    "Columbia (COU)",
    "Columbus (CMH)",
    "Columbus (GTR)",
    "Corpus Christi (CRP)",
    "Dallas (DFW)",
    "Dallas (DAL)",
    "Dayton (DAY)",
    "Daytona Beach (DAB)",
    "Denver (DEN)",
    "Devils Lake (DVL)",
    "Destin (VPS)",
    "Detroit (DTW)",
    "Des Moines (DSM)",
    "Dickinson (DIK)",
    "Dothan (DHN)",
    "Dubuque (DBQ)",
    "Duluth (DLH)",
    "Eau Claire (EAU)",
    "Edmonton (YEG)",
    "El Paso (ELP)",
    "Erie (ERI)",
    "Eugene (EUG)",
    "Evansville (EVV)",
    "Fairbanks (FAI)",
    "Fargo (FAR)",
    "Fayetteville (FAY)",
    "Fayetteville (XNA)",
    "Flint (FNT)",
    "Fort Lauderdale (FLL)",
    "Fort Myers (RSW)",
    "Fort Wayne (FWA)",
    "Fresno (FAT)",
    "Gainesville (GNV)",
    "Grand Forks (GFK)",
    "Grand Junction (GJT)",
    "Grand Rapids (GRR)",
    "Great Falls (GTF)",
    "Green Bay (GRB)",
    "Greensboro (GSO)",
    "Greenville (GSP)",
    "Gulfport (GPT)",
    "Harrisburg (MDT)",
    "Hartford (BDL)",
    "Hibbing (HIB)",
    "Honolulu (HNL)",
    "Houston (IAH)",
    "Houston (HOU)",
    "Huntsville (HSV)",
    "Idaho Falls (IDA)",
    "Indianapolis (IND)",
    "International Falls (INL)",
    "Jackson (JAN)",
    "Jackson Hole (JAC)",
    "Jacksonville (JAX)",
    "Jamestown (JMS)",
    "Joplin (JLN)",
    "Juneau (JNU)",
    "Kalamazoo (AZO)",
    "Kalispell (FCA)",
    "Kansas City (MCI)",
    "Key West (EYW)",
    "Knoxville (TYS)",
    "Kona (KOA)",
    "La Crosse (LSE)",
    "Lafayette (LFT)",
    "Lansing (LAN)",
    "Las Vegas (LAS)",
    "Lexington (LEX)",
    "Little Rock (LIT)",
    "Lincoln (LNK)",
    "Louisville (SDF)",
    "Long Beach (LGB)",
    "Los Angeles (LAX)",
    "Lubbock (LBB)",
    "Madison (MSN)",
    "Manchester–Boston (MHT)",
    "McAllen (MFE)",
    "Medford (MFR)",
    "Melbourne (MLB)",
    "Memphis (MEM)",
    "Miami (MIA)",
    "Midland (MAF)",
    "Milwaukee (MKE)",
    "Minneapolis (MSP)",
    "Minot (MOT)",
    "Missoula (MSO)",
    "Mobile (MOB)",
    "Moline (MLI)",
    "Monterey (MRY)",
    "Montgomery (MGM)",
    "Montreal (YUL)",
    "Montrose (MTJ)",
    "Myrtle Beach (MYR)",
    "Nashville (BNA)",
    "New Orleans (MSY)",
    "New York (JFK)",
    "New York (LGA)",
    "Newark (EWR)",
    "Norfolk (ORF)",
    "Oakland (OAK)",
    "Oklahoma City (OKC)",
    "Omaha (OMA)",
    "Ontario (ONT)",
    "Orlando (MCO)",
    "Ottawa (YOW)",
    "Palm Springs (PSP)",
    "Panama City (ECP)",
    "Pasco (PSC)",
    "Pensacola (PNS)",
    "Peoria (PIA)",
    "Philadelphia (PHL)",
    "Phoenix (PHX)",
    "Pittsburgh (PIT)",
    "Pocatello (PIH)",
    "Portland (PDX)",
    "Portland (PWM)",
    "Providence (PVD)",
    "Quebec City (YQB)",
    "Raleigh (RDU)",
    "Rapid City (RAP)",
    "Redding (RDD)",
    "Redmond (RDM)",
    "Regina (YQR)",
    "Reno (RNO)",
    "Rhinelander (RHI)",
    "Richmond (RIC)",
    "Roanoke (ROA)",
    "Rochester (ROC)",
    "Rochester (RST)",
    "Salt Lake City (SLC)",
    "San Antonio (SAT)",
    "Sacramento (SMF)",
    "San Diego (SAN)",
    "San Jose (SJC)",
    "San Juan (SJU)",
    "San Francisco (SFO)",
    "San Luis Obispo (SBP)",
    "Santa Ana (SNA)",
    "Santa Barbara (SBA)",
    "Santa Fe (SAF)",
    "Sarasota (SRQ)",
    "Saskatoon (YXE)",
    "Savannah (SAV)",
    "Scranton (AVP)",
    "Seattle (SEA)",
    "Shreveport (SHV)",
    "Sioux City (SUX)",
    "Sioux Falls (FSD)",
    "South Bend (SBN)",
    "Spokane (GEG)",
    "Springfield (SGF)",
    "Springfield (SPI)",
    "St. Louis (STL)",
    "St. Thomas (STT)",
    "Steamboat Springs (HDN)",
    "Syracuse (SYR)",
    "Tallahassee (TLH)",
    "Tampa (TPA)",
    "Thunder Bay (YQT)",
    "Toledo (TOL)",
    "Toronto (YYZ)",
    "Traverse City (TVC)",
    "Tucson (TUS)",
    "Tulsa (TUL)",
    "Vancouver (YVR)",
    "Victoria (YYJ)",
    "Waco (ACT)",
    "Washington, D.C. (DCA)",
    "Washington, D.C. (IAD)",
    "Watertown (ATY)",
    "Westchester County (HPN)",
    "Wichita (ICT)",
    "Wichita Falls (SPS)",
    "Williston (XWA)",
    "Wilmington (ILM)",
    "Winnipeg (YWG)",
    "Wausau (CWA)",
    "West Palm Beach (PBI)"
]
