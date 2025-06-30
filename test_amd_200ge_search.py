import json
import re
from typing import Dict, List, Optional

def load_csv_data(csv_file: str) -> List[Dict]:
    """Загружает данные из CSV файла"""
    data = []
    try:
        # Пробуем разные кодировки для amd-cpus.csv
        encodings = ['utf-8', 'cp1252', 'latin-1', 'iso-8859-1']
        for encoding in encodings:
            try:
                with open(csv_file, 'r', encoding=encoding) as f:
                    lines = f.readlines()
                    
                    # Для amd-cpus.csv исправляем неправильную структуру
                    if 'amd-cpus.csv' in csv_file and len(lines) > 1:
                        # Парсим вручную, так как CSV имеет неправильную структуру
                        headers = [
                            'Status', 'Model', 'Family', 'Line', 'Platform', 
                            'Product ID Tray', 'Product ID Boxed', 'Product ID MPK',
                            'Launch Date', '# of CPU Cores', '# of Threads', 
                            'Graphics Core Count', 'Base Clock', 'Max. Boost Clock',
                            'All Core Boost Speed', 'L1 Cache', 'L2 Cache', 'L3 Cache',
                            '1kU Pricing', 'Unlocked for Overclocking', 
                            'Processor Technology for CPU Cores', 'CPU Socket',
                            'Socket Count', 'PCI Express Version', 'Thermal Solution PIB',
                            'Recommended Cooler', 'Thermal Solution MPK', 'Default TDP',
                            'AMD Configurable TDP', 'Max. Operating Temperature',
                            'OS Support', 'System Memory Specification', 'System Memory Type',
                            'Memory Channels', 'Per Socket Mem BW', 'Graphics Frequency',
                            'Graphics Model', 'Supported Technologies', 'Workload Affinity',
                            'AMD Ryzen AI'
                        ]
                        
                        for i, line in enumerate(lines[1:], 1):  # Пропускаем заголовок
                            # Проверяем строку 603 (индекс 602)
                            if i == 603:
                                print(f"\n=== Отладка строки 603 ===")
                                print(f"Исходная строка: {line[:200]}...")
                            
                            # Разбиваем строку по запятой, учитывая кавычки
                            parts = []
                            current = ""
                            in_quotes = False
                            for char in line:
                                if char == '"':
                                    in_quotes = not in_quotes
                                elif char == ',' and not in_quotes:
                                    parts.append(current.strip().strip('"'))
                                    current = ""
                                else:
                                    current += char
                            parts.append(current.strip().strip('"'))
                            
                            # Проверяем строку 603
                            if i == 603:
                                print(f"Количество частей: {len(parts)}")
                                for j, part in enumerate(parts[:10]):
                                    print(f"  {j}: '{part}'")
                            
                            # Создаем словарь
                            row = {}
                            for j, header in enumerate(headers):
                                if j < len(parts):
                                    row[header] = parts[j]
                                else:
                                    row[header] = ""
                            
                            # Проверяем строку 603
                            if i == 603:
                                print(f"\nПарсированная запись 603:")
                                print(f"  Model: '{row.get('Model', '')}'")
                                print(f"  Product ID Tray: '{row.get('Product ID Tray', '')}'")
                                print(f"  Product ID Boxed: '{row.get('Product ID Boxed', '')}'")
                                print(f"  Product ID MPK: '{row.get('Product ID MPK', '')}'")
                            
                            data.append(row)
                print(f"Загружено {len(data)} записей из {csv_file} (кодировка: {encoding})")
                return data
            except UnicodeDecodeError:
                continue
        print(f"Не удалось загрузить {csv_file} ни с одной кодировкой")
    except Exception as e:
        print(f"Ошибка при загрузке {csv_file}: {e}")
    return data

