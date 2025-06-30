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
                            # Если parts всего 1 (вся строка), делаем split(',') без учёта кавычек
                            if len(parts) == 1:
                                parts = [p.strip(' "') for p in line.split(',')]
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

def extract_clean_intel_name(cpu_name: str) -> str:
    """Извлекает чистое название процессора Intel из поля CpuName"""
    if not cpu_name:
        return ""
    
    # Убираем лишние символы и слова
    clean_name = cpu_name
    
    # Убираем торговые марки
    clean_name = re.sub(r'Intel®\s*', 'Intel ', clean_name)
    clean_name = re.sub(r'™\s*', ' ', clean_name)  # Заменяем на пробел
    clean_name = re.sub(r'®\s*', ' ', clean_name)  # Заменяем на пробел
    
    # Убираем слово "Processor" в конце
    clean_name = re.sub(r'\s+Processor\s*$', '', clean_name)
    
    # Убираем слово "Processor" в середине (если есть)
    clean_name = re.sub(r'\s+Processor\s+', ' ', clean_name)
    
    # Убираем лишние пробелы (но сохраняем один пробел между словами)
    clean_name = re.sub(r'\s+', ' ', clean_name)
    clean_name = clean_name.strip()
    
    return clean_name

def extract_clean_amd_name(family: str, original_name: str = "") -> str:
    """Извлекает чистое название процессора AMD из поля Family"""
    if not family:
        return ""
    
    # Проверяем, является ли это старой моделью AMD (A-серия)
    if "7th Gen" in family or "APU" in family:
        # Для старых моделей извлекаем из оригинального названия
        if original_name:
            # Ищем паттерн "AMD A6 9500" или "AMD A10 9700" и т.д.
            match = re.search(r'AMD\s+(A\d+)\s+(\d+)', original_name, re.IGNORECASE)
            if match:
                return f"AMD {match.group(1)} {match.group(2)}"
    
    clean_name = family
    # Обрезаем по 'with', 'с', 'с графикой', 'с видеоядром' и т.п.
    clean_name = re.split(r' with | с | с графикой| с видеоядром', clean_name, flags=re.IGNORECASE)[0]
    clean_name = re.sub(r'\s+', ' ', clean_name)
    clean_name = clean_name.strip()
    return clean_name

def extract_cpu_model(name: str) -> str:
    """Извлекает и нормализует модель CPU из названия, включая суффиксы (F, K, T и др.)"""
    name = str(name).upper()
    
    # Pentium Gold
    pentium_gold_match = re.search(r'PENTIUM\s+GOLD\s+([A-Z0-9]+)', name)
    if pentium_gold_match:
        return f"PENTIUM GOLD {pentium_gold_match.group(1)}"
    
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
    
    # Старые паттерны (оставляем для совместимости)
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
    """Нормализует модель CPU для сравнения (универсально для Intel, AMD, Ryzen, и др.)"""
    if not model:
        return ""
    normalized = model.lower()
    # Удаляем все маркетинговые слова и спецсимволы
    normalized = re.sub(
        r'(intel|amd|core|ryzen|athlon|pentium|celeron|threadripper|dual-core|gold|silver|platinum|pro|extreme|edition|processor|cpu|x-series|series|™|®|with radeon vega graphics|with radeon graphics|radeon vega|radeon|graphics|box|oem|tray)',
        '', normalized)
    normalized = re.sub(r'[^a-z0-9]', '', normalized)  # Оставляем только буквы и цифры
    return normalized

