import json

def check_gpu_clean_name():
    """Проверяет добавление поля clean_name к видеокартам"""
    
    print("=== ПРОВЕРКА ПОЛЯ CLEAN_NAME У ВИДЕОКАРТ ===\n")
    
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
        
        # Проверяем наличие поля clean_name
        gpus_with_clean_name = []
        gpus_without_clean_name = []
        
        for i, gpu in enumerate(gpus):
            clean_name = gpu.get('clean_name', None)
            if clean_name:
                gpus_with_clean_name.append((i+1, gpu.get('name', ''), clean_name))
            else:
                gpus_without_clean_name.append((i+1, gpu.get('name', '')))
        
        print(f"📊 Статистика:")
        print(f"  Видеокарт с полем clean_name: {len(gpus_with_clean_name)}")
        print(f"  Видеокарт без поля clean_name: {len(gpus_without_clean_name)}")
        print(f"  Процент покрытия: {(len(gpus_with_clean_name)/len(gpus)*100):.1f}%")
        
        # Показываем примеры с clean_name
        if gpus_with_clean_name:
            print(f"\n✅ Примеры видеокарт с полем clean_name:")
            for i, (num, name, clean_name) in enumerate(gpus_with_clean_name[:10]):
                print(f"{i+1:2d}. {num:3d}. {name[:80]}...")
                print(f"    clean_name: {clean_name}")
                print()
        
        # Показываем примеры без clean_name
        if gpus_without_clean_name:
            print(f"\n❌ Примеры видеокарт БЕЗ поля clean_name:")
            for i, (num, name) in enumerate(gpus_without_clean_name[:5]):
                print(f"{i+1}. {num:3d}. {name[:80]}...")
        
        # Показываем уникальные значения clean_name
        unique_clean_names = set()
        for gpu in gpus:
            clean_name = gpu.get('clean_name', '')
            if clean_name:
                unique_clean_names.add(clean_name)
        
        print(f"\n📝 Уникальных значений clean_name: {len(unique_clean_names)}")
        print(f"Примеры уникальных clean_name:")
        for i, clean_name in enumerate(sorted(list(unique_clean_names))[:20]):
            print(f"  {i+1:2d}. {clean_name}")
        
        if len(unique_clean_names) > 20:
            print(f"  ... и еще {len(unique_clean_names) - 20} значений")
        
    except FileNotFoundError:
        print("❌ Файл components.json не найден!")
    except Exception as e:
        print(f"❌ Ошибка при чтении JSON файла: {e}")

if __name__ == "__main__":
    check_gpu_clean_name() 