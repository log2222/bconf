import json
import os

def remove_unenriched_cpus():
    """Удаляет не обогащённые процессоры из JSON файла"""
    
    # Список не обогащённых процессоров
    unenriched_cpus = [
        "Процессор Intel Socket 1151 Pentium G5600F (3.90Ghz/4Mb) tray (CM8068403377516SRF7Y)",
        "Процессор AMD A6 7480 FM2+ (AD7480ACI23AB) (3.5GHz/AMD Radeon R5) OEM",
        "Процессор AMD A6 7480 FM2+ (AD7480ACABBOX) (3.5GHz/AMD Radeon R5) Box",
        "Процессор AMD A8 7680 FM2+ (AD7680ACI43AB) (3.5GHz/AMD Radeon R7) OEM",
        "Процессор AMD A8 7680 FM2+ (AD7680ACABBOX) (3.8GHz/AMD Radeon R7) Box",
        "Процессор Dell Xeon Silver 4116 FCLGA3647 16.5Mb 2.1Ghz (338-BLUT)"
    ]
    
    # Загружаем JSON файл
    json_file = "components.json"
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"Загружен JSON файл")
    except Exception as e:
        print(f"Ошибка при загрузке JSON: {e}")
        return
    
    cpu_list = data.get("CPU", [])
    initial_count = len(cpu_list)
    print(f"Найдено {initial_count} CPU в JSON")
    
    # Удаляем не обогащённые процессоры
    removed_count = 0
    filtered_cpus = []
    
    for cpu in cpu_list:
        cpu_name = cpu.get("name", "")
        if cpu_name in unenriched_cpus:
            print(f"Удаляется: {cpu_name}")
            removed_count += 1
        else:
            filtered_cpus.append(cpu)
    
    # Обновляем данные
    data["CPU"] = filtered_cpus
    
    # Сохраняем обновлённый JSON
    try:
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"\nУдалено {removed_count} CPU из {initial_count}")
        print(f"Осталось {len(filtered_cpus)} CPU")
        print(f"Обновлённый файл сохранён: {json_file}")
    except Exception as e:
        print(f"Ошибка при сохранении JSON: {e}")

if __name__ == "__main__":
    remove_unenriched_cpus() 