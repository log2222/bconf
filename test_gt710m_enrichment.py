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
        r'(\d+\s*(?:ti|super|xt|m)?)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, name)
        if match:
            model = match.group(1).strip()
            # Убираем лишние слова
            model = re.sub(r'\b(geforce|radeon|pro|wx|w|v|e|s|d|u|z|vega|fe|56|64|liquid|air|limited|edition|cooled)\b', '', model).strip()
            model = re.sub(r'\s+', ' ', model).strip()
            if model and len(model) > 2:
                return model
    
    return ""

def normalize_gpu_name(name: str) -> str:
    """Нормализует название видеокарты для лучшего сопоставления"""
    if not name:
        return ""
    
    # Приводим к нижнему регистру
    name = name.lower()
    
    # Удаляем лишние пробелы
    name = re.sub(r'\s+', ' ', name).strip()
    
    # Удаляем специальные символы, но оставляем цифры и буквы
    name = re.sub(r'[^\w\s\d]', ' ', name)
    
    # Удаляем лишние пробелы снова
    name = re.sub(r'\s+', ' ', name).strip()
    
    return name

def find_matching_gpu(gpu_name: str, gpu_database: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """Находит соответствующую видеокарту в базе данных"""
    
    # Извлекаем модель из названия
    model_name = extract_model_name(gpu_name)
    normalized_name = normalize_gpu_name(gpu_name)
    
    print(f"  Извлечена модель: '{model_name}'")
    print(f"  Нормализованное название: '{normalized_name}'")
    
    if not model_name and not normalized_name:
        return None
    
    # Сначала ищем точное совпадение по модели
    if model_name:
        for gpu in gpu_database:
            db_name = normalize_gpu_name(gpu.get('name', ''))
            db_model = extract_model_name(gpu.get('name', ''))
            
            if model_name == db_model:
                print(f"  ✅ Найдено точное совпадение по модели: {gpu.get('name', '')}")
                return gpu
            
            # Проверяем, содержит ли название базы данных нашу модель
            if model_name in db_name or model_name in db_model:
                print(f"  ✅ Найдено частичное совпадение по модели: {gpu.get('name', '')}")
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
    
    if best_match:
        print(f"  ✅ Найдено совпадение по сходству ({best_score:.2f}): {best_match.get('name', '')}")
    
    return best_match

def test_gt710m_enrichment():
    """Тестирует обогащение GeForce GT 710M"""
    
    print("=== ТЕСТ ОБОГАЩЕНИЯ GEFORCE GT 710M ===\n")
    
    # Загружаем CSV базу данных
    gpu_database = []
    try:
        with open('gpu-database.csv', 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            gpu_database = list(reader)
        print(f"Загружено {len(gpu_database)} видеокарт из CSV базы данных")
    except FileNotFoundError:
        print("❌ Файл gpu-database.csv не найден!")
        return
    
    # Тестовые видеокарты с GT 710M
    test_gpus = [
        "Видеокарта NVIDIA GeForce GT 710M 2GB DDR3",
        "NVIDIA GeForce GT 710M",
        "GT 710M",
        "GeForce GT 710M 1GB",
        "Видеокарта GT 710M для ноутбука"
    ]
    
    print(f"\nТестируем обогащение {len(test_gpus)} вариантов GT 710M:\n")
    
    for i, gpu_name in enumerate(test_gpus, 1):
        print(f"{i}. {gpu_name}")
        
        # Ищем соответствующую видеокарту в базе данных
        matching_gpu = find_matching_gpu(gpu_name, gpu_database)
        
        if matching_gpu:
            print(f"  📊 Найдена в базе: {matching_gpu.get('name', '')}")
            print(f"  🏭 Производитель: {matching_gpu.get('manufacturer', 'Не указан')}")
            print(f"  🏗️  Архитектура: {matching_gpu.get('architecture', 'Не указана')}")
            print(f"  💾 Память: {matching_gpu.get('memory_size', 'Не указана')} {matching_gpu.get('memory_type', '')}")
            print(f"  ⚡ TDP: {matching_gpu.get('thermal_design_power', 'Не указан')}")
            print(f"  📅 Дата выпуска: {matching_gpu.get('release_date', 'Не указана')}")
            print(f"  🔧 Процесс: {matching_gpu.get('process_size', 'Не указан')}")
            print(f"  🎯 Шейдеры: {matching_gpu.get('shading_units', 'Не указано')}")
            print(f"  🖼️  TMU: {matching_gpu.get('texture_mapping_units', 'Не указано')}")
            print(f"  📺 ROP: {matching_gpu.get('render_output_processors', 'Не указано')}")
            print(f"  ⏱️  Базовая частота: {matching_gpu.get('base_clock', 'Не указана')}")
            print(f"  🚀 Boost частота: {matching_gpu.get('boost_clock', 'Не указана')}")
            print(f"  🔌 Интерфейс: {matching_gpu.get('bus_interface', 'Не указан')}")
        else:
            print(f"  ❌ Не найдено соответствие в базе данных")
        
        print()

if __name__ == "__main__":
    test_gt710m_enrichment() 