import json

def show_gpu_names():
    """Выводит все поля name из видеокарт в JSON файле и итоговое название"""
    
    print("=== ПОЛЯ NAME ВИДЕОКАРТ В JSON ===\n")
    
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
        
        # Выводим все поля name и итоговое название
        for i, gpu in enumerate(gpus, 1):
            name = gpu.get('name', 'Название отсутствует')
            clean_name = gpu.get('clean_name', '')
            name_gb = gpu.get('name_gb', '')
            final_gpu_name = f"{clean_name} {name_gb}".strip()
            print(f"{i:3d}. {name}")
            print(f"     Итоговое название: {final_gpu_name}")
        
        print(f"\nВсего видеокарт: {len(gpus)}")
        
        # Показываем статистику по производителям
        manufacturers = {}
        for gpu in gpus:
            m = gpu.get('manufacturer', 'Unknown')
            manufacturers[m] = manufacturers.get(m, 0) + 1
        print("\nПроизводители:")
        for m, count in manufacturers.items():
            print(f"  {m}: {count}")
        
        # Показываем примеры обогащенных видеокарт
        enriched_count = 0
        for gpu in gpus:
            if len(gpu) > 5:  # Более 5 полей = обогащенная
                enriched_count += 1
        
        print(f"\nОбогащенных видеокарт: {enriched_count}/{len(gpus)} ({enriched_count/len(gpus)*100:.1f}%)")
        
    except FileNotFoundError:
        print("❌ Файл components.json не найден!")
    except Exception as e:
        print(f"❌ Ошибка при чтении JSON файла: {e}")

if __name__ == "__main__":
    show_gpu_names() 