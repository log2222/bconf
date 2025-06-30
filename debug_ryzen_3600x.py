import json
import csv
import re
from typing import Dict, List, Optional

def load_csv_data(csv_file: str) -> List[Dict]:
    """Загружает данные из CSV файла"""
    data = []
    try:
        with open(csv_file, 'r', encoding='latin-1') as f:
            lines = f.readlines()
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
                if len(parts) == 1:
                    parts = [p.strip(' "') for p in line.split(',')]
                row = {}
                for i, header in enumerate(headers):
                    if i < len(parts):
                        row[header] = parts[i]
                    else:
                        row[header] = ""
                data.append(row)
        print(f"Загружено {len(data)} записей из {csv_file}")
        return data
    except Exception as e:
        print(f"Ошибка при загрузке {csv_file}: {e}")
        return data

def extract_cpu_model(name: str) -> str:
    """Извлекает и нормализует модель CPU из названия"""
    name = str(name).upper()
    
    # Core iX-YYYYSUFFIX (например, i3-9100F, i5-10400F, i7-8700K)
    core_ix_full = re.search(r'CORE\s+I([3579])\s+(\d{4})([A-Z]*)', name)
    if core_ix_full:
        ix = core_ix_full.group(1)
        number = core_ix_full.group(2)
        suffix = core_ix_full.group(3)
        return f"i{ix}-{number}{suffix}"
    
    # Core iX YYYYSUFFIX (без дефиса)
    core_ix_full2 = re.search(r'CORE\s+I([3579])\s*(\d{4})([A-Z]*)', name)
    if core_ix_full2:
        ix = core_ix_full2.group(1)
        number = core_ix_full2.group(2)
        suffix = core_ix_full2.group(3)
        return f"i{ix}-{number}{suffix}"
    
    # Старые паттерны
    patterns = [
        r'CORE\s+I[3579][ -]?\d{4}[A-Z]*',
        r'I[3579][ -]?\d{4}[A-Z]*',
        r'PENTIUM\s+DUAL-CORE\s+[A-Z0-9]+',
        r'PENTIUM\s+[A-Z0-9]+',
        r'CELERON\s+[A-Z0-9]+',
        r'RYZEN\s+[3579]\s+[0-9]+[A-Z]*[0-9]*',
        r'ATHLON\s+[0-9]+[A-Z]*[0-9]*',
        r'FX\s*[-]?\s*[0-9]+[A-Z]*[0-9]*',
        r'A[0-9]\s*[-]?\s*[0-9]+[A-Z]*[0-9]*',
    ]
    for pattern in patterns:
        match = re.search(pattern, name)
        if match:
            model = match.group(0)
            model = re.sub(r'\s+', '-', model)
            model = re.sub(r'-+', '-', model)
            model = model.strip('-')
            return model
    return ""

def normalize_model(model: str) -> str:
    """Нормализует модель CPU для сравнения"""
    if not model:
        return ""
    normalized = model.lower()
    normalized = re.sub(
        r'(intel|amd|core|ryzen|athlon|pentium|celeron|threadripper|dual-core|gold|silver|platinum|pro|extreme|edition|processor|cpu|x-series|series|™|®|with radeon vega graphics|with radeon graphics|radeon vega|radeon|graphics|box|oem|tray)',
        '', normalized)
    normalized = re.sub(r'[^a-z0-9]', '', normalized)
    return normalized

