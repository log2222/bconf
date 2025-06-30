import json

# Загружаем данные
with open('components.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Ищем процессор i5 6600 и исправляем его данные
for cpu in data['CPU']:
    if 'i5 6600' in cpu['name']:
        print(f"Исправляем процессор: {cpu['name']}")
        print(f"Было ProcessorNumber: {cpu.get('ProcessorNumber', 'НЕТ')}")
        
        # Очищаем неправильные данные
        fields_to_clear = [
            'ProcessorNumber', 'CoreCount', 'ThreadCount', 'ClockSpeed', 'Cache',
            'Bus', 'CoreVoltage', 'DieSize', 'MaxMemorySize', 'MemoryTypes',
            'MaxMemoryBandwidth', 'GraphicsMaxFreq', 'GraphicsBaseFreq',
            'GraphicsMaxDynamicFreq', 'GraphicsOutput', 'GraphicsDirectX',
            'GraphicsOpenGL', 'Graphics4KSupport', 'GraphicsMaxResolution',
            'GraphicsMaxDisplays', 'GraphicsExecutionUnits', 'GraphicsMaxMemory',
            'GraphicsMemoryBandwidth', 'GraphicsMemoryInterface'
        ]
        
        for field in fields_to_clear:
            if field in cpu:
                del cpu[field]
        
        print("Неправильные данные очищены")
        break

# Сохраняем исправленные данные
with open('components.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Файл обновлен") 