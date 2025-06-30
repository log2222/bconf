import json

def check_enriched_cpus():
    """Проверяет обогащенные процессоры"""
    with open('components.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    cpus = data.get('CPU', [])
    print(f"Всего CPU: {len(cpus)}")
    
    enriched_count = 0
    intel_enriched = 0
    amd_enriched = 0
    
    for cpu in cpus:
        name = cpu.get('name', '')
        
        # Проверяем наличие полей обогащения
        has_cpu_name = 'CpuName' in cpu and cpu['CpuName']
        has_family = 'Family' in cpu and cpu['Family']
        
        if has_cpu_name or has_family:
            enriched_count += 1
            
            if 'Intel' in name:
                intel_enriched += 1
                print(f"\nIntel (обогащенный): {name}")
                print(f"  CpuName: {cpu.get('CpuName', 'НЕТ')}")
            elif 'AMD' in name:
                amd_enriched += 1
                print(f"\nAMD (обогащенный): {name}")
                print(f"  Family: {cpu.get('Family', 'НЕТ')}")
    
    print(f"\nВсего обогащенных: {enriched_count}")
    print(f"Intel обогащенных: {intel_enriched}")
    print(f"AMD обогащенных: {amd_enriched}")

if __name__ == "__main__":
    check_enriched_cpus() 