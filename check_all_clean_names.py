import json

def check_all_clean_names():
    """Проверяет, что все процессоры имеют clean_name"""
    
    # Загружаем данные
    with open('components.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    cpus_with_clean_name = []
    cpus_without_clean_name = []
    
    for cpu in data['CPU']:
        if cpu.get('clean_name'):
            cpus_with_clean_name.append({
                'name': cpu['name'],
                'clean_name': cpu['clean_name']
            })
        else:
            cpus_without_clean_name.append(cpu['name'])
    
    print(f"Всего процессоров: {len(data['CPU'])}")
    print(f"С clean_name: {len(cpus_with_clean_name)}")
    print(f"Без clean_name: {len(cpus_without_clean_name)}")
    
    if cpus_without_clean_name:
        print("\n=== Процессоры БЕЗ clean_name ===")
        for name in cpus_without_clean_name:
            print(f"- {name}")
    
    print(f"\n=== Примеры clean_name ===")
    for i, cpu in enumerate(cpus_with_clean_name[:10]):
        print(f"{i+1}. {cpu['clean_name']}")
        print(f"   Оригинал: {cpu['name']}")
        print()

if __name__ == "__main__":
    check_all_clean_names() 