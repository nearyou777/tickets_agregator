import telebot
from time import sleep
from telebot import types
from bot import bot
from dotenv import load_dotenv
import os
from models import Tickets, SentMessage, Session, Users
load_dotenv()
my_id = os.getenv('my_id')

from PIL import Image
import os


import re
import logging

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
from datetime import datetime, timedelta
import re
one_day_ago = datetime.now() - timedelta(days=1)
# def fix_markdown(text):
#     # Удаление лишних звездочек в конце строк, не трогая обрамляющие текст
#     text = re.sub(r'(\S)\*(?!\w)', r'\1', text)
    
#     # Исправление выделения текста (курсив/жирный)
#     text = re.sub(r'\*(\S.*?)\*(?!\*)', r'*\1*', text)
#     text = re.sub(r'_(\S.*?)_(?!_)', r'_\1_', text)

#     # Исправление списков (добавление пробела после звезды)
#     text = re.sub(r'\n\*([^\s])', r'\n* \1', text)
    
#     return text

# # Ваш текст
# text = """*LAS > San Francisco, California $97 Round Trip!!*✈️
# Basic Economy
# -----------------------
# $97 (was $200+)
# -----------------------
# August  - November 2024
# -----------------------
# ORDER BY: Cash
# -----------------------
# Departure cities:

# Las Vegas, Nevada (LAS) — Large - $97

# San Francisco (SFO) - $745*"""

# # Исправление текста
# fixed_text = fix_markdown(text)

# print(fixed_text)
# def reduce_image_size(input_path, output_path):
#     # Максимальный размер в байтах
#     max_size_bytes = 1024 * 1024
    
#     # Открываем изображение
#     with Image.open(input_path) as img:
#         # Получаем исходные размеры изображения
#         width, height = img.size
        
#         # Сначала сохраняем изображение с исходным разрешением и качеством
#         img.save(output_path, optimize=True, quality=95)
#         final_size = os.path.getsize(output_path)
        
#         # Проверяем размер файла и уменьшаем разрешение до достижения нужного размера
#         while final_size > max_size_bytes:
#             # Уменьшаем разрешение на 10%
#             width = int(width * 0.9)
#             height = int(height * 0.9)
#             img = img.resize((width, height), Image.LANCZOS)
            
#             # Сохраняем изображение с уменьшенным разрешением
#             img.save(output_path, optimize=True, quality=95)
#             final_size = os.path.getsize(output_path)
        

# # Пример использования функции
# input_path = 'imgs/01HZFEWPDDA3T17NXD8R5QHSJG.avif'
# output_path = 'imgs/01HZG2QH1CVREC24ASE0W7V8XP.jpg'
# # reduce_image_size(input_path, output_path)

# with open(output_path, 'rb') as f:
#     bot.send_photo(my_id,f)
# input_path = r'imgs/01HZFEZFBCRFVDQWVSJ2AKX8TJ.jpg'
# with Image.open(input_path) as img:
#     img.size
# import tls_client
# import requests
# s = tls_client.Session(client_identifier='chrome_105')
# headers = {
#     'Upgrade-Insecure-Requests': '1',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
#     'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
#     'sec-ch-ua-mobile': '?0',
#     'sec-ch-ua-platform': '"Windows"',
# }
# from sqlalchemy.orm import aliased

# date = (datetime.utcnow() - timedelta(days=10)).date()
# print(date)
# with Session() as session:
#     # a = session.query(Tickets).all()
#     #2024-06-08 < #2024-06-17
#     #17 - today
#     a = session.query(Tickets).filter(Tickets.DateAdded >= date).first()
#     print(a.Title, a.DateAdded)
#     # for row in a:
#     #     print(row.Title)
#     session.commit()
# a = ' 2'
# print(int(a))
# models.py
from sqlalchemy import create_engine, Column, Integer, ForeignKey, String, DateTime, Boolean, BigInteger, Table,text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import logging
from sqlalchemy import MetaData
from sqlalchemy import DDL


