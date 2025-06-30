import openpyxl
import json
import re
import os

FILENAME = 'your_file.xlsx'

CATEGORIES = {
    "CPU": "Процессор",
    "Motherboard": "Материнская плата",
    "SSD": "Накопитель SSD",
    "RAM": "Память DDR",
    "Case": "Корпус",
    "PSU": "Блок питания",
    "GPU": "Видеокарта"
}

SOCKET_PATTERNS = [
    r"LGA\s?-?\d{3,4}\w*",      # LGA1151, LGA1151v2
    r"Soc\s?-?\d{3,4}\w*",     # Soc-1151, Soc-1151v2
    r"Socket\s?\w+",            # Socket AM4, Socket FM2+
    r"AM\d",                     # AM4
    r"FM\d",                     # FM2
    r"sTRX\w*",
    r"sTRX\s?\w*",
    r"TRX\w*",
    r"sWRX\w*",
    r"sWRX\s?\w*"
]

RAM_TYPE_PATTERNS = [
    r"DDR2",
    r"DDR-III",
    r"DDR3",
    r"DDR4",
    r"DDR5"
]


def find_pattern(patterns, text):
    for pat in patterns:
        match = re.search(pat, text)
        if match:
            return match.group(0)
    return ""


def extract_storage_capacity(name: str) -> dict:
    """Извлекает объем накопителя из названия"""
    name_upper = name.upper()
    
    # Паттерны для поиска объема
    capacity_patterns = [
        r'(\d+(?:\.\d+)?)\s*(GB|ГБ|TB|ТБ|MB|МБ)',  # 256GB, 1TB, 512 ГБ, 2 ТБ
        r'(\d+(?:\.\d+)?)\s*(GB|ГБ|TB|ТБ|MB|МБ)',  # 256 GB, 1 TB
    ]
    
    for pattern in capacity_patterns:
        match = re.search(pattern, name_upper)
        if match:
            value = float(match.group(1))
            unit = match.group(2).upper()
            
            # Конвертируем в GB
            if unit in ['TB', 'ТБ']:
                capacity_gb = value * 1024
            elif unit in ['MB', 'МБ']:
                capacity_gb = value / 1024
            else:  # GB, ГБ
                capacity_gb = value
            
            return {
                "capacity_gb": round(capacity_gb, 2),
                "capacity_raw": f"{value}{unit}"
            }
    
    return {
        "capacity_gb": None,
        "capacity_raw": None
    }


def extract_ram_capacity(name: str) -> dict:
    """Извлекает объем памяти из названия модуля RAM"""
    name_upper = name.upper()
    
    # Паттерны для поиска объема памяти (обычно в MB/GB)
    capacity_patterns = [
        r'(\d+(?:\.\d+)?)\s*(GB|ГБ|MB|МБ)',  # 8GB, 16 ГБ, 512MB, 1024 МБ
        r'(\d+(?:\.\d+)?)\s*(GB|ГБ|MB|МБ)',  # 8 GB, 16 ГБ
    ]
    
    for pattern in capacity_patterns:
        match = re.search(pattern, name_upper)
        if match:
            value = float(match.group(1))
            unit = match.group(2).upper()
            
            # Конвертируем в GB
            if unit in ['MB', 'МБ']:
                capacity_gb = value / 1024
            else:  # GB, ГБ
                capacity_gb = value
            
            return {
                "capacity_gb": round(capacity_gb, 2),
                "capacity_raw": f"{value}{unit}"
            }
    
    return {
        "capacity_gb": None,
        "capacity_raw": None
    }


