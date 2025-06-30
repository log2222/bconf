import json

# Загружаем данные
with open('components.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Ищем все CPU с 200GE в артикуле или названии
found = []
for cpu in data['CPU']:
    name = cpu.get('name', '')
    article = cpu.get('article', '')
    if '200GE' in name or '200GE' in article:
        found.append(cpu)

if found:
    for cpu in found:
        print('---')
        print(f'name: {cpu.get("name")}')
        print(f'article: {cpu.get("article")}',)
        print(f'clean_name: {cpu.get("clean_name")}')
        print(f'enriched: {cpu.get("enriched")}')
        enrichment = cpu.get('enrichment_data', {})
        print(f'Family: {enrichment.get("Family")}')
        print(f'Model: {enrichment.get("Model")}')
        # Проверяем clean_name
        if cpu.get('clean_name') == 'AMD Athlon 200GE':
            print('✅ clean_name OK')
        else:
            print('❌ clean_name НЕВЕРНО')
else:
    print('Не найдено CPU с 200GE') 