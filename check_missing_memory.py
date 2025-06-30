import json
import re

def check_missing_memory():
    """Анализирует GPU без поля name_gb и пытается найти размер памяти в других полях"""
    
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
    
    print(f"🔍 Анализ GPU без поля name_gb ({len(without_name_gb)} штук):")
    print("=" * 80)
    
    for i, gpu in enumerate(without_name_gb):
        name = gpu.get('name', 'Неизвестно')
        memory_size_gb = gpu.get('memory_size_gb')
        memory_size_raw = gpu.get('memory_size_raw')
        clean_name = gpu.get('clean_name', 'Нет')
        
        print(f"\n{i+1}. {name}")
        print(f"   memory_size_gb: {memory_size_gb}")
        print(f"   memory_size_raw: {memory_size_raw}")
        print(f"   clean_name: {clean_name}")
        
        # Пытаемся извлечь размер памяти из названия
        memory_patterns = [
            r'(\d+)\s*[mg]b\s*[dg]dr',  # 2048Mb GDDR5
            r'(\d+)\s*[mg]b',           # 2048Mb
            r'(\d+)\s*[dg]dr',          # 2048 GDDR5
            r'(\d+)\s*bit',             # 256bit
        ]
        
        extracted_memory = None
        for pattern in memory_patterns:
            match = re.search(pattern, name.lower())
            if match:
                value = int(match.group(1))
                if 'bit' in pattern:
                    # Это шина памяти, пропускаем
                    continue
                if value > 1000:  # Скорее всего это размер в MB
                    extracted_memory = value // 1024  # Конвертируем в GB
                else:
                    extracted_memory = value
                break
        
        if extracted_memory:
            print(f"   🔍 Извлеченный размер памяти: {extracted_memory}GB")
        else:
            print(f"   ❌ Не удалось извлечь размер памяти из названия")
        
        # Проверяем другие поля на наличие информации о памяти
        for key, value in gpu.items():
            if isinstance(value, str) and any(word in value.lower() for word in ['mb', 'gb', 'memory', 'vram']):
                print(f"   📝 Поле {key}: {value}")

if __name__ == "__main__":
    check_missing_memory() 