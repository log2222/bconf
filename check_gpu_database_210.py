import csv

def check_gpu_database_210():
    """Проверяет записи GeForce 210 в базе данных GPU"""
    
    try:
        with open('gpu-database.csv', 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            geforce210_db = [row for row in reader if '210' in row.get('name', '')]
    except FileNotFoundError:
        print("❌ Файл gpu-database.csv не найден!")
        return
    except Exception as e:
        print(f"❌ Ошибка при чтении CSV файла: {e}")
        return
    
    print(f"🔍 Найдено {len(geforce210_db)} записей GeForce 210 в базе данных:")
    print("=" * 80)
    
    for i, gpu in enumerate(geforce210_db):
        print(f"\n{i+1}. {gpu.get('name', 'Неизвестно')}")
        print(f"   manufacturer: {gpu.get('manufacturer', 'Нет')}")
        print(f"   architecture: {gpu.get('architecture', 'Нет')}")
        print(f"   generation: {gpu.get('generation', 'Нет')}")
        print(f"   memory_size: {gpu.get('memory_size', 'Нет')}")
        print(f"   memory_type: {gpu.get('memory_type', 'Нет')}")
        print(f"   shading_units: {gpu.get('shading_units', 'Нет')}")
    
    # Также проверим RTX 4090 D
    print(f"\n🔍 Проверяем RTX 4090 D в базе данных:")
    print("=" * 80)
    
    try:
        with open('gpu-database.csv', 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            rtx4090d_db = [row for row in reader if '4090' in row.get('name', '') and 'D' in row.get('name', '')]
    except:
        rtx4090d_db = []
    
    for i, gpu in enumerate(rtx4090d_db):
        print(f"\n{i+1}. {gpu.get('name', 'Неизвестно')}")
        print(f"   manufacturer: {gpu.get('manufacturer', 'Нет')}")
        print(f"   architecture: {gpu.get('architecture', 'Нет')}")
        print(f"   generation: {gpu.get('generation', 'Нет')}")

if __name__ == "__main__":
    check_gpu_database_210() 