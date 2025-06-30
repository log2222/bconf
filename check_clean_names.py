import json

# Загружаем обогащенные данные
with open('components.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("=== Проверка чистых названий Intel процессоров ===\n")

intel_count = 0
for cpu in data['CPU']:
    if cpu.get('enriched') and cpu.get('clean_name') and 'Intel' in cpu['name']:
        print(f"Исходное название: {cpu['name']}")
        print(f"Чистое название: {cpu['clean_name']}")
        print("-" * 80)
        intel_count += 1
        
        if intel_count >= 15:  # Показываем первые 15 для примера
            break

print(f"\nНайдено {intel_count} Intel процессоров с чистыми названиями")

# Проверяем общую статистику
total_intel = 0
with_clean_names = 0

for cpu in data['CPU']:
    if 'Intel' in cpu['name']:
        total_intel += 1
        if cpu.get('clean_name'):
            with_clean_names += 1

print(f"\nСтатистика:")
print(f"Всего Intel процессоров: {total_intel}")
print(f"С чистыми названиями: {with_clean_names}")
print(f"Процент: {with_clean_names/total_intel*100:.1f}%") 