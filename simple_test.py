import csv

def simple_test():
    """Простой тест парсинга AMD CSV"""
    
    # Читаем строку 261 (где должен быть YD1200BBM4KAE)
    with open('amd-cpus.csv', 'r', encoding='cp1252') as f:
        lines = f.readlines()
    
    line_261 = lines[260]  # 0-based index
    print(f"Строка 261: {line_261[:200]}...")
    
    # Парсим с помощью csv.reader
    reader = csv.reader([line_261])
    parts = next(reader)
    
    print(f"Количество частей: {len(parts)}")
    print("Первые 10 частей:")
    for i, part in enumerate(parts[:10]):
        print(f"  {i}: '{part}'")
    
    # Ищем YD1200BBM4KAE
    for i, part in enumerate(parts):
        if 'YD1200BBM4KAE' in part:
            print(f"YD1200BBM4KAE найден в части {i}: '{part}'")
            break

if __name__ == "__main__":
    simple_test() 