def find_best_match(cpu_name: str, csv_data: List[Dict], vendor: str = "amd") -> Optional[Dict]:
    """Находит лучшее совпадение CPU в CSV данных"""
    extracted_model = extract_cpu_model(cpu_name)
    if not extracted_model:
        print(f"Не удалось извлечь модель из: {cpu_name}")
        return None
    
    print(f"Ищем совпадение для модели: '{extracted_model}' в CPU: '{cpu_name}' (vendor={vendor})")
    normalized_extracted = normalize_model(extracted_model)
    print(f"Нормализованная модель: '{normalized_extracted}'")
    
    # Извлекаем article из названия CPU
    article_match = re.search(r'\(([A-Z0-9]+)\)', cpu_name)
    article = article_match.group(1) if article_match else ""
    if article:
        print(f"Извлеченный article: '{article}'")
    
    if vendor == "amd":
        # Определяем серию процессора
        cpu_series = ""
        if "ATHLON" in cpu_name.upper():
            cpu_series = "ATHLON"
        elif "RYZEN" in cpu_name.upper():
            cpu_series = "RYZEN"
        elif "THREADRIPPER" in cpu_name.upper():
            cpu_series = "THREADRIPPER"
        
        print(f"Серия процессора: {cpu_series}")
        
        # Сначала ищем по article (Product ID Tray/Boxed/MPK)
        if article:
            print(f"\nПоиск по article '{article}':")
            for i, row in enumerate(csv_data):
                for key in ['Product ID Tray', 'Product ID Boxed', 'Product ID MPK']:
                    product_ids = row.get(key, '')
                    if product_ids:
                        # Разбиваем по / и убираем пробелы
                        for pid in product_ids.split('/'):
                            pid = pid.strip()
                            if article == pid:
                                print(f"  Найдено совпадение в строке {i+1}:")
                                print(f"    {key}: {pid}")
                                print(f"    Model: {row.get('Model', '')}")
                                print(f"    Family: {row.get('Family', '')}")
                                print(f"    Line: {row.get('Line', '')}")
                                
                                # Дополнительно проверяем серию
                                if cpu_series:
                                    model = row.get('Model', '')
                                    family = row.get('Family', '')
                                    line = row.get('Line', '')
                                    row_series = ''
                                    # Если Model невалиден (короткий или "on"), определяем серию только по Family и Line
                                    if not model or model == 'on' or len(model) < 8:
                                        if 'ATHLON' in (family + line).upper():
                                            row_series = 'ATHLON'
                                        elif 'RYZEN' in (family + line).upper():
                                            row_series = 'RYZEN'
                                        elif 'THREADRIPPER' in (family + line).upper():
                                            row_series = 'THREADRIPPER'
                                        else:
                                            print(f"    Не удалось определить серию для строки {i+1}")
                                            continue
                                    else:
                                        if 'ATHLON' in (model + family + line).upper():
                                            row_series = 'ATHLON'
                                        elif 'RYZEN' in (model + family + line).upper():
                                            row_series = 'RYZEN'
                                        elif 'THREADRIPPER' in (model + family + line).upper():
                                            row_series = 'THREADRIPPER'
                                    
                                    print(f"    Определенная серия строки: {row_series}")
                                    if row_series and row_series != cpu_series:
                                        print(f"    Серии не совпадают: {row_series} != {cpu_series}")
                                        continue
                                
                                print(f"    ✓ Возвращаем эту строку")
                                return row
                            else:
                                print(f"    Строка {i+1}, {key}: '{pid}' != '{article}'")
        
        # Затем ищем по Model с проверкой серии
        print(f"\nПоиск по Model '{normalized_extracted}':")
        for i, row in enumerate(csv_data):
            model = row.get('Model', '')
            family = row.get('Family', '')
            line = row.get('Line', '')
            
            # Проверяем, что серия совпадает
            if cpu_series:
                row_series = ""
                if "ATHLON" in (model + family + line).upper():
                    row_series = "ATHLON"
                elif "RYZEN" in (model + family + line).upper():
                    row_series = "RYZEN"
                elif "THREADRIPPER" in (model + family + line).upper():
                    row_series = "THREADRIPPER"
                
                # Если серии не совпадают, пропускаем
                if row_series and row_series != cpu_series:
                    continue
            
            if model and normalize_model(model) == normalized_extracted:
                print(f"  Найдено по Model в строке {i+1}: {model}")
                return row
        
        # Затем ищем по Family с проверкой серии
        print(f"\nПоиск по Family (включение '{normalized_extracted}'):")
        for i, row in enumerate(csv_data):
            family = row.get('Family', '')
            
            # Проверяем, что серия совпадает
            if cpu_series:
                row_series = ""
                if "ATHLON" in family.upper():
                    row_series = "ATHLON"
                elif "RYZEN" in family.upper():
                    row_series = "RYZEN"
                elif "THREADRIPPER" in family.upper():
                    row_series = "THREADRIPPER"
                
                # Если серии не совпадают, пропускаем
                if row_series and row_series != cpu_series:
                    continue
            
            if family and normalized_extracted in normalize_model(family):
                print(f"  Найдено по Family в строке {i+1}: {family}")
                return row
    
    return None

def main():
    # Загружаем CSV данные
    amd_csv = load_csv_data('amd-cpus.csv')
    
    # Тестируем конкретный случай
    cpu_name = "Процессор AMD Ryzen 5 3600X AM4 (100-100000022BOX) (3.8GHz) Box"
    
    print("=" * 80)
    print(f"Тестируем CPU: {cpu_name}")
    print("=" * 80)
    
    match = find_best_match(cpu_name, amd_csv, "amd")
    
    if match:
        print(f"\n✓ Найдено совпадение:")
        print(f"  Model: {match.get('Model', '')}")
        print(f"  Family: {match.get('Family', '')}")
        print(f"  Line: {match.get('Line', '')}")
        print(f"  Product ID Boxed: {match.get('Product ID Boxed', '')}")
    else:
        print(f"\n✗ Совпадение не найдено")

if __name__ == "__main__":
    main() 