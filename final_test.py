import json

def test_final_results():
    """Финальный тест всех исправлений"""
    
    print("=== ФИНАЛЬНЫЙ ТЕСТ ВСЕХ ИСПРАВЛЕНИЙ ===\n")
    
    try:
        # Загружаем JSON файл
        with open('components.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if 'GPU' not in data:
            print("❌ В JSON файле нет секции GPU!")
            return
        
        gpus = data['GPU']
        print(f"Найдено {len(gpus)} видеокарт в JSON файле\n")
        
        # Тестируем проблемные видеокарты
        test_cases = [
            {
                "name": "(TUF 3-GTX1660S-O6G-GAMING)",
                "expected_clean_name": "GeForce GTX 1660 SUPER",
                "expected_name_gb": "6Gb"
            },
            {
                "name": "(ROG-STRIX-GTX1650S-A4G-GAMING)",
                "expected_clean_name": "GeForce GTX 1650 SUPER",
                "expected_name_gb": "4Gb"
            },
            {
                "name": "(PH-GTX1660S-O6G)",
                "expected_clean_name": "GeForce GTX 1660 SUPER",
                "expected_name_gb": "6Gb"
            },
            {
                "name": "Видеокарта MSI PCI-E GTX 1650 SUPER GAMING X nVidia GeForce GTX 1650SUPER 4096Mb 128bit GDDR6 1485/12000 DVIx1/HDMIx1/DPx3/HDCP Ret",
                "expected_clean_name": "GeForce GTX 1650 SUPER",
                "expected_name_gb": "4Gb"
            },
            {
                "name": "Видеокарта Palit PCI-E PA-GTX1660SUPER STORMX 6G nVidia GeForce GTX 1660SUPER 6144Mb 192bit GDDR6 1530/14000 DVIx1/HDMIx1/DPx1/HDCP Ret",
                "expected_clean_name": "GeForce GTX 1660 SUPER",
                "expected_name_gb": "6Gb"
            }
        ]
        
        print("🔍 ТЕСТИРОВАНИЕ ПРОБЛЕМНЫХ ВИДЕОКАРТ:\n")
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"Тест {i}: {test_case['name']}")
            
            # Ищем видеокарту
            found_gpu = None
            for gpu in gpus:
                if gpu.get('name') == test_case['name']:
                    found_gpu = gpu
                    break
            
            if found_gpu:
                clean_name = found_gpu.get('clean_name', '')
                name_gb = found_gpu.get('name_gb', '')
                memory_size_gb = found_gpu.get('memory_size_gb', '')
                manufacturer = found_gpu.get('manufacturer', '')
                architecture = found_gpu.get('architecture', '')
                
                print(f"  ✅ Найдена в JSON")
                print(f"  clean_name: '{clean_name}'")
                print(f"  name_gb: '{name_gb}'")
                print(f"  memory_size_gb: {memory_size_gb}")
                print(f"  manufacturer: '{manufacturer}'")
                print(f"  architecture: '{architecture}'")
                
                # Проверяем ожидаемые значения
                clean_name_ok = clean_name == test_case['expected_clean_name']
                name_gb_ok = name_gb == test_case['expected_name_gb']
                
                if clean_name_ok and name_gb_ok:
                    print(f"  🎉 ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ!")
                else:
                    print(f"  ⚠️  ПРОБЛЕМЫ:")
                    if not clean_name_ok:
                        print(f"    - clean_name: ожидалось '{test_case['expected_clean_name']}', получено '{clean_name}'")
                    if not name_gb_ok:
                        print(f"    - name_gb: ожидалось '{test_case['expected_name_gb']}', получено '{name_gb}'")
            else:
                print(f"  ❌ НЕ НАЙДЕНА В JSON")
            
            print()
        
        # Статистика по полю name_gb
        print("📊 СТАТИСТИКА ПО ПОЛЮ NAME_GB:\n")
        
        with_name_gb = 0
        without_name_gb = 0
        without_memory = 0
        
        for gpu in gpus:
            if gpu.get('name_gb'):
                with_name_gb += 1
            elif gpu.get('memory_size_gb'):
                without_name_gb += 1
            else:
                without_memory += 1
        
        print(f"  Всего видеокарт: {len(gpus)}")
        print(f"  С полем name_gb: {with_name_gb}")
        print(f"  Без поля name_gb (но с memory_size_gb): {without_name_gb}")
        print(f"  Без информации о памяти: {without_memory}")
        print(f"  Процент покрытия name_gb: {(with_name_gb / len(gpus) * 100):.1f}%")
        
        # Примеры итоговых названий
        print("\n🎯 ПРИМЕРЫ ИТОГОВЫХ НАЗВАНИЙ ВИДЕОКАРТ:\n")
        
        examples = [
            "GeForce GT 710 2Gb",
            "GeForce GTX 1650 SUPER 4Gb", 
            "GeForce GTX 1660 SUPER 6Gb",
            "GeForce RTX 2060 6Gb",
            "Radeon RX 570 8Gb"
        ]
        
        for example in examples:
            print(f"  {example}")
        
        print("\n✅ ФИНАЛЬНЫЙ ТЕСТ ЗАВЕРШЕН!")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    test_final_results() 