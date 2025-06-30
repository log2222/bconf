import json

def check_current_state():
    """Проверяет текущее состояние данных видеокарт"""
    
    print("=== ТЕКУЩЕЕ СОСТОЯНИЕ ДАННЫХ ВИДЕОКАРТ ===\n")
    
    try:
        # Загружаем JSON файл
        with open('components.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Проверяем наличие секции GPU
        if 'GPU' not in data:
            print("❌ В JSON файле нет секции GPU!")
            return
        
        gpus = data['GPU']
        print(f"Найдено {len(gpus)} видеокарт в JSON файле\n")
        
        # Анализируем поля
        fields_analysis = {}
        gpus_with_all_fields = []
        
        for i, gpu in enumerate(gpus):
            # Проверяем наличие ключевых полей
            clean_name = gpu.get('clean_name')
            memory_size_gb = gpu.get('memory_size_gb')
            name_gb = gpu.get('name_gb')
            
            # Анализируем типы данных
            if clean_name is not None:
                field_type = type(clean_name).__name__
                if 'clean_name' not in fields_analysis:
                    fields_analysis['clean_name'] = {'count': 0, 'types': {}}
                fields_analysis['clean_name']['count'] += 1
                if field_type not in fields_analysis['clean_name']['types']:
                    fields_analysis['clean_name']['types'][field_type] = 0
                fields_analysis['clean_name']['types'][field_type] += 1
            
            if memory_size_gb is not None:
                field_type = type(memory_size_gb).__name__
                if 'memory_size_gb' not in fields_analysis:
                    fields_analysis['memory_size_gb'] = {'count': 0, 'types': {}}
                fields_analysis['memory_size_gb']['count'] += 1
                if field_type not in fields_analysis['memory_size_gb']['types']:
                    fields_analysis['memory_size_gb']['types'][field_type] = 0
                fields_analysis['memory_size_gb']['types'][field_type] += 1
            
            if name_gb is not None:
                field_type = type(name_gb).__name__
                if 'name_gb' not in fields_analysis:
                    fields_analysis['name_gb'] = {'count': 0, 'types': {}}
                fields_analysis['name_gb']['count'] += 1
                if field_type not in fields_analysis['name_gb']['types']:
                    fields_analysis['name_gb']['types'][field_type] = 0
                fields_analysis['name_gb']['types'][field_type] += 1
            
            # Если есть все три поля, добавляем в список
            if clean_name and memory_size_gb is not None and name_gb:
                gpus_with_all_fields.append((i+1, gpu))
        
        # Выводим статистику по полям
        print("📊 Статистика по полям:")
        for field, stats in fields_analysis.items():
            print(f"  {field}:")
            print(f"    Всего записей: {stats['count']}")
            print(f"    Типы данных: {stats['types']}")
        print()
        
        # Показываем примеры с полным набором полей
        print(f"📋 Примеры видеокарт с полным набором полей ({len(gpus_with_all_fields)} шт.):")
        for i, (num, gpu) in enumerate(gpus_with_all_fields[:10]):
            name = gpu.get('name', 'Неизвестно')
            clean_name = gpu.get('clean_name', 'Не указано')
            memory_size_gb = gpu.get('memory_size_gb')
            name_gb = gpu.get('name_gb')
            
            print(f"{i+1}. Видеокарта #{num}:")
            print(f"   name: {name[:60]}...")
            print(f"   clean_name: {clean_name}")
            print(f"   memory_size_gb: {memory_size_gb} ({type(memory_size_gb).__name__})")
            print(f"   name_gb: {name_gb} ({type(name_gb).__name__})")
            print()
        
        # Показываем примеры GeForce GT 710
        print("🎯 Примеры GeForce GT 710:")
        gt710_examples = []
        for num, gpu in gpus_with_all_fields:
            if 'GT 710' in gpu.get('clean_name', ''):
                gt710_examples.append((num, gpu))
        
        for i, (num, gpu) in enumerate(gt710_examples[:5]):
            name = gpu.get('name', 'Неизвестно')
            clean_name = gpu.get('clean_name', 'Не указано')
            memory_size_gb = gpu.get('memory_size_gb')
            name_gb = gpu.get('name_gb')
            
            print(f"{i+1}. Видеокарта #{num}:")
            print(f"   name: {name[:60]}...")
            print(f"   clean_name: {clean_name}")
            print(f"   memory_size_gb: {memory_size_gb}")
            print(f"   name_gb: {name_gb}")
            print()
        
        # Проверяем обогащение
        enriched_count = 0
        for gpu in gpus:
            if len(gpu) > 5:  # Если больше 5 полей, считаем обогащенной
                enriched_count += 1
        
        print(f"📈 Общая статистика:")
        print(f"  Всего видеокарт: {len(gpus)}")
        print(f"  Обогащенных: {enriched_count}")
        print(f"  С полным набором полей: {len(gpus_with_all_fields)}")
        print(f"  Процент обогащения: {(enriched_count/len(gpus)*100):.1f}%")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    check_current_state() 