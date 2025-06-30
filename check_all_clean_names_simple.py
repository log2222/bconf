import json

# Загружаем данные
with open('data/components.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

cpus = data.get('CPU', [])
total = len(cpus)
with_clean_name = sum(1 for cpu in cpus if cpu.get('clean_name'))
without_clean_name = total - with_clean_name

print(f'Всего CPU: {total}')
print(f'С clean_name: {with_clean_name}')
print(f'Без clean_name: {without_clean_name}')

if with_clean_name > 0:
    example = next((cpu for cpu in cpus if cpu.get('clean_name')), None)
    if example:
        print(f'\nПример CPU с clean_name:')
        print(f'  name: {example.get("name")}')
        print(f'  clean_name: {example.get("clean_name")}') 