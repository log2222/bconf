import re

def analyze_ram_kit(ram_name):
    """Анализирует название комплекта памяти и определяет количество планок"""
    # Паттерны для поиска количества планок в комплекте
    patterns = [
        # 2x4Gb, 4x8Gb, 2x16Gb и т.д.
        r'(\d+)x(\d+)gb',
        # 2x4G, 4x8G, 2x16G и т.д.
        r'(\d+)x(\d+)g',
        # 2x4, 4x8, 2x16 и т.д. (если после этого идет Gb/G)
        r'(\d+)x(\d+)(?=\s*[gG])',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, ram_name, re.IGNORECASE)
        if match:
            kit_count = int(match.group(1))
            capacity_per_stick = int(match.group(2))
            return kit_count, capacity_per_stick
    
    # Если паттерн не найден, ищем просто объем памяти (например, 8Gb, 16Gb)
    volume_patterns = [
        r'(\d+)gb',
        r'(\d+)g(?=\s|$)',
    ]
    
    for pattern in volume_patterns:
        match = re.search(pattern, ram_name, re.IGNORECASE)
        if match:
            capacity = int(match.group(1))
            return 1, capacity
    
    # Если ничего не найдено, предполагаем 1 планку
    return 1, 0

def test_ram_analysis():
    """Тестирует функцию анализа комплектов памяти"""
    test_cases = [
        "Память DDR3 2x4Gb 1600MHz Corsair CMZ8GX3M2A1600C9",
        "Память DDR4 4x4Gb 3200MHz Kingston KVR32N22S8K4/16",
        "Память DDR4 2x8Gb 3600MHz G.Skill F4-3600C18D-16GVK",
        "Память DDR4 1x16Gb 3200MHz Crucial CT16G4DFD832A",
        "Память DDR4 8Gb 3200MHz Patriot PSD48G320081",
        "Память DDR4 16Gb 3600MHz Corsair CMK16GX4M1D3600C18",
        "Память DDR4 32Gb 3200MHz G.Skill F4-3200C16D-32GTZ",
    ]
    
    print("🧪 Тестирование анализа комплектов памяти:")
    print("=" * 60)
    
    for i, test_case in enumerate(test_cases, 1):
        kit_count, capacity_per_stick = analyze_ram_kit(test_case)
        
        if kit_count > 1 and capacity_per_stick > 0:
            result = f"DDR4 {kit_count}x{capacity_per_stick}Gb"
        elif kit_count == 1 and capacity_per_stick > 0:
            result = f"DDR4 {capacity_per_stick}Gb"
        else:
            result = "DDR4"
        
        print(f"{i}. {test_case}")
        print(f"   Результат: {result}")
        print(f"   Количество планок: {kit_count}, Объем на планку: {capacity_per_stick}Gb")
        print()

if __name__ == "__main__":
    test_ram_analysis() 