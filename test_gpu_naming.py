import json

def test_gpu_naming():
    """Тестирует правильное формирование названия GPU для итогового названия компьютера"""
    
    print("=== ТЕСТ ФОРМИРОВАНИЯ НАЗВАНИЯ GPU ===\n")
    
    try:
        # Загружаем JSON файл
        with open('components.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if 'GPU' not in data:
            print("❌ В JSON файле нет секции GPU!")
            return
        
        gpus = data['GPU']
        print(f"Найдено {len(gpus)} видеокарт\n")
        
        # Тестируем несколько примеров
        test_gpus = [
            "Видеокарта Palit PCI-E PA-GT710-1GD5 nVidia GeForce GT 710 1024Mb 64bit GDDR5 954/2500 DVIx1/HDMIx1/CRTx1/HDCP Bulk low profile",
            "Видеокарта MSI PCI-E GT 710 2GD3H LP nVidia GeForce GT 710 2048Mb 64bit DDR3 954/1600 DVIx1/HDMIx1/CRTx1/HDCP Ret low profile",
            "Видеокарта Gigabyte PCI-E GV-N1050OC-2GD nVidia GeForce GTX 1050 2048Mb 128bit GDDR5 1379/7008 DVIx1/HDMIx1/DPx1/HDCP Ret",
            "Видеокарта MSI PCI-E GTX 1650 VENTUS XS 4G nVidia GeForce GTX 1650 4096Mb 128bit GDDR5 1485/8000 DVIx1/HDMIx1/DPx1/HDCP Ret"
        ]
        
        for test_name in test_gpus:
            gpu = next((g for g in gpus if g['name'] == test_name), None)
            if gpu:
                print(f"Исходное название: {test_name}")
                print(f"clean_name: {gpu.get('clean_name', 'НЕТ')}")
                print(f"name_gb: {gpu.get('name_gb', 'НЕТ')}")
                print(f"memory_size_gb: {gpu.get('memory_size_gb', 'НЕТ')}")
                
                # Имитируем логику фронтенда
                gpu_label = test_name
                if gpu.get('clean_name') and gpu.get('name_gb'):
                    gpu_label = f"{gpu['clean_name']} {gpu['name_gb']}"
                elif gpu.get('clean_name'):
                    memory_gb = gpu.get('memory_size_gb')
                    if memory_gb:
                        gpu_label = f"{gpu['clean_name']} {memory_gb}Gb"
                    else:
                        gpu_label = gpu['clean_name']
                
                print(f"Итоговое название GPU: {gpu_label}")
                print("-" * 80)
        
        # Показываем статистику по полям
        print("\n📊 Статистика полей GPU:")
        clean_name_count = sum(1 for gpu in gpus if gpu.get('clean_name'))
        name_gb_count = sum(1 for gpu in gpus if gpu.get('name_gb'))
        memory_size_gb_count = sum(1 for gpu in gpus if gpu.get('memory_size_gb'))
        
        print(f"  clean_name: {clean_name_count}/{len(gpus)} ({clean_name_count/len(gpus)*100:.1f}%)")
        print(f"  name_gb: {name_gb_count}/{len(gpus)} ({name_gb_count/len(gpus)*100:.1f}%)")
        print(f"  memory_size_gb: {memory_size_gb_count}/{len(gpus)} ({memory_size_gb_count/len(gpus)*100:.1f}%)")
        
        # Примеры с clean_name и name_gb
        print("\n🎯 Примеры с clean_name и name_gb:")
        examples = [gpu for gpu in gpus if gpu.get('clean_name') and gpu.get('name_gb')][:5]
        for i, gpu in enumerate(examples, 1):
            final_name = f"{gpu['clean_name']} {gpu['name_gb']}"
            print(f"{i}. {final_name}")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    test_gpu_naming() 