import json
import re
import csv
from typing import List, Dict, Any, Optional

def extract_model_name(name: str) -> str:
    """Извлекает название модели из полного названия видеокарты и нормализует суффиксы (SUPER, TI, XT) с пробелом"""
    if not name:
        return ""
    name = name.lower()
    name = re.sub(r'\s+', ' ', name).strip()
    
    print(f"Обрабатываем: '{name}'")
    
    # Паттерн: вставить пробел перед суффиксами, если его нет
    name = re.sub(r'(\d)(super|ti|xt|m)\b', r'\1 \2', name)
    
    # Специальная обработка для названий в скобках (артикулы)
    if name.startswith('(') and name.endswith(')'):
        print("  Найдено название в скобках")
        # Ищем модель в артикуле, например: TUF 3-GTX1660S-O6G-GAMING
        bracket_patterns = [
            r'gtx\s*(\d+)\s*(super|ti|xt|s)?',
            r'rtx\s*(\d+)\s*(super|ti|xt|s)?',
            r'gt\s*(\d+)',
            r'rx\s*(\d+)\s*(xt)?',
            r'hd\s*(\d+)',
            r'(\d+)\s*(super|ti|xt|s)?',
            # Паттерны без пробела между числом и суффиксом
            r'gtx\s*(\d+)(super|ti|xt|s)\b',
            r'rtx\s*(\d+)(super|ti|xt|s)\b',
            r'(\d+)(super|ti|xt|s)\b'
        ]
        for i, pattern in enumerate(bracket_patterns):
            match = re.search(pattern, name)
            if match:
                number = match.group(1)
                suffix = match.group(2) if len(match.groups()) > 1 else ""
                print(f"    Паттерн {i}: {pattern}")
                print(f"    Найдено: number='{number}', suffix='{suffix}'")
                if suffix:
                    # Преобразуем 'S' в 'SUPER' для лучшего сопоставления
                    if suffix.lower() == 's':
                        suffix = 'super'
                    result = f"{number} {suffix}"
                    print(f"    Возвращаем: '{result}'")
                    return result
                print(f"    Суффикс не найден, продолжаем поиск")
        print("  Ни один паттерн в скобках не дал суффикс")
    
    # Паттерны для извлечения модели
    patterns = [
        # Специфичные паттерны с суффиксами (высший приоритет)
        r'(geforce\s+(?:gtx|rtx)\s+\d+\s*(?:ti|super)?)',
        r'(gtx\s+\d+\s*(?:ti|super)?)',
        r'(rtx\s+\d+\s*(?:ti|super)?)',
        r'(geforce\s+gt\s+\d+)',
        r'(gt\s+\d+)',
        r'(geforce\s+gts\s+\d+)',
        r'(gts\s+\d+)',
        r'(geforce\s+gs\s+\d+)',
        r'(gs\s+\d+)',
        r'(geforce\s+g\s+\d+)',
        r'(g\s+\d+)',
        r'(radeon\s+rx\s+\d+\s*(?:xt)?)',
        r'(rx\s+\d+\s*(?:xt)?)',
        r'(radeon\s+hd\s+\d+)',
        r'(hd\s+\d+)',
        r'(radeon\s+r\d+\s+\d+)',
        r'(r\d+\s+\d+)',
        r'(radeon\s+pro\s+wx\s+\d+)',
        r'(pro\s+wx\s+\d+)',
        r'(quadro\s+\w+\s+\d+)',
        r'(quadro\s+\d+)',
        r'(radeon\s+pro\s+wx\s+\d+)',
        r'(pro\s+wx\s+\d+)',
        r'(radeon\s+pro\s+w\s+\d+)',
        r'(pro\s+w\s+\d+)',
        r'(radeon\s+pro\s+v\s+\d+)',
        r'(pro\s+v\s+\d+)',
        r'(radeon\s+pro\s+e\s+\d+)',
        r'(pro\s+e\s+\d+)',
        r'(radeon\s+pro\s+s\s+\d+)',
        r'(pro\s+s\s+\d+)',
        # Общий паттерн для цифр (низший приоритет)
        r'(\d+\s*(?:ti|super|xt)?)',
    ]
    for i, pattern in enumerate(patterns):
        match = re.search(pattern, name)
        if match:
            model = match.group(1).strip()
            print(f"  Основной паттерн {i}: {pattern}")
            print(f"  Найдено: '{model}'")
            # Убираем лишние слова
            model = re.sub(r'\b(geforce|radeon|pro|wx|w|v|e|s|d|u|z|vega|fe|56|64|liquid|air|limited|edition|cooled)\b', '', model).strip()
            model = re.sub(r'\s+', ' ', model).strip()
            if model and len(model) > 2:
                print(f"  Возвращаем: '{model}'")
                return model
    print("  Ничего не найдено")
    return ""

