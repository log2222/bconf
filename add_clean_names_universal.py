import json
import re

def extract_intel_clean_name(cpu_data):
    """Извлекает чистое имя для Intel процессоров из enrichment_data["CpuName"]"""
    enrichment = cpu_data.get('enrichment_data', {})
    cpu_name = enrichment.get('CpuName', '')
    if not cpu_name or 'Intel' not in cpu_name:
        return None
    clean_name = cpu_name.replace('®', '').replace('™', '').replace('Processor', '').strip()
    return clean_name

def extract_amd_clean_name(cpu_data):
    """Извлекает чистое имя для AMD процессоров из enrichment_data"""
    enrichment = cpu_data.get('enrichment_data', {})
    name = cpu_data.get('name', '')
    if 'Athlon' in name:
        model = enrichment.get('Model', '')
        family = enrichment.get('Family', '')
        if model and len(model) > 8 and 'Athlon' in model:
            clean_name = model.replace('(OEM Only)', '').replace('7th Gen ', '').replace(' APU', '').strip()
            return clean_name
        elif family:
            clean_name = family.replace('(OEM Only)', '').replace('7th Gen ', '').replace(' APU', '').strip()
            return clean_name
    else:
        family = enrichment.get('Family', '')
        if family and 'AMD' in family:
            clean_name = family.replace('(OEM Only)', '').replace('7th Gen ', '').replace(' APU', '').strip()
            return clean_name
    return None

def extract_clean_name_from_name(cpu_data):
    """Извлекает чистое имя из поля name для необогащенных процессоров"""
    name = cpu_data.get('name', '')
    
    if not name:
        return None
    
    # Убираем лишние слова
    clean_name = name.replace("Процессор", "").replace("Processor", "").strip()
    
    # Убираем технические характеристики в скобках
    import re
    clean_name = re.sub(r'\s*\([^)]*\)', '', clean_name)
    
    # Убираем лишние пробелы
    clean_name = ' '.join(clean_name.split())
    
    return clean_name

def add_clean_names():
    """Добавляет clean_name для всех процессоров"""
    # Загружаем данные
    with open('components.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    cpus = data.get('CPU', [])
    added_count = 0
    updated_count = 0
    
    for cpu in cpus:
        name = cpu.get('name', '')
        enriched = cpu.get('enriched', False)
        
        clean_name = None
        
        if enriched:
            # Для обогащенных процессоров
            if 'Intel' in name:
                clean_name = extract_intel_clean_name(cpu)
            elif 'AMD' in name:
                clean_name = extract_amd_clean_name(cpu)
        else:
            # Для необогащенных процессоров
            clean_name = extract_clean_name_from_name(cpu)
        
        if clean_name:
            if 'clean_name' not in cpu:
                cpu['clean_name'] = clean_name
                added_count += 1
                print(f"Добавлен clean_name: {clean_name}")
                print(f"  Для: {name}")
                print()
            else:
                old_clean_name = cpu['clean_name']
                cpu['clean_name'] = clean_name
                updated_count += 1
                print(f"Обновлен clean_name: {old_clean_name} → {clean_name}")
                print(f"  Для: {name}")
                print()
    
    # Сохраняем обновленные данные
    with open('components.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"Добавлено clean_name для {added_count} процессоров")
    print(f"Обновлено clean_name для {updated_count} процессоров")
    print("Файл components.json обновлен")

if __name__ == "__main__":
    add_clean_names() 