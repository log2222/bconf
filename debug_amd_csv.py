import csv

def debug_amd_csv():
    """Детальная отладка amd-cpus.csv"""
    
    # Читаем файл построчно
    with open('amd-cpus.csv', 'r', encoding='cp1252') as f:
        lines = f.readlines()
    
    print(f"Всего строк: {len(lines)}")
    print("\nПервые 5 строк:")
    for i, line in enumerate(lines[:5]):
        print(f"Строка {i+1}: {repr(line[:200])}")
    
    # Пробуем найти строку с YD1200BBM4KAE
    print("\nПоиск YD1200BBM4KAE:")
    for i, line in enumerate(lines):
        if 'YD1200BBM4KAE' in line:
            print(f"Найдено в строке {i+1}: {line.strip()}")
            break
    
    # Парсим CSV вручную
    print("\nПарсинг CSV вручную:")
    for i, line in enumerate(lines[1:6]):  # Пропускаем первую строку
        print(f"\nСтрока {i+2}:")
        # Разбиваем по запятой, учитывая кавычки
        parts = []
        current = ""
        in_quotes = False
        for char in line:
            if char == '"':
                in_quotes = not in_quotes
            elif char == ',' and not in_quotes:
                parts.append(current.strip())
                current = ""
            else:
                current += char
        parts.append(current.strip())
        
        print(f"Количество частей: {len(parts)}")
        for j, part in enumerate(parts):
            if part:  # Показываем только непустые
                print(f"  {j}: {part}")

if __name__ == "__main__":
    debug_amd_csv() 