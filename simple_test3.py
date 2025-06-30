import csv

def simple_test3():
    """Простой тест парсинга AMD CSV с простым split"""
    
    # Читаем строку 261 (где должен быть YD1200BBM4KAE)
    with open('amd-cpus.csv', 'r', encoding='cp1252') as f:
        lines = f.readlines()
    
    line_261 = lines[260]  # 0-based index
    print(f"Строка 261: {line_261[:200]}...")
    
    # Простой парсинг по запятой, игнорируя кавычки
    parts = line_261.split(',')
    parts = [part.strip().strip('"') for part in parts]
    
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
    simple_test3() 