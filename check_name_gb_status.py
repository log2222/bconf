import json

def check_gpu_status():
    """Проверяет статус обогащения GPU и наличие поля name_gb"""
    
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
    print(f"📊 Всего GPU в JSON: {len(gpus)}")
    
    # Проверяем обогащенные GPU
    enriched = [g for g in gpus if 'clean_name' in g]
    print(f"✅ Обогащенных GPU: {len(enriched)}")
    
    # Проверяем GPU с полем name_gb
    with_name_gb = [g for g in gpus if 'name_gb' in g]
    print(f"💾 GPU с полем name_gb: {len(with_name_gb)}")
    
    # Проверяем процент обогащения
    if gpus:
        enrichment_percent = (len(enriched) / len(gpus)) * 100
        name_gb_percent = (len(with_name_gb) / len(gpus)) * 100
        print(f"📈 Процент обогащения: {enrichment_percent:.1f}%")
        print(f"📈 Процент с name_gb: {name_gb_percent:.1f}%")
    
    # Показываем примеры GPU с name_gb
    if with_name_gb:
        print(f"\n🔍 Примеры GPU с полем name_gb:")
        for i, gpu in enumerate(with_name_gb[:3]):
            print(f"{i+1}. {gpu.get('name', 'Неизвестно')}")
            print(f"   name_gb: {gpu.get('name_gb', 'Нет')}")
            print(f"   memory_size_gb: {gpu.get('memory_size_gb', 'Нет')}")
            print(f"   clean_name: {gpu.get('clean_name', 'Нет')}")
            print()
    
    # Показываем примеры GPU без name_gb
    without_name_gb = [g for g in gpus if 'name_gb' not in g]
    if without_name_gb:
        print(f"❌ Примеры GPU БЕЗ поля name_gb:")
        for i, gpu in enumerate(without_name_gb[:3]):
            print(f"{i+1}. {gpu.get('name', 'Неизвестно')}")
            print(f"   memory_size_gb: {gpu.get('memory_size_gb', 'Нет')}")
            print(f"   clean_name: {gpu.get('clean_name', 'Нет')}")
            print()

if __name__ == "__main__":
    check_gpu_status() 