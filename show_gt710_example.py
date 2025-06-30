import json

def show_gt710_example():
    """Показывает пример GeForce GT 710 с полем clean_name"""
    
    print("=== ПРИМЕР GEForce GT 710 С ПОЛЕМ CLEAN_NAME ===\n")
    
    try:
        # Загружаем JSON файл
        with open('components.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Ищем GeForce GT 710
        gpus = data['GPU']
        gt710_examples = []
        
        for i, gpu in enumerate(gpus):
            name = gpu.get('name', '')
            if 'GT 710' in name:
                gt710_examples.append((i+1, gpu))
        
        print(f"Найдено {len(gt710_examples)} видеокарт GeForce GT 710:\n")
        
        for i, (num, gpu) in enumerate(gt710_examples):
            print(f"{i+1}. Видеокарта #{num}:")
            print(f"   name: {gpu.get('name', '')}")
            print(f"   clean_name: {gpu.get('clean_name', 'НЕ НАЙДЕНО')}")
            print(f"   price: {gpu.get('price', 'НЕ УКАЗАНО')}")
            print(f"   article: {gpu.get('article', 'НЕ УКАЗАНО')}")
            print(f"   manufacturer: {gpu.get('manufacturer', 'НЕ УКАЗАНО')}")
            print(f"   architecture: {gpu.get('architecture', 'НЕ УКАЗАНО')}")
            print(f"   memory_size_gb: {gpu.get('memory_size_gb', 'НЕ УКАЗАНО')}")
            print(f"   memory_type: {gpu.get('memory_type', 'НЕ УКАЗАНО')}")
            print()
        
        # Показываем общую статистику по GT 710
        if gt710_examples:
            clean_names = set()
            for _, gpu in gt710_examples:
                clean_name = gpu.get('clean_name', '')
                if clean_name:
                    clean_names.add(clean_name)
            
            print(f"📊 Статистика по GeForce GT 710:")
            print(f"  Всего моделей: {len(gt710_examples)}")
            print(f"  Уникальных clean_name: {len(clean_names)}")
            print(f"  Значения clean_name: {', '.join(sorted(clean_names))}")
        
    except FileNotFoundError:
        print("❌ Файл components.json не найден!")
    except Exception as e:
        print(f"❌ Ошибка при чтении JSON файла: {e}")

if __name__ == "__main__":
    show_gt710_example() 