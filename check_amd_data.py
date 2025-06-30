import csv

def check_amd_data():
    """Проверяет структуру AMD данных"""
    
    # Читаем файл построчно
    with open('amd-cpus.csv', 'r', encoding='cp1252') as f:
        lines = f.readlines()
    
    print(f"Всего строк: {len(lines)}")
    
    # Парсим вручную
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
        
        # Создаем словарь
        row = {}
        for i, header in enumerate(headers):
            if i < len(parts):
                row[header] = parts[i]
            else:
                row[header] = ""
        data.append(row)
    
    print(f"Загружено {len(data)} записей")
    
    # Показываем первые 3 записи с ключевыми полями
    for i, row in enumerate(data[:3]):
        print(f"\nЗапись {i+1}:")
        print(f"  Status: {row.get('Status', 'НЕТ')}")
        print(f"  Model: {row.get('Model', 'НЕТ')}")
        print(f"  Family: {row.get('Family', 'НЕТ')}")
        print(f"  Product ID Tray: {row.get('Product ID Tray', 'НЕТ')}")
        print(f"  Product ID Boxed: {row.get('Product ID Boxed', 'НЕТ')}")
        print(f"  Product ID MPK: {row.get('Product ID MPK', 'НЕТ')}")
    
    # Ищем строку с YD1200BBM4KAE
    target_article = "YD1200BBM4KAE"
    print(f"\nИщем article: {target_article}")
    
    for i, row in enumerate(data):
        for key in ['Product ID Tray', 'Product ID Boxed', 'Product ID MPK']:
            value = row.get(key, '')
            if target_article in value:
                print(f"Найдено в {key} (строка {i+1}): {value}")
                print(f"Модель: {row.get('Model', 'НЕТ')}")
                return
    
    print(f"Article {target_article} не найден")

if __name__ == "__main__":
    check_amd_data() 