import json

def main():
    # Загружаем JSON файл
    print("📁 Загружаем components.json...")
    try:
        with open('components.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("❌ Файл components.json не найден!")
        return
    
    # Ищем конкретную видеокарту
    target_name = "(TUF 3-GTX1660S-O6G-GAMING)"
    
    print(f"🔍 Ищем видеокарту: {target_name}")
    print("=" * 60)
    
    if 'GPU' not in data:
        print("❌ В JSON файле нет секции GPU!")
        return
    
    gpus = data['GPU']
    found = False
    
    for i, gpu in enumerate(gpus):
        if gpu.get('name') == target_name:
            found = True
            print(f"✅ Найдена видеокарта на позиции {i+1}:")
            print(f"   Название: {gpu.get('name', 'Не указано')}")
            print(f"   Чистое название: {gpu.get('clean_name', 'Не указано')}")
            print(f"   Производитель: {gpu.get('manufacturer', 'Не указан')}")
            print(f"   Архитектура: {gpu.get('architecture', 'Не указана')}")
            print(f"   Память: {gpu.get('memory_size_gb', 'Не указана')} GB")
            print(f"   Всего полей: {len(gpu)}")
            print()
            print("📋 Все поля:")
            for key, value in gpu.items():
                print(f"   {key}: {value}")
            break
    
    if not found:
        print(f"❌ Видеокарта '{target_name}' не найдена в JSON файле")
        
        # Показываем похожие названия
        print("\n🔍 Похожие названия:")
        for i, gpu in enumerate(gpus):
            name = gpu.get('name', '')
            if 'tuf' in name.lower() and '1660' in name.lower():
                print(f"   {i+1}. {name}")
                print(f"      clean_name: {gpu.get('clean_name', 'Не указано')}")
                print(f"      manufacturer: {gpu.get('manufacturer', 'Не указан')}")

if __name__ == "__main__":
    main() 