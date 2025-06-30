import csv

def simple_test2():
    """Простой тест парсинга AMD CSV"""
    
    # Читаем строку 261 (где должен быть YD1200BBM4KAE)
    with open('amd-cpus.csv', 'r', encoding='cp1252') as f:
        lines = f.readlines()
    
    line_261 = lines[260]  # 0-based index
    print(f"Строка 261: {line_261[:200]}...")
    
    # Простой парсинг по запятой, учитывая кавычки
    parts = []
    current = ""
    in_quotes = False
    for char in line_261:
        if char == '"':
            in_quotes = not in_quotes
        elif char == ',' and not in_quotes:
            parts.append(current.strip().strip('"'))
            current = ""
        else:
            current += char
    parts.append(current.strip().strip('"'))
    
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
    simple_test2() 