import json

def fix_last_cpu():
    """Добавляет clean_name для последнего процессора без него"""
    
    # Загружаем данные
    with open('components.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for cpu in data['CPU']:
        if not cpu.get('clean_name'):
            print(f"Найден процессор без clean_name: {cpu['name']}")
            if "Pentium G5600F" in cpu['name']:
                cpu['clean_name'] = "Intel Pentium G5600F"
                print(f"Добавлен clean_name: Intel Pentium G5600F")
                break
    
    # Сохраняем обновленные данные
    with open('components.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("Файл components.json обновлен")

if __name__ == "__main__":
    fix_last_cpu() 