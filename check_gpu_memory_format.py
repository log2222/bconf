import json

def check_gpu_memory_format():
    """Проверяет текущий формат поля memory_size_gb у видеокарт"""
    
    print("=== ПРОВЕРКА ФОРМАТА MEMORY_SIZE_GB У ВИДЕОКАРТ ===\n")
    
    try:
        # Загружаем JSON файл
        with open('components.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Проверяем наличие секции GPU
        if 'GPU' not in data:
            print("❌ В JSON файле нет секции GPU!")
            return
        
        gpus = data['GPU']
        print(f"Найдено {len(gpus)} видеокарт в JSON файле\n")
        
        # Анализируем формат memory_size_gb
        memory_formats = {}
        gpus_with_memory = []
        
        for i, gpu in enumerate(gpus):
            memory_size = gpu.get('memory_size_gb')
            if memory_size is not None:
                gpus_with_memory.append((i+1, gpu))
                memory_type = type(memory_size).__name__
                if memory_type not in memory_formats:
                    memory_formats[memory_type] = []
                memory_formats[memory_type].append(memory_size)
        
        print(f"Видеокарт с полем memory_size_gb: {len(gpus_with_memory)}\n")
        
        # Показываем статистику по типам данных
        print("📊 Статистика по типам данных memory_size_gb:")
        for data_type, values in memory_formats.items():
            unique_values = list(set(values))
            print(f"  {data_type}: {len(values)} записей, уникальные значения: {unique_values[:10]}")
        
        # Показываем примеры видеокарт с memory_size_gb
        print(f"\n📋 Примеры видеокарт с memory_size_gb:")
        for i, (num, gpu) in enumerate(gpus_with_memory[:10]):
            name = gpu.get('name', 'Неизвестно')
            clean_name = gpu.get('clean_name', 'Не указано')
            memory_size = gpu.get('memory_size_gb')
            memory_type = type(memory_size).__name__
            
            print(f"{i+1}. Видеокарта #{num}:")
            print(f"   name: {name[:80]}...")
            print(f"   clean_name: {clean_name}")
            print(f"   memory_size_gb: {memory_size} (тип: {memory_type})")
            print()
        
        # Показываем примеры GeForce GT 710
        print("🎯 Примеры GeForce GT 710:")
        gt710_examples = []
        for num, gpu in gpus_with_memory:
            if 'GT 710' in gpu.get('clean_name', ''):
                gt710_examples.append((num, gpu))
        
        for i, (num, gpu) in enumerate(gt710_examples[:5]):
            name = gpu.get('name', 'Неизвестно')
            clean_name = gpu.get('clean_name', 'Не указано')
            memory_size = gpu.get('memory_size_gb')
            memory_type = type(memory_size).__name__
            
            print(f"{i+1}. Видеокарта #{num}:")
            print(f"   name: {name[:80]}...")
            print(f"   clean_name: {clean_name}")
            print(f"   memory_size_gb: {memory_size} (тип: {memory_type})")
            print()
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    check_gpu_memory_format() 