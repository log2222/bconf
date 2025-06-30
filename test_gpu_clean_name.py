import json
import csv
import re
from typing import Dict, List, Any, Optional

def extract_model_name(name: str) -> str:
    """Извлекает название модели из полного названия видеокарты"""
    if not name:
        return ""
    
    # Приводим к нижнему регистру
    name = name.lower()
    
    # Удаляем лишние пробелы
    name = re.sub(r'\s+', ' ', name).strip()
    
    # Паттерны для извлечения модели
    patterns = [
        # NVIDIA GeForce GTX/RTX
        r'(geforce\s+(?:gtx|rtx)\s+\d+\s*(?:ti|super)?)',
        r'(gtx\s+\d+\s*(?:ti|super)?)',
        r'(rtx\s+\d+\s*(?:ti|super)?)',
        # NVIDIA GeForce GT
        r'(geforce\s+gt\s+\d+\s*(?:m)?)',
        r'(gt\s+\d+\s*(?:m)?)',
        # AMD Radeon RX
        r'(radeon\s+rx\s+\d+\s*(?:xt)?)',
        r'(rx\s+\d+\s*(?:xt)?)',
        # Общие паттерны для цифр
        r'(\d+\s*(?:ti|super|xt)?)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, name)
        if match:
            return match.group(1)
    
    return ""

def normalize_gpu_name(name: str) -> str:
    """Нормализует название видеокарты для сравнения"""
    if not name:
        return ""
    
    # Приводим к нижнему регистру
    name = name.lower()
    
    # Удаляем лишние пробелы
    name = re.sub(r'\s+', ' ', name).strip()
    
    return name

def find_matching_gpu(gpu_name: str, gpu_database: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """Находит соответствующую видеокарту в базе данных"""
    
    # Извлекаем модель из названия
    model_name = extract_model_name(gpu_name)
    normalized_name = normalize_gpu_name(gpu_name)
    
    if not model_name and not normalized_name:
        return None
    
    # Сначала ищем точное совпадение по модели
    if model_name:
        for gpu in gpu_database:
            db_name = normalize_gpu_name(gpu.get('name', ''))
            db_model = extract_model_name(gpu.get('name', ''))
            
            if model_name == db_model:
                return gpu
            
            # Проверяем, содержит ли название базы данных нашу модель
            if model_name in db_name or model_name in db_model:
                return gpu
    
    # Ищем частичные совпадения по нормализованному названию
    best_match = None
    best_score = 0
    
    for gpu in gpu_database:
        db_name = normalize_gpu_name(gpu.get('name', ''))
        
        if not db_name:
            continue
        
        # Проверяем, содержит ли название базы данных ключевые слова из нашего названия
        name_parts = normalized_name.split()
        db_parts = db_name.split()
        
        # Считаем количество совпадающих частей
        matches = 0
        for part in name_parts:
            if any(part in db_part or db_part in part for db_part in db_parts):
                matches += 1
        
        # Вычисляем процент совпадения
        if name_parts:
            score = matches / len(name_parts)
            if score > best_score and score > 0.3:  # Снижаем порог до 30%
                best_score = score
                best_match = gpu
    
    return best_match

def test_gpu_clean_name():
    """Тестирует добавление поля clean_name для видеокарт"""
    
    print("=== ТЕСТ ДОБАВЛЕНИЯ ПОЛЯ CLEAN_NAME ДЛЯ ВИДЕОКАРТ ===\n")
    
    # Загружаем CSV базу данных
    print("Загружаем базу данных видеокарт...")
    gpu_database = []
    try:
        with open('gpu-database.csv', 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            gpu_database = list(reader)
        print(f"✅ Загружено {len(gpu_database)} видеокарт из CSV")
    except Exception as e:
        print(f"❌ Ошибка при загрузке CSV: {e}")
        return
    
    # Тестовые видеокарты из JSON
    test_gpus = [
        {
            "name": "Видеокарта Palit PCI-E PA-GT710-1GD5 nVidia GeForce GT 710 1024Mb 64bit GDDR5 954/2500 DVIx1/HDMIx1/CRTx1/HDCP Bulk low profile",
            "price": 2889,
            "code": "00-00236339",
            "article": "NE5T7100HD06-2081F"
        },
        {
            "name": "Видеокарта MSI PCI-E GT 710 1GD3H LP nVidia GeForce GT 710 1024Mb 64bit DDR3 954/1600 DVIx1/HDMIx1/CRTx1/HDCP Ret low profile",
            "price": 3000,
            "code": "00-00236340",
            "article": "GT710-1GD3H-LP"
        },
        {
            "name": "Видеокарта MSI PCI-E RX 550 2GT LP OC AMD Radeon RX 550 2048Mb 128bit GDDR5 1203/7000 DVIx1/HDMIx1/HDCP Ret low profile",
            "price": 15000,
            "code": "00-00236341",
            "article": "RX550-2GT-LP-OC"
        }
    ]
    
    print(f"\nТестируем {len(test_gpus)} видеокарт:\n")
    
    for i, test_gpu in enumerate(test_gpus, 1):
        gpu_name = test_gpu.get('name', '')
        print(f"{i}. {gpu_name}")
        
        # Ищем соответствие в базе данных
        matching_gpu = find_matching_gpu(gpu_name, gpu_database)
        
        if matching_gpu:
            csv_name = matching_gpu.get('name', '')
            print(f"   ✅ Найдено соответствие в CSV: {csv_name}")
            print(f"   📝 Будет добавлено поле clean_name: {csv_name}")
            
            # Показываем дополнительные поля из CSV
            manufacturer = matching_gpu.get('manufacturer', '')
            architecture = matching_gpu.get('architecture', '')
            memory_type = matching_gpu.get('memory_type', '')
            print(f"   🏭 Производитель: {manufacturer}")
            print(f"   🏗️  Архитектура: {architecture}")
            print(f"   💾 Тип памяти: {memory_type}")
        else:
            print(f"   ❌ Не найдено соответствие в CSV")
        
        print()
    
    print("=== РЕЗУЛЬТАТ ТЕСТА ===")
    print("✅ Поле clean_name будет добавлено для всех найденных соответствий")
    print("📝 Это поле будет содержать чистое название модели из CSV базы данных")
    print("🔧 Для применения изменений запустите: python gpu_enrich_from_csv.py")

if __name__ == "__main__":
    test_gpu_clean_name() 