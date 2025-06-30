import json

def test_amd_clean_names():
    """Тестирует чистые названия AMD процессоров"""
    
    # Загружаем обогащенные данные
    with open('components.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Ищем AMD процессоры с clean_name
    amd_cpus_with_clean_names = []
    amd_cpus_without_clean_names = []
    
    for cpu in data['CPU']:
        if "AMD" in cpu['name'].upper() or "RYZEN" in cpu['name'].upper() or "ATHLON" in cpu['name'].upper():
            if cpu.get('enriched') and cpu.get('clean_name'):
                amd_cpus_with_clean_names.append({
                    'name': cpu['name'],
                    'clean_name': cpu['clean_name'],
                    'family': cpu.get('enrichment_data', {}).get('Family', 'N/A')
                })
            elif cpu.get('enriched'):
                amd_cpus_without_clean_names.append({
                    'name': cpu['name'],
                    'family': cpu.get('enrichment_data', {}).get('Family', 'N/A')
                })
    
    print(f"AMD процессоры с чистыми названиями: {len(amd_cpus_with_clean_names)}")
    print(f"AMD процессоры без чистых названий: {len(amd_cpus_without_clean_names)}")
    
    print("\n=== AMD процессоры с чистыми названиями ===")
    for cpu in amd_cpus_with_clean_names[:10]:  # Показываем первые 10
        print(f"Оригинал: {cpu['name']}")
        print(f"Чистое:   {cpu['clean_name']}")
        print(f"Family:    {cpu['family']}")
        print("-" * 50)
    
    if len(amd_cpus_with_clean_names) > 10:
        print(f"... и еще {len(amd_cpus_with_clean_names) - 10} процессоров")
    
    if amd_cpus_without_clean_names:
        print("\n=== AMD процессоры БЕЗ чистых названий ===")
        for cpu in amd_cpus_without_clean_names[:5]:  # Показываем первые 5
            print(f"Название: {cpu['name']}")
            print(f"Family:   {cpu['family']}")
            print("-" * 30)
        
        if len(amd_cpus_without_clean_names) > 5:
            print(f"... и еще {len(amd_cpus_without_clean_names) - 5} процессоров")
    
    # Проверим конкретно Ryzen 5 2600
    print("\n=== Проверка Ryzen 5 2600 ===")
    for cpu in amd_cpus_with_clean_names:
        if "2600" in cpu['clean_name'] and "RYZEN" in cpu['clean_name'].upper():
            print(f"Найден Ryzen 5 2600: {cpu['clean_name']}")
            print(f"Оригинал: {cpu['name']}")

if __name__ == "__main__":
    test_amd_clean_names() 