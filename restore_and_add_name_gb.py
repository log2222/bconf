import json

def restore_and_add_name_gb():
    """Восстанавливает поле memory_size_gb к числовому формату и добавляет новое поле name_gb"""
    
    print("=== ВОССТАНОВЛЕНИЕ MEMORY_SIZE_GB И ДОБАВЛЕНИЕ NAME_GB ===\n")
    
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
        restored_count = 0
        added_name_gb_count = 0
        skipped_count = 0
        examples = []
        
        # Обрабатываем каждую видеокарту
        for i, gpu in enumerate(gpus):
            memory_size = gpu.get('memory_size_gb')
            
            if memory_size is not None:
                # Проверяем, нужно ли восстановить числовой формат
                if isinstance(memory_size, str) and memory_size.endswith('Gb'):
                    # Извлекаем числовое значение из строки "2Gb"
                    try:
                        numeric_value = int(memory_size.replace('Gb', ''))
                        
                        # Восстанавливаем числовое значение в memory_size_gb
                        gpus[i]['memory_size_gb'] = numeric_value
                        restored_count += 1
                        
                        # Добавляем новое поле name_gb со строковым форматом
                        gpus[i]['name_gb'] = memory_size  # "2Gb"
                        added_name_gb_count += 1
                        
                        # Сохраняем примеры для показа
                        if len(examples) < 5:
                            examples.append({
                                'name': gpu.get('name', 'Неизвестно'),
                                'clean_name': gpu.get('clean_name', 'Не указано'),
                                'memory_size_gb': numeric_value,
                                'name_gb': memory_size
                            })
                    except ValueError:
                        skipped_count += 1
                else:
                    # Если уже числовой формат, просто добавляем name_gb
                    if isinstance(memory_size, (int, float)):
                        numeric_value = int(memory_size) if isinstance(memory_size, float) else memory_size
                        gpus[i]['name_gb'] = f"{numeric_value}Gb"
                        added_name_gb_count += 1
                    else:
                        skipped_count += 1
            else:
                skipped_count += 1
        
        # Сохраняем обновленный JSON
        print("Сохраняем обновленный JSON файл...")
        with open('components.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("✅ JSON файл успешно обновлен\n")
        
        # Выводим статистику
        print(f"📊 Статистика обработки:")
        print(f"  Всего видеокарт: {len(gpus)}")
        print(f"  Восстановлено memory_size_gb: {restored_count}")
        print(f"  Добавлено name_gb: {added_name_gb_count}")
        print(f"  Пропущено: {skipped_count}")
        print(f"  Процент обработки: {((restored_count + added_name_gb_count)/len(gpus)*100):.1f}%\n")
        
        # Показываем примеры
        print("📋 Примеры обработки:")
        for i, example in enumerate(examples, 1):
            print(f"{i}. {example['clean_name']}:")
            print(f"   name: {example['name'][:80]}...")
            print(f"   memory_size_gb: {example['memory_size_gb']} (числовой)")
            print(f"   name_gb: {example['name_gb']} (строковый)")
            print()
        
        # Показываем примеры GeForce GT 710
        print("🎯 Примеры GeForce GT 710 после обработки:")
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
            print(f"   name: {name[:80]}...")
            print(f"   clean_name: {clean_name}")
            print(f"   memory_size_gb: {memory_size_gb}")
            print(f"   name_gb: {name_gb}")
            print()
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

if __name__ == "__main__":
    restore_and_add_name_gb() 