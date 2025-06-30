import json

def debug_amd_data():
    """Отлаживает данные AMD процессоров"""
    
    # Загружаем обогащенные данные
    with open('components.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Ищем AMD процессоры
    amd_cpus = []
    
    for cpu in data['CPU']:
        if "AMD" in cpu['name'].upper() or "RYZEN" in cpu['name'].upper() or "ATHLON" in cpu['name'].upper():
            amd_cpus.append({
                'name': cpu['name'],
                'enriched': cpu.get('enriched', False),
                'clean_name': cpu.get('clean_name', 'N/A'),
                'family': cpu.get('enrichment_data', {}).get('Family', 'N/A') if cpu.get('enrichment_data') else 'N/A'
            })
    
    print(f"Всего AMD процессоров: {len(amd_cpus)}")
    print(f"Обогащенных AMD процессоров: {len([c for c in amd_cpus if c['enriched']])}")
    print(f"AMD процессоров с clean_name: {len([c for c in amd_cpus if c['clean_name'] != 'N/A'])}")
    
    print("\n=== Примеры AMD процессоров ===")
    for i, cpu in enumerate(amd_cpus[:5]):
        print(f"{i+1}. {cpu['name']}")
        print(f"   Обогащен: {cpu['enriched']}")
        print(f"   Clean name: {cpu['clean_name']}")
        print(f"   Family: {cpu['family']}")
        print()
    
    # Проверим конкретно Ryzen 5 2600
    print("=== Поиск Ryzen 5 2600 ===")
    for cpu in amd_cpus:
        if "2600" in cpu['name'] and "RYZEN" in cpu['name'].upper():
            print(f"Найден: {cpu['name']}")
            print(f"Обогащен: {cpu['enriched']}")
            print(f"Clean name: {cpu['clean_name']}")
            print(f"Family: {cpu['family']}")
            print()

if __name__ == "__main__":
    debug_amd_data() 