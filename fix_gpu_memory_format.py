import json

def fix_gpu_memory_format():
    """Преобразует поле memory_size_gb из числового формата в строковый с суффиксом Gb"""
    
    print("=== ПРЕОБРАЗОВАНИЕ ФОРМАТА MEMORY_SIZE_GB У ВИДЕОКАРТ ===\n")
    
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
        converted_count = 0
        skipped_count = 0
        examples = []
        
        # Обрабатываем каждую видеокарту
        for i, gpu in enumerate(gpus):
            memory_size = gpu.get('memory_size_gb')
            
            if memory_size is not None:
                # Проверяем, нужно ли конвертировать
                if isinstance(memory_size, (int, float)):
                    # Преобразуем в целое число и добавляем суффикс Gb
                    if isinstance(memory_size, float):
                        # Убираем .0 и преобразуем в int
                        memory_size_int = int(memory_size)
                    else:
                        memory_size_int = memory_size
                    
                    # Формируем новое значение
                    new_memory_size = f"{memory_size_int}Gb"
                    
                    # Обновляем поле
                    gpus[i]['memory_size_gb'] = new_memory_size
                    converted_count += 1
                    
                    # Сохраняем примеры для показа
                    if len(examples) < 5:
                        examples.append({
                            'name': gpu.get('name', 'Неизвестно'),
                            'clean_name': gpu.get('clean_name', 'Не указано'),
                            'old_value': memory_size,
                            'new_value': new_memory_size
                        })
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
        print(f"📊 Статистика преобразования:")
        print(f"  Всего видеокарт: {len(gpus)}")
        print(f"  Преобразовано: {converted_count}")
        print(f"  Пропущено: {skipped_count}")
        print(f"  Процент преобразования: {(converted_count/len(gpus)*100):.1f}%\n")
        
        # Показываем примеры преобразований
        print("📋 Примеры преобразований:")
        for i, example in enumerate(examples, 1):
            print(f"{i}. {example['clean_name']}:")
            print(f"   name: {example['name'][:80]}...")
            print(f"   memory_size_gb: {example['old_value']} → {example['new_value']}")
            print()
        
        # Показываем примеры GeForce GT 710
        print("🎯 Примеры GeForce GT 710 после преобразования:")
        gt710_examples = []
        for i, gpu in enumerate(gpus):
            if 'GT 710' in gpu.get('clean_name', ''):
                gt710_examples.append((i+1, gpu))
        
        for i, (num, gpu) in enumerate(gt710_examples[:5]):
            name = gpu.get('name', 'Неизвестно')
            clean_name = gpu.get('clean_name', 'Не указано')
            memory_size = gpu.get('memory_size_gb')
            
            print(f"{i+1}. Видеокарта #{num}:")
            print(f"   name: {name[:80]}...")
            print(f"   clean_name: {clean_name}")
            print(f"   memory_size_gb: {memory_size}")
            print()
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

if __name__ == "__main__":
    fix_gpu_memory_format() 