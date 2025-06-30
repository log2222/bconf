import json

def add_name_gb_to_all():
    """Добавляет поле name_gb ко всем видеокартам, у которых есть memory_size_gb"""
    
    print("=== ДОБАВЛЕНИЕ ПОЛЯ NAME_GB КО ВСЕМ ВИДЕОКАРТАМ ===\n")
    
    try:
        # Загружаем JSON файл
        with open('components.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Проверяем наличие секции GPU
        if 'GPU' not in data:
            print("❌ В JSON файле нет секции GPU!")
            return False
        
        gpus = data['GPU']
        print(f"Найдено {len(gpus)} видеокарт в JSON файле\n")
        
        # Счетчики для статистики
        added_count = 0
        already_exists_count = 0
        no_memory_count = 0
        examples = []
        
        # Обрабатываем каждую видеокарту
        for i, gpu in enumerate(gpus):
            memory_size_gb = gpu.get('memory_size_gb')
            name_gb = gpu.get('name_gb')
            
            if memory_size_gb is not None:
                if name_gb is None:
                    # Добавляем поле name_gb
                    if isinstance(memory_size_gb, (int, float)):
                        numeric_value = int(memory_size_gb) if isinstance(memory_size_gb, float) else memory_size_gb
                        gpus[i]['name_gb'] = f"{numeric_value}Gb"
                        added_count += 1
                        
                        # Сохраняем примеры для показа
                        if len(examples) < 5:
                            examples.append({
                                'name': gpu.get('name', 'Неизвестно'),
                                'clean_name': gpu.get('clean_name', 'Не указано'),
                                'memory_size_gb': memory_size_gb,
                                'name_gb': f"{numeric_value}Gb"
                            })
                    else:
                        no_memory_count += 1
                else:
                    already_exists_count += 1
            else:
                no_memory_count += 1
        
        # Сохраняем обновленный JSON
        print("Сохраняем обновленный JSON файл...")
        with open('components.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("✅ JSON файл успешно обновлен\n")
        
        # Выводим статистику
        print(f"📊 Статистика добавления name_gb:")
        print(f"  Всего видеокарт: {len(gpus)}")
        print(f"  Добавлено name_gb: {added_count}")
        print(f"  Уже существовало: {already_exists_count}")
        print(f"  Без memory_size_gb: {no_memory_count}")
        print(f"  Процент покрытия: {((added_count + already_exists_count)/len(gpus)*100):.1f}%\n")
        
        # Показываем примеры
        print("📋 Примеры добавления name_gb:")
        for i, example in enumerate(examples, 1):
            print(f"{i}. {example['clean_name']}:")
            print(f"   name: {example['name'][:60]}...")
            print(f"   memory_size_gb: {example['memory_size_gb']}")
            print(f"   name_gb: {example['name_gb']}")
            print()
        
        # Показываем примеры GeForce GT 710
        print("🎯 Примеры GeForce GT 710:")
        gt710_examples = []
        for i, gpu in enumerate(gpus):
            if 'GT 710' in gpu.get('clean_name', ''):
                gt710_examples.append((i+1, gpu))
        
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
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

if __name__ == "__main__":
    add_name_gb_to_all() 