def normalize_gpu_name(name: str) -> str:
    """Нормализует название видеокарты для сравнения"""
    if not name:
        return ""
    name = name.lower()
    name = re.sub(r'\s+', ' ', name).strip()
    # Убираем лишние слова и символы
    name = re.sub(r'\b(geforce|radeon|pro|wx|w|v|e|s|d|u|z|vega|fe|56|64|liquid|air|limited|edition|cooled)\b', '', name)
    name = re.sub(r'[^\w\s]', '', name)
    name = re.sub(r'\s+', ' ', name).strip()
    return name

def find_matching_gpu(gpu_name: str, gpu_database: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """Находит соответствующую видеокарту в базе данных с приоритетом десктопных версий и точного совпадения"""
    
    # Извлекаем модель из названия
    model_name = extract_model_name(gpu_name)
    normalized_name = normalize_gpu_name(gpu_name)
    
    print(f"  Извлечена модель: {model_name}")
    print(f"  Нормализованное название: {normalized_name}")
    
    if not model_name and not normalized_name:
        return None
    
    # 1. Сначала ищем точное совпадение по нормализованному названию (например, 'geforce gtx 1650 super')
    for gpu in gpu_database:
        db_name = normalize_gpu_name(gpu.get('name', ''))
        if normalized_name == db_name:
            print(f"  ✅ Точное совпадение по нормализованному названию: {gpu.get('name', '')}")
            return gpu
    
    # 2. Ищем по модели
    if model_name:
        for gpu in gpu_database:
            db_name = gpu.get('name', '').lower()
            if model_name in db_name:
                print(f"  ✅ Совпадение по модели: {gpu.get('name', '')}")
                return gpu
    
    # 3. Частичное совпадение с фильтрацией по бренду
    if model_name:
        # Определяем бренд из названия
        brand = "nvidia" if any(word in gpu_name.lower() for word in ["geforce", "gtx", "rtx", "gt", "quadro"]) else \
                "amd" if any(word in gpu_name.lower() for word in ["radeon", "rx", "hd"]) else \
                "intel"
        
        print(f"  Определен бренд: {brand}")
        
        for gpu in gpu_database:
            db_name = gpu.get('name', '').lower()
            db_brand = gpu.get('manufacturer', '').lower()
            
            # Проверяем совпадение бренда
            if brand == "nvidia" and db_brand == "nvidia" and model_name in db_name:
                print(f"  ✅ Частичное совпадение NVIDIA: {gpu.get('name', '')}")
                return gpu
            elif brand == "amd" and db_brand == "amd" and model_name in db_name:
                print(f"  ✅ Частичное совпадение AMD: {gpu.get('name', '')}")
                return gpu
            elif brand == "intel" and db_brand == "intel" and model_name in db_name:
                print(f"  ✅ Частичное совпадение Intel: {gpu.get('name', '')}")
                return gpu
    
    print(f"  ❌ Совпадение не найдено")
    return None

# Тестируем проблемную видеокарту
test_gpu_name = "(TUF 3-GTX1660S-O6G-GAMING)"

print("=" * 80)
print(f"ТЕСТИРУЕМ: {test_gpu_name}")
print("=" * 80)

# Загружаем базу данных GPU
gpu_database = []
with open('gpu-database.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        gpu_database.append(row)

print(f"Загружено {len(gpu_database)} записей из базы данных GPU")

# Ищем совпадение
result = find_matching_gpu(test_gpu_name, gpu_database)

if result:
    print(f"\n✅ НАЙДЕНО СОВПАДЕНИЕ:")
    print(f"   Название: {result.get('name', '')}")
    print(f"   Производитель: {result.get('manufacturer', '')}")
    print(f"   Архитектура: {result.get('architecture', '')}")
else:
    print(f"\n❌ СОВПАДЕНИЕ НЕ НАЙДЕНО") 