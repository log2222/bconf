import json

def check_geforce210():
    """Проверяет записи GeForce 210 и их обогащение"""
    
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
    geforce210_entries = [g for g in gpus if '210' in g.get('name', '')]
    
    print(f"🔍 Найдено {len(geforce210_entries)} записей GeForce 210:")
    print("=" * 80)
    
    for i, gpu in enumerate(geforce210_entries):
        print(f"\n{i+1}. {gpu.get('name', 'Неизвестно')}")
        print(f"   clean_name: {gpu.get('clean_name', 'Нет')}")
        print(f"   name_gb: {gpu.get('name_gb', 'Нет')}")
        print(f"   memory_size_gb: {gpu.get('memory_size_gb', 'Нет')}")
        print(f"   manufacturer: {gpu.get('manufacturer', 'Нет')}")
        print(f"   architecture: {gpu.get('architecture', 'Нет')}")
        print(f"   generation: {gpu.get('generation', 'Нет')}")
        print(f"   memory_type: {gpu.get('memory_type', 'Нет')}")
        print(f"   shading_units: {gpu.get('shading_units', 'Нет')}")
        print(f"   tensor_cores: {gpu.get('tensor_cores', 'Нет')}")
        print(f"   ray_tracing_cores: {gpu.get('ray_tracing_cores', 'Нет')}")
        
        # Проверяем, правильно ли обогащена
        if gpu.get('clean_name') == 'GeForce RTX 4090 D':
            print("   ❌ НЕПРАВИЛЬНОЕ ОБОГАЩЕНИЕ!")
        elif gpu.get('clean_name') == 'GeForce 210':
            print("   ✅ Правильное обогащение")
        else:
            print("   ⚠️ Неизвестное обогащение")

if __name__ == "__main__":
    check_geforce210() 