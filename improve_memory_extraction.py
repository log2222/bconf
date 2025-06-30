import json
import re

def extract_memory_from_name(name):
    """Улучшенная функция извлечения размера памяти из названия GPU"""
    if not name:
        return None
    
    name_lower = name.lower()
    
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
            return value
    
    return None

def test_memory_extraction():
    """Тестирует улучшенную функцию извлечения памяти"""
    
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
    
    print(f"🧪 Тестирование улучшенного извлечения памяти для {len(without_name_gb)} GPU:")
    print("=" * 80)
    
    success_count = 0
    for i, gpu in enumerate(without_name_gb):
        name = gpu.get('name', 'Неизвестно')
        extracted = extract_memory_from_name(name)
        
        print(f"\n{i+1}. {name}")
        print(f"   Извлеченный размер: {extracted}GB" if extracted else "   ❌ Не удалось извлечь")
        
        if extracted:
            success_count += 1
    
    print(f"\n📊 Результаты:")
    print(f"   Успешно извлечено: {success_count}/{len(without_name_gb)} ({success_count/len(without_name_gb)*100:.1f}%)")

if __name__ == "__main__":
    test_memory_extraction() 