load_dotenv()
# engine = create_engine(os.getenv('connection_string'), echo=True, pool_size=20, max_overflow=20, pool_timeout=30, pool_recycle=3600)
# Создание метаданных и загрузка существующей таблицы
# Создание метаданных и загрузка существующей таблицы
# with engine.connect() as conn:
#     conn.execute(text('ALTER TABLE public.users ADD COLUMN filtered_offers VARCHAR(50) DEFAULT \'Both\''))
# r = requests.get('https://d3mdkiyq6mk8lq.cloudfront.net/images/deals/01HZFEZFBCRFVDQWVSJ2AKX8TJ.jpg', headers=headers,)
# print(r)
# import math
# print(math.ceil(7.05))
# print(round(7.05))
# import json
# all_airports = [
#     "Aberdeen (ABR)",
#     "Abilene (ABI)",
#     "Akron (CAK)",
#     "Albany (ALB)",
#     "Albuquerque (ABQ)",
#     "Allentown (ABE)",
#     "Anchorage (ANC)",
#     "Appleton (ATW)",
#     "Arcata–Eureka (ACV)",
#     "Augusta (AGS)",
#     "Austin (AUS)",
#     "Asheville (AVL)",
#     "Atlanta (ATL)",
#     "Bakersfield (BFL)",
#     "Baltimore (BWI)",
#     "Bangor (BGR)",
#     "Baton Rouge (BTR)",
#     "Bemidji (BJI)",
#     "Billings (BIL)",
#     "Birmingham (BHM)",
#     "Bismarck (BIS)",
#     "Bloomington (BMI)",
#     "Boise (BOI)",
#     "Boston (BOS)",
#     "Bozeman (BZN)",
#     "Brainerd (BRD)",
#     "Bristol (TRI)",
#     "Buffalo (BUF)",
#     "Burbank (BUR)",
#     "Burlington (BTV)",
#     "Butte (BTM)",
#     "Calgary (YYC)",
#     "Cedar Rapids (CID)",
#     "Charleston (CHS)",
#     "Charleston (CRW)",
#     "Charlotte (CLT)",
#     "Charlottesville (CHO)",
#     "Chattanooga (CHA)",
#     "Chicago (ORD)",
#     "Chicago (MDW)",
#     "Cincinnati (CVG)",
#     "Cleveland (CLE)",
#     "Colorado Springs (COS)",
#     "Columbia (CAE)",
#     "Columbia (COU)",
#     "Columbus (CMH)",
#     "Columbus (GTR)",
#     "Corpus Christi (CRP)",
#     "Dallas (DFW)",
#     "Dallas (DAL)",
#     "Dayton (DAY)",
#     "Daytona Beach (DAB)",
#     "Denver (DEN)",
#     "Devils Lake (DVL)",
#     "Destin (VPS)",
#     "Detroit (DTW)",
#     "Des Moines (DSM)",
#     "Dickinson (DIK)",
#     "Dothan (DHN)",
#     "Dubuque (DBQ)",
#     "Duluth (DLH)",
#     "Eau Claire (EAU)",
#     "Edmonton (YEG)",
#     "El Paso (ELP)",
#     "Erie (ERI)",
#     "Eugene (EUG)",
#     "Evansville (EVV)",
#     "Fairbanks (FAI)",
#     "Fargo (FAR)",
#     "Fayetteville (FAY)",
#     "Fayetteville (XNA)",
#     "Flint (FNT)",
#     "Fort Lauderdale (FLL)",
#     "Fort Myers (RSW)",
#     "Fort Wayne (FWA)",
#     "Fresno (FAT)",
#     "Gainesville (GNV)",
#     "Grand Forks (GFK)",
#     "Grand Junction (GJT)",
#     "Grand Rapids (GRR)",
#     "Great Falls (GTF)",
#     "Green Bay (GRB)",
#     "Greensboro (GSO)",
#     "Greenville (GSP)",
#     "Gulfport (GPT)",
#     "Harrisburg (MDT)",
#     "Hartford (BDL)",
#     "Hibbing (HIB)",
#     "Honolulu (HNL)",
#     "Houston (IAH)",
#     "Houston (HOU)",
#     "Huntsville (HSV)",
#     "Idaho Falls (IDA)",
#     "Indianapolis (IND)",
#     "International Falls (INL)",
#     "Jackson (JAN)",
#     "Jackson Hole (JAC)",
#     "Jacksonville (JAX)",
#     "Jamestown (JMS)",
#     "Joplin (JLN)",
#     "Juneau (JNU)",
#     "Kalamazoo (AZO)",
#     "Kalispell (FCA)",
#     "Kansas City (MCI)",
#     "Key West (EYW)",
#     "Knoxville (TYS)",
#     "Kona (KOA)",
#     "La Crosse (LSE)",
#     "Lafayette (LFT)",
#     "Lansing (LAN)",
#     "Las Vegas (LAS)",
#     "Lexington (LEX)",
#     "Little Rock (LIT)",
#     "Lincoln (LNK)",
#     "Louisville (SDF)",
#     "Long Beach (LGB)",
#     "Los Angeles (LAX)",
#     "Lubbock (LBB)",
#     "Madison (MSN)",
#     "Manchester–Boston (MHT)",
#     "McAllen (MFE)",
#     "Medford (MFR)",
#     "Melbourne (MLB)",
#     "Memphis (MEM)",
#     "Miami (MIA)",
#     "Midland (MAF)",
#     "Milwaukee (MKE)",
#     "Minneapolis (MSP)",
#     "Minot (MOT)",
#     "Missoula (MSO)",
#     "Mobile (MOB)",
#     "Moline (MLI)",
#     "Monterey (MRY)",
#     "Montgomery (MGM)",
#     "Montreal (YUL)",
#     "Montrose (MTJ)",
#     "Myrtle Beach (MYR)",
#     "Nashville (BNA)",
#     "New Orleans (MSY)",
#     "New York (JFK)",
#     "New York (LGA)",
#     "Newark (EWR)",
#     "Norfolk (ORF)",
#     "Oakland (OAK)",
#     "Oklahoma City (OKC)",
#     "Omaha (OMA)",
#     "Ontario (ONT)",
#     "Orlando (MCO)",
#     "Ottawa (YOW)",
#     "Palm Springs (PSP)",
#     "Panama City (ECP)",
#     "Pasco (PSC)",
#     "Pensacola (PNS)",
#     "Peoria (PIA)",
#     "Philadelphia (PHL)",
#     "Phoenix (PHX)",
#     "Pittsburgh (PIT)",
#     "Pocatello (PIH)",
#     "Portland (PDX)",
#     "Portland (PWM)",
#     "Providence (PVD)",
#     "Quebec City (YQB)",
#     "Raleigh (RDU)",
#     "Rapid City (RAP)",
#     "Redding (RDD)",
#     "Redmond (RDM)",
#     "Regina (YQR)",
#     "Reno (RNO)",
#     "Rhinelander (RHI)",
#     "Richmond (RIC)",
#     "Roanoke (ROA)",
#     "Rochester (ROC)",
#     "Rochester (RST)",
#     "Salt Lake City (SLC)",
#     "San Antonio (SAT)",
#     "Sacramento (SMF)",
#     "San Diego (SAN)",
#     "San Jose (SJC)",
#     "San Juan (SJU)",
#     "San Francisco (SFO)",
#     "San Luis Obispo (SBP)",
#     "Santa Ana (SNA)",
#     "Santa Barbara (SBA)",
#     "Santa Fe (SAF)",
#     "Sarasota (SRQ)",
#     "Saskatoon (YXE)",
#     "Savannah (SAV)",
#     "Scranton (AVP)",
#     "Seattle (SEA)",
#     "Shreveport (SHV)",
#     "Sioux City (SUX)",
#     "Sioux Falls (FSD)",
#     "South Bend (SBN)",
#     "Spokane (GEG)",
#     "Springfield (SGF)",
#     "Springfield (SPI)",
#     "St. Louis (STL)",
#     "St. Thomas (STT)",
#     "Steamboat Springs (HDN)",
#     "Syracuse (SYR)",
#     "Tallahassee (TLH)",
#     "Tampa (TPA)",
#     "Thunder Bay (YQT)",
#     "Toledo (TOL)",
#     "Toronto (YYZ)",
#     "Traverse City (TVC)",
#     "Tucson (TUS)",
#     "Tulsa (TUL)",
#     "Vancouver (YVR)",
#     "Victoria (YYJ)",
#     "Waco (ACT)",
#     "Washington, D.C. (DCA)",
#     "Washington, D.C. (IAD)",
#     "Watertown (ATY)",
#     "Westchester County (HPN)",
#     "Wichita (ICT)",
#     "Wichita Falls (SPS)",
#     "Williston (XWA)",
#     "Wilmington (ILM)",
#     "Winnipeg (YWG)",
#     "Wausau (CWA)",
#     "West Palm Beach (PBI)"
# ]
# count = 0
# with open('pomelo_airports.json', 'r') as f:
#     for item in json.load(f)['data']:
#         if 'New York' in item['city']:
#             continue
#         if f"{item['city']} ({item['IATA']})" not in all_airports :
#             count += 1
#             all_airports.append(f"{item['city']} ({item['IATA']})")

# print(count)
# with open('airports.json', 'w') as f:
#     json.dump(sorted(all_airports),f,indent=2)


# bot.send_message(my_id, 'Arcata\u2013Eureka')


# a = [4,56,67,893,1,2,5,6,8]
# a.sort()
# print(a)
a = (0.33**3) - 1.67 * (1-0.33)
print(a)