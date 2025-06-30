import json
import csv
import re

def extract_model_name(gpu_name):
    """Извлекает название модели из названия видеокарты"""
    if not gpu_name:
        return None
    
    # Убираем скобки и их содержимое
    name = re.sub(r'\([^)]*\)', '', gpu_name)
    
    # Приводим к нижнему регистру
    name = name.lower()
    
    # Паттерны для извлечения модели
    patterns = [
        r'geforce\s+(gtx?\s*)?(\d+[a-z]*\s*(?:super|ti)?)',
        r'radeon\s+(rx\s*)?(\d+[a-z]*\s*(?:xt)?)',
        r'rtx\s+(\d+[a-z]*\s*(?:super|ti)?)',
        r'gtx\s+(\d+[a-z]*\s*(?:super|ti)?)',
        r'gt\s+(\d+[a-z]*)',
        r'quadro\s+(\w+)',
        r'firepro\s+(\w+)',
        r'arc\s+(\w+)',
        r'(\d+[a-z]*\s*(?:super|ti|xt)?)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, name)
        if match:
            model = match.group(1) if len(match.groups()) == 1 else match.group(2)
            if model:
                return model.strip()
    
    return None

def find_matching_gpu_debug(gpu_name, gpu_database):
    """Отладочная версия функции поиска соответствия"""
    
    print(f"\n🔍 ОТЛАДКА для: {gpu_name}")
    print("=" * 80)
    
    # Извлекаем модель из названия
    model_name = extract_model_name(gpu_name)
    
    print(f"📝 Извлеченная модель: '{model_name}'")
    
    if not model_name:
        print("❌ Не удалось извлечь модель")
        return None
    
    # Ищем точное совпадение по clean_name для GeForce 210
    if '210' in gpu_name.lower():
        print("\n🎯 Поиск точного совпадения для GeForce 210:")
        for gpu in gpu_database:
            db_name = gpu.get('name', '').lower()
            if 'geforce' in db_name and '210' in db_name:
                print(f"   ✅ Найдено: {gpu.get('name')}")
                return gpu
    
    # Ищем по модели
    print(f"\n🔍 Поиск по модели '{model_name}':")
    matches = []
    for gpu in gpu_database:
        db_name = gpu.get('name', '').lower()
        db_model = extract_model_name(gpu.get('name', ''))
        
        if model_name == db_model:
            print(f"   ✅ Точное совпадение модели: {gpu.get('name')}")
            matches.append((gpu, 100, 'exact_model'))
        elif model_name and model_name in db_name:
            print(f"   ⚠️ Частичное совпадение: {gpu.get('name')}")
            matches.append((gpu, 80, 'partial_model'))
    
    if matches:
        # Сортируем по приоритету
        matches.sort(key=lambda x: x[1], reverse=True)
        best_match = matches[0]
        print(f"\n🏆 Лучшее совпадение: {best_match[0].get('name')} (оценка: {best_match[1]})")
        return best_match[0]
    
    print("❌ Совпадений не найдено")
    return None

def main():
    # Загружаем JSON данные
    try:
        with open('components.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ Ошибка при чтении JSON: {e}")
        return
    
    # Загружаем базу данных GPU
    try:
        with open('gpu-database.csv', 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            gpu_database = list(reader)
    except Exception as e:
        print(f"❌ Ошибка при чтении CSV: {e}")
        return
    
    # Находим GeForce 210 в JSON
    gpus = data.get('GPU', [])
    geforce210_entries = [g for g in gpus if '210' in g.get('name', '')]
    
    if not geforce210_entries:
        print("❌ GeForce 210 не найден в JSON")
        return
    
    # Тестируем первую запись GeForce 210
    test_gpu = geforce210_entries[0]
    print(f"🧪 Тестируем: {test_gpu.get('name')}")
    
    # Ищем соответствие
    match = find_matching_gpu_debug(test_gpu.get('name'), gpu_database)
    
    if match:
        print(f"\n✅ Найдено правильное соответствие: {match.get('name')}")
    else:
        print("\n❌ Соответствие не найдено")

if __name__ == "__main__":
    main() 