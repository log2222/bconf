import json

def test_cpu_structure():
    """Проверяет структуру данных CPU"""
    with open('components.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    cpus = data.get('CPU', [])
    print(f"Всего CPU: {len(cpus)}")
    
    if cpus:
        cpu = cpus[0]
        print("\nПоля первого CPU:")
        for key, value in cpu.items():
            print(f"  {key}: {value}")
        
        print(f"\nЕсть ли CpuName: {'CpuName' in cpu}")
        print(f"Есть ли Family: {'Family' in cpu}")
        print(f"Есть ли name: {'name' in cpu}")
        
        # Проверим несколько Intel и AMD процессоров
        intel_count = 0
        amd_count = 0
        
        for cpu in cpus[:10]:  # Первые 10
            name = cpu.get('name', '')
            if 'Intel' in name:
                intel_count += 1
                print(f"\nIntel CPU: {name}")
                print(f"  CpuName: {cpu.get('CpuName', 'НЕТ')}")
            elif 'AMD' in name:
                amd_count += 1
                print(f"\nAMD CPU: {name}")
                print(f"  Family: {cpu.get('Family', 'НЕТ')}")
        
        print(f"\nIntel в первых 10: {intel_count}")
        print(f"AMD в первых 10: {amd_count}")

if __name__ == "__main__":
    test_cpu_structure() 