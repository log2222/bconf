import json
import re

def extract_memory_from_name(name):
    """Улучшенная функция извлечения размера памяти из названия GPU с исправлениями"""
    if not name:
        return None
    
    name_lower = name.lower()
    
    # Специальные случаи для известных моделей
    known_memory = {
        'rx 5700 xt': 8,
        'rtx 2080 ti': 11,
        'rtx 2080': 8,
        'rtx 2070': 8,
        'rtx 2060': 6,
        'gtx 1660 super': 6,
        'gtx 1650 super': 4,
        'gtx 1650': 4,
        'gtx 1660': 6,
        'gtx 1070': 8,
        'gtx 1080': 8,
        'gtx 1080 ti': 11,
        'rx 580': 8,
        'rx 570': 4,
        'gt 1030': 2,
        'gt 710': 1,
    }
    
    # Проверяем известные модели
    for model, memory in known_memory.items():
        if model in name_lower:
            return memory
    
    # Паттерны для извлечения размера памяти
    patterns = [
        # Паттерны с G в конце (например, O2G, A4G, O6G, O8G, A11G)
        r'[ao](\d+)g\b',
        # Паттерны с G в середине (например, 1GD5, 8GC)
        r'(\d+)g[dch]\d*',
        # Паттерны с пробелом (например, 8G , 4G)
        r'(\d+)g\s*[,]',
        # Паттерны с Mb/MB
        r'(\d+)\s*mb\b',
        # Паттерны с Gb/GB
        r'(\d+)\s*gb\b',
        # Паттерны с G в конце слова
        r'(\d+)g\b',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, name_lower)
        if match:
            value = int(match.group(1))
            # Если значение больше 100, скорее всего это MB, конвертируем в GB
            if value > 100:
                return value // 1024
            # Проверяем, что значение разумное (1-24 GB)
            if 1 <= value <= 24:
                return value
    
    return None

def test_fixed_memory_extraction():
    """Тестирует исправленную функцию извлечения памяти"""
    
    try:
        with open('components.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("❌ Файл components.json не найден!")
        return
    except Exception as e:
        print(f"❌ Ошибка при чтении JSON файла: {e}")
        return
    
    gpus = data.get('GPU', [])
    without_name_gb = [g for g in gpus if 'name_gb' not in g]
    
    print(f"🧪 Тестирование исправленного извлечения памяти для {len(without_name_gb)} GPU:")
    print("=" * 80)
    
    success_count = 0
    for i, gpu in enumerate(without_name_gb):
        name = gpu.get('name', 'Неизвестно')
        clean_name = gpu.get('clean_name', '')
        extracted = extract_memory_from_name(name)
        
        print(f"\n{i+1}. {name}")
        print(f"   clean_name: {clean_name}")
        print(f"   Извлеченный размер: {extracted}GB" if extracted else "   ❌ Не удалось извлечь")
        
        if extracted:
            success_count += 1
    
    print(f"\n📊 Результаты:")
    print(f"   Успешно извлечено: {success_count}/{len(without_name_gb)} ({success_count/len(without_name_gb)*100:.1f}%)")

if __name__ == "__main__":
    test_fixed_memory_extraction() 