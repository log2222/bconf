import json

# Загружаем данные
with open('data/components.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

cpus = data.get('CPU', [])
a8_9600 = next((cpu for cpu in cpus if 'A8 9600' in cpu.get('name', '')), None)

if a8_9600:
    print('AMD A8 9600 найден:')
    print(f'  name: {a8_9600.get("name")}')
    print(f'  clean_name: {a8_9600.get("clean_name")}')
    print(f'  has clean_name field: {"clean_name" in a8_9600}')
else:
    print('AMD A8 9600 не найден') 