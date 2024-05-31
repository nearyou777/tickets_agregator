from datetime import datetime

# Исходная строка даты
date_str = "2024-09-15T00:00:00.000Z"

# Преобразуем строку в объект datetime
date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")

# Получаем название месяца
month_name = date_obj.strftime("%B")
print(month_name)