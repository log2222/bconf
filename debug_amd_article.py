import json
import csv
import re
import os
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
                    else:
                        reader = csv.DictReader(lines)
                        for row in reader:
                            data.append(row)
                print(f"Загружено {len(data)} записей из {csv_file} (кодировка: {encoding})")
                return data
            except UnicodeDecodeError:
                continue
        print(f"Не удалось загрузить {csv_file} ни с одной кодировкой")
    except Exception as e:
        print(f"Ошибка при загрузке {csv_file}: {e}")
    return data

def debug_amd_article():
    """Отладка поиска по article в AMD данных"""
    
    amd_csv = load_csv_data('amd-cpus.csv')
    
    if not amd_csv:
        print("Не удалось загрузить AMD CSV")
        return
    
    # Ищем конкретный article
    target_article = "YD1200BBM4KAE"
    print(f"\nИщем article: {target_article}")
    
    found = False
    for i, row in enumerate(amd_csv):
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
        for row in amd_csv:
            product_id_tray = row.get('Product ID Tray', '')
            if product_id_tray and count < 10:
                print(f"  {product_id_tray} -> {row.get('Model', 'НЕТ')}")
                count += 1

if __name__ == "__main__":
    debug_amd_article() 