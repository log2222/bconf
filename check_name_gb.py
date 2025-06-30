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
    
    # Проверяем наличие видеокарт в JSON
    if 'GPU' not in data:
        print("❌ В JSON файле нет секции GPU!")
        return
    
    gpus = data['GPU']
    print(f"📊 Всего видеокарт в JSON: {len(gpus)}")
    
    # Проверяем наличие поля name_gb
    gpus_with_name_gb = 0
    gpus_without_name_gb = []
    
    for i, gpu in enumerate(gpus):
        if 'name_gb' in gpu and gpu['name_gb'] is not None:
            gpus_with_name_gb += 1
        else:
            gpus_without_name_gb.append((i+1, gpu.get('name', 'Не указано')))
    
    print(f"\n📋 Статистика поля name_gb:")
    print(f"   Видеокарт с полем name_gb: {gpus_with_name_gb}")
    print(f"   Видеокарт без поля name_gb: {len(gpus_without_name_gb)}")
    print(f"   Процент покрытия: {(gpus_with_name_gb / len(gpus) * 100):.1f}%")
    
    if gpus_without_name_gb:
        print(f"\n❌ Видеокарты без поля name_gb:")
        for i, (index, name) in enumerate(gpus_without_name_gb[:10]):  # Показываем первые 10
            print(f"   {index}. {name}")
        if len(gpus_without_name_gb) > 10:
            print(f"   ... и еще {len(gpus_without_name_gb) - 10} видеокарт")
    
    # Проверяем конкретную проблемную видеокарту
    print(f"\n🔍 Проверяем конкретную видеокарту:")
    target_name = "(TUF 3-GTX1660S-O6G-GAMING)"
    
    for i, gpu in enumerate(gpus):
        if gpu.get('name') == target_name:
            print(f"   Найдена на позиции {i+1}:")
            print(f"   Название: {gpu.get('name', 'Не указано')}")
            print(f"   clean_name: {gpu.get('clean_name', 'Не указано')}")
            print(f"   name_gb: {gpu.get('name_gb', 'Не указано')}")
            print(f"   memory_size_gb: {gpu.get('memory_size_gb', 'Не указано')}")
            print(f"   Производитель: {gpu.get('manufacturer', 'Не указан')}")
            print(f"   Архитектура: {gpu.get('architecture', 'Не указана')}")
            break
    else:
        print(f"   ❌ Видеокарта '{target_name}' не найдена")

if __name__ == "__main__":
    main() 