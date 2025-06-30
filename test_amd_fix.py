import csv

def test_amd_parsing():
    """Тестирует парсинг AMD CSV"""
    
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
    
    # Показываем первые 3 записи
    for i, row in enumerate(data[:3]):
        print(f"\nЗапись {i+1}:")
        for key, value in row.items():
            if value:  # Показываем только непустые значения
                print(f"  {key}: {value}")
    
    # Ищем конкретный article
    target_article = "YD1200BBM4KAE"
    print(f"\nИщем article: {target_article}")
    
    found = False
    for row in data:
        product_id_tray = row.get('Product ID Tray', '')
        if product_id_tray == target_article:
            print(f"Найдено в Product ID Tray: {product_id_tray}")
            print(f"Модель: {row.get('Model', 'НЕТ')}")
            found = True
            break
    
    if not found:
        print(f"Article {target_article} не найден")

if __name__ == "__main__":
    test_amd_parsing() 