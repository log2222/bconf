import json

def check_unenriched_cpus():
    """Проверяет необогащенные процессоры"""
    with open('components.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    cpus = data.get('CPU', [])
    print(f"Всего CPU: {len(cpus)}")
    
    unenriched_count = 0
    
    for cpu in cpus:
        name = cpu.get('name', '')
        enriched = cpu.get('enriched', False)
        
        if not enriched:
            unenriched_count += 1
            print(f"\nНеобогащенный CPU: {name}")
            print(f"  enriched: {enriched}")
            print(f"  Поля: {list(cpu.keys())}")
            
            # Проверяем, есть ли поля CpuName или Family на верхнем уровне
            if 'CpuName' in cpu:
                print(f"  CpuName: {cpu['CpuName']}")
            if 'Family' in cpu:
                print(f"  Family: {cpu['Family']}")
    
    print(f"\nВсего необогащенных CPU: {unenriched_count}")

if __name__ == "__main__":
    check_unenriched_cpus() 