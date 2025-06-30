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
                            # Простой парсинг по запятой, игнорируя кавычки
                            parts = line.split(',')
                            parts = [part.strip().strip('"') for part in parts]
                            
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
        # Сначала ищем по article (Product ID Tray)
        if article:
            for row in csv_data:
                product_id_tray = row.get('Product ID Tray', '')
                if product_id_tray and article == product_id_tray:
                    print(f"Найдено по Product ID Tray: {product_id_tray}")
                    return row
                product_id_boxed = row.get('Product ID Boxed', '')
                if product_id_boxed and article == product_id_boxed:
                    print(f"Найдено по Product ID Boxed: {product_id_boxed}")
                    return row
                product_id_mpk = row.get('Product ID MPK', '')
                if product_id_mpk and article == product_id_mpk:
                    print(f"Найдено по Product ID MPK: {product_id_mpk}")
                    return row
        
        # Затем ищем по Model
        for row in csv_data:
            model = row.get('Model', '')
            if model and normalize_model(model) == normalized_extracted:
                print(f"Найдено по Model: {model}")
                return row
        
        # Затем ищем по названию (fallback)
        for row in csv_data:
            for key in ['Model', 'Family', 'Line']:
                val = row.get(key, '')
                if val and normalized_extracted in normalize_model(val):
                    print(f"Включение в {key}: {val}")
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