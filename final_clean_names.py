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

# Загружаем обогащенные данные
with open('components.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("=== Тестирование чистых названий Intel процессоров ===\n")

intel_count = 0
for cpu in data['CPU']:
    if cpu.get('enriched') and cpu.get('enrichment_data') and 'Intel' in cpu['name']:
        enrichment_data = cpu['enrichment_data']
        cpu_name_field = enrichment_data.get('CpuName', '')
        
        if cpu_name_field:
            clean_name = extract_clean_intel_name(cpu_name_field)
            print(f"Оригинальное название: {cpu_name_field}")
            print(f"Чистое название: {clean_name}")
            print(f"Исходное название: {cpu['name']}")
            print("-" * 80)
            intel_count += 1
            
            if intel_count >= 10:  # Показываем только первые 10 для примера
                break

print(f"\nПроверено {intel_count} Intel процессоров") 