def extract_motherboard_info(name):
    """Извлекает информацию о слотах RAM и типе памяти из названия материнской платы"""
    name_upper = name.upper()

    # Ищем паттерны типа "4xDDR4", "2xDDR5", "DDR4x4" и т.д.
    ram_slots_patterns = [
        r"(\d+)X?DDR(\d)",  # 4XDDR4, 2xDDR5
        r"DDR(\d)X(\d)",  # DDR4x4, DDR5x2
        r"(\d+)DDR(\d)",  # 4DDR4, 2DDR5
        r"DDR(\d)\s*(\d+)",  # DDR4 4, DDR5 2
    ]

    ram_type = ""
    ram_slots = 2  # По умолчанию 2 слота

    # Сначала ищем тип памяти
    for pattern in RAM_TYPE_PATTERNS:
        if re.search(pattern, name_upper):
            ram_type = pattern
            break

    # Затем ищем количество слотов
    for pattern in ram_slots_patterns:
        match = re.search(pattern, name_upper)
        if match:
            if len(match.groups()) == 2:
                # Если найдено два числа, первое - слоты, второе - тип DDR
                slots = int(match.group(1))
                ddr_type = f"DDR{match.group(2)}"
                if ddr_type == ram_type or not ram_type:  # Проверяем совпадение типа
                    ram_slots = slots
                    ram_type = ddr_type
                    break
            else:
                # Если найдено одно число, это количество слотов
                ram_slots = int(match.group(1))
                break

    return {
        "ram_type": ram_type,
        "ram_slots": ram_slots
    }


def parse_ram_modules_in_kit(ram_name: str) -> int:
    # Ищем паттерн типа 2x, 4x, 1x в любом месте строки
    match = re.search(r'(\d+)x', ram_name, re.IGNORECASE)
    if match:
        return int(match.group(1))
    return 1


def normalize_socket(socket_str):
    if not socket_str:
        return ""
    # Не обрезаем суффиксы типа v2, просто убираем лишние пробелы и приводим к верхнему регистру
    s = socket_str.strip().replace("-", "-").replace(" ", " ")
    return s.upper()


def parse_power(name: str) -> int:
    # Ищем паттерны мощности: 350W, 350 W, 350Вт, 350 Вт, 350+W, 350+Вт, 350W+, 350Вт+ и т.д.
    # Поддерживаем любые (или отсутствие) нецифровые символы между числом и W/Вт
    # Добавляем поддержку английской буквы W
    patterns = [
        r'(\d{3,4})\D*([wв][тt])',  # 350Вт, 350 Вт, 350Wт и т.д.
        r'(\d{3,4})\D*W',  # 350W, 350 W и т.д.
    ]
    
    for pattern in patterns:
        match = re.search(pattern, name, re.IGNORECASE)
        if match:
            return int(match.group(1))
    return 0


def extract_power_from_name(name: str) -> int | None:
    match = re.search(r'(1[5-9][0-9]|[2-9][0-9]{2}|[12][0-9]{3}|3000)\D', name)
    if match:
        digits = re.match(r'\d+', match.group(0))
        if digits:
            value = int(digits.group(0))
            if 150 <= value <= 3000:
                return value
    return None


def extract_ram_size(name: str) -> str:
    """Определяет размер модуля памяти: SODIMM или DIMM"""
    name_upper = name.upper()
    
    # Ищем SODIMM в различных вариантах написания
    sodimm_patterns = [
        r'SO\s*DIMM',
        r'SODIMM',
        r'SO-DIMM'
    ]
    
    for pattern in sodimm_patterns:
        if re.search(pattern, name_upper):
            return "SODIMM"
    
    # Если SODIMM не найден, то это DIMM
    return "DIMM"


def extract_ram_type(name: str) -> str:
    """Извлекает тип RAM из названия с обработкой частных случаев"""
    name_upper = name.upper()
    
    # Специальные случаи
    if "DDR2" in name_upper:
        return "DDR2"
    if "DDR-III" in name_upper:
        return "DDR3"
    
    # Обычные паттерны
    for pattern in RAM_TYPE_PATTERNS:
        match = re.search(pattern, name_upper)
        if match:
            return match.group(0)
    
    return ""


wb = openpyxl.load_workbook(FILENAME)
ws = wb.active

components = {cat: [] for cat in CATEGORIES}

