# Вибір базового образу
FROM python:3.11-slim

# Встановлюємо робочу директорію
WORKDIR /tickets

# Копіюємо файли requirements.txt
COPY requirements.txt ./

# Встановлюємо залежності
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо код парсера
COPY . .

# Вказуємо команду для запуску парсера
CMD ["python", "main.py"]
