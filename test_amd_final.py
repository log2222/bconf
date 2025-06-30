import csv

def test_amd_final():
    """Тестирует поиск по article в AMD данных"""
    
    # Читаем файл построчно
    with open('amd-cpus.csv', 'r', encoding='cp1252') as f:
        lines = f.readlines()
    
    print(f"Всего строк: {len(lines)}")
    
    # Парсим вручную с исправленным парсером
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
    
    data = []
    for line in lines[1:]:  # Пропускаем заголовок
        # Простой парсинг по запятой, учитывая кавычки
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
        
        # Создаем словарь
        row = {}
        for i, header in enumerate(headers):
            if i < len(parts):
                row[header] = parts[i]
            else:
                row[header] = ""
        data.append(row)
    
    print(f"Загружено {len(data)} записей")
    
    # Ищем конкретный article
    target_article = "YD1200BBM4KAE"
    print(f"\nИщем article: {target_article}")
    
    found = False
    for i, row in enumerate(data):
        product_id_tray = row.get('Product ID Tray', '')
        product_id_boxed = row.get('Product ID Boxed', '')
        product_id_mpk = row.get('Product ID MPK', '')
        
        if product_id_tray == target_article:
            print(f"Найдено в Product ID Tray (строка {i+1}): {product_id_tray}")
            print(f"Модель: {row.get('Model', 'НЕТ')}")
            print(f"Семейство: {row.get('Family', 'НЕТ')}")
            found = True
            break
        elif product_id_boxed == target_article:
            print(f"Найдено в Product ID Boxed (строка {i+1}): {product_id_boxed}")
            print(f"Модель: {row.get('Model', 'НЕТ')}")
            print(f"Семейство: {row.get('Family', 'НЕТ')}")
            found = True
            break
        elif product_id_mpk == target_article:
            print(f"Найдено в Product ID MPK (строка {i+1}): {product_id_mpk}")
            print(f"Модель: {row.get('Model', 'НЕТ')}")
            print(f"Семейство: {row.get('Family', 'НЕТ')}")
            found = True
            break
    
    if not found:
        print(f"Article {target_article} не найден")
        
        # Показываем несколько примеров Product ID Tray
        print("\nПримеры Product ID Tray:")
        count = 0
        for row in data:
            product_id_tray = row.get('Product ID Tray', '')
            if product_id_tray and count < 10:
                print(f"  {product_id_tray} -> {row.get('Model', 'НЕТ')}")
                count += 1
        
        # Показываем строку 261 (где должен быть YD1200BBM4KAE)
        if len(data) >= 260:
            row_261 = data[259]  # 0-based index
            print(f"\nСтрока 261:")
            print(f"  Status: {row_261.get('Status', 'НЕТ')}")
            print(f"  Model: {row_261.get('Model', 'НЕТ')}")
            print(f"  Family: {row_261.get('Family', 'НЕТ')}")
            print(f"  Product ID Tray: {row_261.get('Product ID Tray', 'НЕТ')}")
            print(f"  Product ID Boxed: {row_261.get('Product ID Boxed', 'НЕТ')}")
            print(f"  Product ID MPK: {row_261.get('Product ID MPK', 'НЕТ')}")

if __name__ == "__main__":
    test_amd_final() 