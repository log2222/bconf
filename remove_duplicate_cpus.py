import json
from collections import defaultdict
import os

def remove_duplicate_cpus():
    """Удаляет дубликаты процессоров по CpuId, оставляя тот с наименьшей ценой"""
    
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
    
    # Группируем процессоры по CpuId
    cpu_groups = defaultdict(list)
    
    for cpu in cpu_list:
        cpuid = cpu.get("CpuId", "")
        if cpuid:  # Только если есть CpuId
            cpu_groups[cpuid].append(cpu)
        else:
            # Если нет CpuId, добавляем как есть (не группируем)
            cpu_groups[f"no_cpuid_{len(cpu_groups)}"].append(cpu)
    
    # Обрабатываем каждую группу
    filtered_cpus = []
    removed_count = 0
    
    for cpuid, cpus in cpu_groups.items():
        if len(cpus) == 1:
            # Один процессор в группе - оставляем как есть
            filtered_cpus.append(cpus[0])
        else:
            # Несколько процессоров с одинаковым CpuId
            print(f"\nНайдены дубликаты для CpuId '{cpuid}':")
            for cpu in cpus:
                name = cpu.get("name", "")
                price = cpu.get("price", 0)
                print(f"  - {name} (цена: {price})")
            
            # Находим процессор с наименьшей ценой
            min_price_cpu = min(cpus, key=lambda x: x.get("price", float('inf')))
            filtered_cpus.append(min_price_cpu)
            
            removed_count += len(cpus) - 1
            print(f"  Оставлен: {min_price_cpu.get('name', '')} (цена: {min_price_cpu.get('price', 0)})")
    
    # Обновляем данные
    data["CPU"] = filtered_cpus
    
    # Сохраняем обновлённый JSON
    try:
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"\nУдалено {removed_count} дубликатов из {initial_count}")
        print(f"Осталось {len(filtered_cpus)} CPU")
        print(f"Обновлённый файл сохранён: {json_file}")
    except Exception as e:
        print(f"Ошибка при сохранении JSON: {e}")

if __name__ == "__main__":
    remove_duplicate_cpus() 