for row in ws.iter_rows(min_row=2):
    code = str(row[0].value or "").strip()  # Поле 1 - код
    name = str(row[1].value or "")
    price = row[6].value
    article = str(row[2].value or "").strip()  # Поле 3 - артикул
    field5 = str(row[4].value or "")
    if "есть" not in field5.lower():
        continue

    for cat, keyword in CATEGORIES.items():
        if name.startswith(keyword):
            # Специальная проверка для блоков питания - только те, что начинаются со слов "Блок питания" и содержат ATX
            if cat == "PSU":
                if not name.startswith("Блок питания"):
                    continue
                if not re.search(r"atx", name, re.IGNORECASE):
                    continue
                item = {
                    "name": name.strip(), 
                    "price": price if price is not None else 0, 
                    "atx": True,
                    "code": code,
                    "article": article
                }
                power = extract_power_from_name(name)
                if power:
                    item["power"] = power
            elif cat == "Case" and (re.search(r"майн", name, re.IGNORECASE) or re.search(r"внеш", name, re.IGNORECASE)):
                continue
            # --- Парсинг мощности ---
            elif cat == "Case":
                power = parse_power(name)
                if power > 0:
                    item = {
                        "name": name.strip(), 
                        "price": price if price is not None else 0, 
                        "power": power,
                        "code": code,
                        "article": article
                    }
                else:
                    item = {
                        "name": name.strip(), 
                        "price": price if price is not None else 0, 
                        "power": None,
                        "code": code,
                        "article": article
                    }
            else:
                item = {
                    "name": name.strip(), 
                    "price": price if price is not None else 0,
                    "code": code,
                    "article": article
                }
            
            # Извлечение объема для накопителей SSD
            if cat == "SSD":
                capacity_info = extract_storage_capacity(name)
                if capacity_info["capacity_gb"]:
                    item["capacity_gb"] = capacity_info["capacity_gb"]
                    item["capacity_raw"] = capacity_info["capacity_raw"]
            
            # Извлечение объема для модулей RAM
            if cat == "RAM":
                capacity_info = extract_ram_capacity(name)
                if capacity_info["capacity_gb"]:
                    item["capacity_gb"] = capacity_info["capacity_gb"]
                    item["capacity_raw"] = capacity_info["capacity_raw"]
                item["size"] = extract_ram_size(name)
            
            # Автоматически ищем сокет и тип памяти в наименовании
            if cat in ["CPU", "Motherboard"]:
                raw_socket = find_pattern(SOCKET_PATTERNS, name)
                item["socket"] = normalize_socket(raw_socket)
                if cat == "Motherboard" and not item["socket"]:
                    item["integrated_cpu"] = True
            if cat in ["Motherboard", "RAM"]:
                item["ram_type"] = extract_ram_type(name)
            if cat == "RAM":
                item["modules_in_kit"] = parse_ram_modules_in_kit(name)
            if cat == "Motherboard":
                mb_info = extract_motherboard_info(name)
                if mb_info["ram_type"]:
                    item["ram_type"] = mb_info["ram_type"]
                item["ram_slots"] = mb_info["ram_slots"]
            components[cat].append(item)

# Сохраняем файл только один раз после цикла!
output_json = "components.json"
with open(output_json, 'w', encoding='utf-8') as f:
    json.dump(components, f, ensure_ascii=False, indent=2)
print(f"Готово! Файл {output_json} создан.")

print("Готово! Файл components.json создан.")
print("\nПримеры извлеченной информации:")
for item in components.get("Motherboard", [])[:3]:
    print(f"- {item['name']}")
    print(f"  Код: {item.get('code', 'Не указан')}")
    print(f"  Артикул: {item.get('article', 'Не указан')}")
    print(f"  RAM: {item.get('ram_type', 'Не указан')} x {item.get('ram_slots', 2)} слотов")
    print(f"  Socket: {item.get('socket', 'Не указан')}")
    print()

print("\nПримеры SSD с объемом:")
for item in components.get("SSD", [])[:3]:
    print(f"- {item['name']}")
    print(f"  Код: {item.get('code', 'Не указан')}")
    print(f"  Артикул: {item.get('article', 'Не указан')}")
    print(f"  Объем: {item.get('capacity_raw', 'Не указан')} ({item.get('capacity_gb', 'Не указан')} GB)")
    print()

print("\nПримеры RAM с объемом:")
for item in components.get("RAM", [])[:3]:
    print(f"- {item['name']}")
    print(f"  Код: {item.get('code', 'Не указан')}")
    print(f"  Артикул: {item.get('article', 'Не указан')}")
    print(f"  Объем: {item.get('capacity_raw', 'Не указан')} ({item.get('capacity_gb', 'Не указан')} GB)")
    print() 