def find_best_match(cpu_name: str, csv_data: List[Dict], model_column: str, vendor: str = "intel") -> Optional[Dict]:
    """Находит лучшее совпадение CPU в CSV данных (учитывает vendor)"""
    extracted_model = extract_cpu_model(cpu_name)
    if not extracted_model:
        print(f"Не удалось извлечь модель из: {cpu_name}")
        return None
    
    print(f"Ищем совпадение для модели: '{extracted_model}' в CPU: '{cpu_name}' (vendor={vendor})")
    normalized_extracted = normalize_model(extracted_model)
    print(f"Нормализованная модель: '{normalized_extracted}'")
    
    # Извлекаем article из названия CPU (например, YD1200BBM4KAE)
    article_match = re.search(r'\(([A-Z0-9]+)\)', cpu_name)
    article = article_match.group(1) if article_match else ""
    if article:
        print(f"Извлеченный article: '{article}'")
    
    if vendor == "intel":
        # Сначала ищем по ProcessorNumber
        for row in csv_data:
            proc_num = row.get('ProcessorNumber', '')
            if proc_num and normalize_model(proc_num) == normalized_extracted:
                print(f"Найдено по ProcessorNumber: {proc_num}")
                return row
        # Затем ищем по CpuName
        for row in csv_data:
            csv_model = row.get('CpuName', '')
            if csv_model and normalize_model(csv_model) == normalized_extracted:
                print(f"Найдено по CpuName: {csv_model}")
                return row
    elif vendor == "amd":
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
            for row in csv_data:
                for key in ['Product ID Tray', 'Product ID Boxed', 'Product ID MPK']:
                    product_ids = row.get(key, '')
                    if product_ids:
                        # Разбиваем по / и убираем пробелы
                        for pid in product_ids.split('/'):
                            pid = pid.strip()
                            if article == pid:
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
                                            # Если не удалось определить серию — пропускаем совпадение
                                            continue
                                    else:
                                        if 'ATHLON' in (model + family + line).upper():
                                            row_series = 'ATHLON'
                                        elif 'RYZEN' in (model + family + line).upper():
                                            row_series = 'RYZEN'
                                        elif 'THREADRIPPER' in (model + family + line).upper():
                                            row_series = 'THREADRIPPER'
                                    if row_series and row_series != cpu_series:
                                        continue
                                print(f"Найдено по {key}: {pid}")
                                return row
        
        # Затем ищем по Model с проверкой серии
        for row in csv_data:
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
                print(f"Найдено по Model: {model}")
                return row
        
        # Затем ищем по Family с проверкой серии
        for row in csv_data:
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
            
            # --- STRICT SUFFIX CHECK ---
            def extract_suffix(s):
                s = s.upper().replace(" ", "")
                m = re.search(r'(\d{4,5})([A-Z]*)$', s)
                if m:
                    return m.group(2)  # e.g. '', 'X', 'XT', 'G', etc.
                return ''
            fam_norm = normalize_model(family)
            ext_norm = normalized_extracted
            if fam_norm and ext_norm in fam_norm:
                # Extract numeric part and suffix for both
                fam_suffix = extract_suffix(family)
                ext_suffix = extract_suffix(extracted_model)
                # Only allow match if suffixes are exactly the same
                if fam_suffix != ext_suffix:
                    continue
                print(f"Включение в Family: {family}")
                return row
    
    # Старый fallback: ищем по включению
    for row in csv_data:
        for key in ['ProcessorNumber', 'CpuName', 'Model', 'Family', 'Line']:
            val = row.get(key, '')
            if val and normalized_extracted in normalize_model(val):
                print(f"Включение в {key}: {val}")
                return row
    
    return None

def enrich_cpu_data():
    """Обогащает данные CPU из CSV файлов"""
    print("Загружен JSON файл")
    
    # Загружаем CSV данные
    intel_csv = load_csv_data('intel-cpus.csv')
    amd_csv = load_csv_data('amd-cpus.csv')
    
    # Загружаем JSON
    with open('components.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    enriched_count = 0
    for cpu in data['CPU']:
        name = cpu['name']
        
        # Определяем vendor
        if "AMD" in name.upper() or "RYZEN" in name.upper() or "ATHLON" in name.upper():
            vendor = "amd"
            csv_data = amd_csv
            model_column = "Model"
        else:
            vendor = "intel"
            csv_data = intel_csv
            model_column = "CpuName"
        
        match = find_best_match(name, csv_data, model_column, vendor)
        
        if match:
            # Обогащаем данные
            cpu['enriched'] = True
            cpu['enrichment_data'] = match
            
            # Для Intel процессоров добавляем чистое название из CpuName
            if vendor == "intel" and match.get('CpuName'):
                clean_name = extract_clean_intel_name(match['CpuName'])
                if clean_name:
                    cpu['clean_name'] = clean_name
            
            # Для AMD процессоров добавляем чистое название
            if vendor == "amd":
                # Для Athlon серии берем из Model, если он валиден, иначе из Family
                if "ATHLON" in name.upper():
                    model = match.get('Model', '')
                    family = match.get('Family', '')
                    if model and len(model) > 8 and 'Athlon' in model:
                        clean_name = extract_clean_amd_name(model, name)
                    elif family:
                        clean_name = extract_clean_amd_name(family, name)
                    else:
                        clean_name = None
                    if clean_name:
                        cpu['clean_name'] = clean_name
                else:
                    if match.get('Family'):
                        clean_name = extract_clean_amd_name(match['Family'], name)
                        if clean_name:
                            cpu['clean_name'] = clean_name
            
            enriched_count += 1
            print(f"Обогащён: {name}")
        else:
            print(f"Совпадение не найдено для: {name}")
    
    # Сохраняем обновленные данные
    with open('components.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\nОбогащено {enriched_count} CPU из {len(data['CPU'])}")
    print("Обновлённый файл сохранён: components.json")
    
    # Показываем не обогащенные CPU
    not_enriched = [cpu['name'] for cpu in data['CPU'] if not cpu.get('enriched', False)]
    if not_enriched:
        print("\nНе обогащены:")
        for name in not_enriched:
            print(name)

if __name__ == "__main__":
    enrich_cpu_data() 