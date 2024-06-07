import telebot
from time import sleep
from telebot import types
from bot import bot
from dotenv import load_dotenv
import os

load_dotenv()

my_id = os.getenv('my_id')

from PIL import Image
import os


import re

import re

def fix_markdown(text):
    # Удаление лишних звездочек в конце строк, не трогая обрамляющие текст
    text = re.sub(r'(\S)\*(?!\w)', r'\1', text)
    
    # Исправление выделения текста (курсив/жирный)
    text = re.sub(r'\*(\S.*?)\*(?!\*)', r'*\1*', text)
    text = re.sub(r'_(\S.*?)_(?!_)', r'_\1_', text)

    # Исправление списков (добавление пробела после звезды)
    text = re.sub(r'\n\*([^\s])', r'\n* \1', text)
    
    return text

# Ваш текст
text = """*LAS > San Francisco, California $97 Round Trip!!*✈️
Basic Economy
-----------------------
$97 (was $200+)
-----------------------
August  - November 2024
-----------------------
ORDER BY: Cash
-----------------------
Departure cities:

Las Vegas, Nevada (LAS) — Large - $97

San Francisco (SFO) - $745*"""

# Исправление текста
fixed_text = fix_markdown(text)

print(fixed_text)
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

# r = requests.get('https://d3mdkiyq6mk8lq.cloudfront.net/images/deals/01HZFEZFBCRFVDQWVSJ2AKX8TJ.jpg', headers=headers,)
# print(r)