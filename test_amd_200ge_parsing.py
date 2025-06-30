import csv
import re

def test_amd_200ge_parsing():
    """Тестирует парсинг строки с AMD Athlon 200GE"""
    
    # Строка из amd-cpus.csv для AMD Athlon 200GE
    test_line = ',on,""AMD Athlon 200GE"",""AMD Athlon Processors"",""AMD Athlon Desktop Processors with Radeon Vega Graphics"",""Boxed Processor"",""YD200GC6M2OFB / YD20GGC6M2OFB"",YD200GC6FBBOX,YD200GC6FBMPK,,2,4,3,3.2GHz,,,192KB,1MB,4MB,,No,14nm,AM4,,""PCIe 3.0"",,,,35W,,95C,""Windows 10 - 64-Bit Edition, RHEL x86 64-Bit, Ubuntu x86 64-Bit  *O'
    
    print("Тестируем парсинг строки AMD Athlon 200GE:")
    print(f"Исходная строка: {test_line}")
    print()
    
    # Метод 1: Простой split по запятой
    print("=== Метод 1: Простой split по запятой ===")
    parts1 = test_line.split(',')
    print(f"Количество частей: {len(parts1)}")
    for i, part in enumerate(parts1[:10]):  # Показываем первые 10 частей
        print(f"  {i}: '{part}'")
    print()
    
    # Метод 2: Парсинг с учетом кавычек
    print("=== Метод 2: Парсинг с учетом кавычек ===")
    parts2 = []
    current = ""
    in_quotes = False
    for char in test_line:
        if char == '"':
            in_quotes = not in_quotes
        elif char == ',' and not in_quotes:
            parts2.append(current.strip().strip('"'))
            current = ""
        else:
            current += char
    parts2.append(current.strip().strip('"'))
    
    print(f"Количество частей: {len(parts2)}")
    for i, part in enumerate(parts2[:10]):  # Показываем первые 10 частей
        print(f"  {i}: '{part}'")
    print()
    
    # Проверяем, есть ли YD200GC6M2OFB в результатах
    print("=== Поиск артикула YD200GC6M2OFB ===")
    for i, part in enumerate(parts2):
        if 'YD200GC6M2OFB' in part:
            print(f"Найден в части {i}: '{part}'")
    
    # Проверяем, есть ли YD200GC6M2OFB в простом split
    print("=== Поиск в простом split ===")
    for i, part in enumerate(parts1):
        if 'YD200GC6M2OFB' in part:
            print(f"Найден в части {i}: '{part}'")

if __name__ == "__main__":
    test_amd_200ge_parsing() 