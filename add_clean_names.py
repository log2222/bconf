import json
import re

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
    """Извлекает чистое название процессора AMD из поля Family или оригинального названия"""
    if not family and not original_name:
        return ""
    
    # Если есть Family, используем его
    if family:
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
    
    # Если нет Family, извлекаем из оригинального названия
    if original_name:
        # Паттерны для извлечения коротких названий
        patterns = [
            r'AMD\s+(A\d+)\s+(\d+)',  # AMD A6 9500
            r'AMD\s+(Athlon\s+\d+[A-Z]*)',  # AMD Athlon 200GE
            r'AMD\s+(Ryzen\s+\d+\s+\d+[A-Z]*)',  # AMD Ryzen 5 2600
            r'AMD\s+(Ryzen\s+Threadripper\s+\d+[A-Z]*)',  # AMD Ryzen Threadripper 2970W
        ]
        
        for pattern in patterns:
            match = re.search(pattern, original_name, re.IGNORECASE)
            if match:
                if len(match.groups()) == 2:
                    return f"AMD {match.group(1)} {match.group(2)}"
                else:
                    return f"AMD {match.group(1)}"
    
    return ""

def add_clean_names_to_all_cpus():
    """Добавляет clean_name для всех процессоров, которые его не имеют"""
    
    # Загружаем данные
    with open('components.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    added_count = 0
    updated_count = 0
    
    for cpu in data['CPU']:
        # Проверяем, есть ли уже clean_name
        if 'clean_name' not in cpu or not cpu['clean_name']:
            clean_name = ""
            
            # Для Intel процессоров
            if "Intel" in cpu['name'].upper():
                if cpu.get('enrichment_data', {}).get('CpuName'):
                    clean_name = extract_clean_intel_name(cpu['enrichment_data']['CpuName'])
                else:
                    # Если нет enrichment_data, извлекаем из name
                    clean_name = extract_clean_intel_name(cpu['name'])
            
            # Для AMD процессоров
            elif "AMD" in cpu['name'].upper():
                if cpu.get('enrichment_data', {}).get('Family'):
                    clean_name = extract_clean_amd_name(cpu['enrichment_data']['Family'], cpu['name'])
                else:
                    # Если нет enrichment_data, извлекаем из name
                    clean_name = extract_clean_amd_name("", cpu['name'])
            
            # Добавляем clean_name, если удалось извлечь
            if clean_name:
                cpu['clean_name'] = clean_name
                added_count += 1
                print(f"Добавлен clean_name: {clean_name}")
                print(f"  Для: {cpu['name']}")
                print()
        
        # Обновляем существующие clean_name для AMD (убираем лишние слова)
        elif cpu.get('clean_name') and "AMD" in cpu['clean_name'].upper():
            old_clean_name = cpu['clean_name']
            new_clean_name = extract_clean_amd_name(old_clean_name, cpu['name'])
            if new_clean_name != old_clean_name:
                cpu['clean_name'] = new_clean_name
                updated_count += 1
                print(f"Обновлен clean_name: {old_clean_name} -> {new_clean_name}")
                print(f"  Для: {cpu['name']}")
                print()
    
    # Сохраняем обновленные данные
    with open('components.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"Добавлено clean_name для {added_count} процессоров")
    print(f"Обновлено clean_name для {updated_count} процессоров")
    print("Файл components.json обновлен")

if __name__ == "__main__":
    add_clean_names_to_all_cpus() 