def test_amd_200ge_search():
    """Тестирует поиск AMD Athlon 200GE"""
    
    # Загружаем AMD CSV данные
    amd_csv = load_csv_data('amd-cpus.csv')
    print(f"Загружено {len(amd_csv)} записей из amd-cpus.csv")
    
    # Ищем все записи с Athlon 200GE
    athlon_200ge_rows = []
    for i, row in enumerate(amd_csv):
        model = row.get('Model', '')
        family = row.get('Family', '')
        if '200GE' in model or '200GE' in family:
            athlon_200ge_rows.append((i, row))
    
    print(f"\nНайдено {len(athlon_200ge_rows)} записей с 200GE:")
    for i, row in athlon_200ge_rows:
        print(f"\nЗапись {i}:")
        print(f"  Model: '{row.get('Model', '')}'")
        print(f"  Family: '{row.get('Family', '')}'")
        print(f"  Product ID Tray: '{row.get('Product ID Tray', '')}'")
        print(f"  Product ID Boxed: '{row.get('Product ID Boxed', '')}'")
        print(f"  Product ID MPK: '{row.get('Product ID MPK', '')}'")
        print(f"  Base Clock: '{row.get('Base Clock', '')}'")
        print(f"  # of CPU Cores: '{row.get('# of CPU Cores', '')}'")
        print(f"  # of Threads: '{row.get('# of Threads', '')}'")
        print(f"  Graphics Core Count: '{row.get('Graphics Core Count', '')}'")
        print(f"  L2 Cache: '{row.get('L2 Cache', '')}'")
        print(f"  L3 Cache: '{row.get('L3 Cache', '')}'")
        print(f"  CPU Socket: '{row.get('CPU Socket', '')}'")
        print(f"  AMD Configurable TDP: '{row.get('AMD Configurable TDP', '')}'")
        print(f"  Graphics Model: '{row.get('Graphics Model', '')}'")
    
    # Ищем конкретно AMD Athlon 200GE
    athlon_200ge_row = None
    for row in amd_csv:
        if row.get('Model', '') == 'AMD Athlon 200GE':
            athlon_200ge_row = row
            break
    
    if athlon_200ge_row:
        print("\n=== Найдена точная запись AMD Athlon 200GE ===")
        print(f"Model: {athlon_200ge_row.get('Model', '')}")
        print(f"Product ID Tray: '{athlon_200ge_row.get('Product ID Tray', '')}'")
        print(f"Product ID Boxed: '{athlon_200ge_row.get('Product ID Boxed', '')}'")
        print(f"Product ID MPK: '{athlon_200ge_row.get('Product ID MPK', '')}'")
        print(f"Base Clock: {athlon_200ge_row.get('Base Clock', '')}")
        print(f"# of CPU Cores: {athlon_200ge_row.get('# of CPU Cores', '')}")
        print(f"# of Threads: {athlon_200ge_row.get('# of Threads', '')}")
        print(f"Graphics Core Count: {athlon_200ge_row.get('Graphics Core Count', '')}")
        print(f"L2 Cache: {athlon_200ge_row.get('L2 Cache', '')}")
        print(f"L3 Cache: {athlon_200ge_row.get('L3 Cache', '')}")
        print(f"CPU Socket: {athlon_200ge_row.get('CPU Socket', '')}")
        print(f"AMD Configurable TDP: {athlon_200ge_row.get('AMD Configurable TDP', '')}")
        print(f"Graphics Model: {athlon_200ge_row.get('Graphics Model', '')}")
    else:
        print("\nЗапись AMD Athlon 200GE не найдена!")
        return
    
    # Тестируем поиск по артикулу
    cpu_name = "Процессор AMD Athlon 200GE AM4 (YD200GC6M2OFB) (3.2GHz/100MHz/Radeon Vega 3) Tray"
    article_match = re.search(r'\(([A-Z0-9]+)\)', cpu_name)
    article = article_match.group(1) if article_match else ""
    
    print(f"\n=== Тестируем поиск для CPU ===")
    print(f"CPU: {cpu_name}")
    print(f"Извлеченный article: '{article}'")
    
    # Проверяем точное совпадение
    product_id_tray = athlon_200ge_row.get('Product ID Tray', '')
    product_id_boxed = athlon_200ge_row.get('Product ID Boxed', '')
    product_id_mpk = athlon_200ge_row.get('Product ID MPK', '')
    
    print(f"\n=== Проверяем совпадения ===")
    print(f"Product ID Tray: '{product_id_tray}' == '{article}': {article == product_id_tray}")
    print(f"Product ID Boxed: '{product_id_boxed}' == '{article}': {article == product_id_boxed}")
    print(f"Product ID MPK: '{product_id_mpk}' == '{article}': {article == product_id_mpk}")
    
    # Проверяем включение
    print(f"\n=== Проверяем включения ===")
    print(f"'{article}' in '{product_id_tray}': {article in product_id_tray}")
    print(f"'{article}' in '{product_id_boxed}': {article in product_id_boxed}")
    print(f"'{article}' in '{product_id_mpk}': {article in product_id_mpk}")

if __name__ == "__main__":
    test_amd_200ge_search() 