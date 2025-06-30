import json
import re

def analyze_ram_kit(ram_name):
    """Анализирует название комплекта памяти и определяет количество модулей"""
    if not ram_name:
        return 1
    
    # Паттерны для поиска количества модулей в комплекте
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
            return int(match.group(1))
    
    # Если паттерн не найден, предполагаем 1 модуль
    return 1

def test_ram_compatibility():
    """Тестирует логику совместимости комплектов памяти"""
    
    # Загружаем данные
    try:
        with open('components.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ Ошибка при чтении JSON: {e}")
        return
    
    # Находим материнскую плату с 4 слотами
    motherboards = data.get('Motherboard', [])
    test_motherboard = None
    for mb in motherboards:
        if mb.get('ram_slots', 0) >= 4:
            test_motherboard = mb
            break
    
    if not test_motherboard:
        print("❌ Не найдена материнская плата с 4+ слотами")
        return
    
    print(f"🧪 Тестируем на материнской плате: {test_motherboard.get('name')}")
    print(f"   Слотов памяти: {test_motherboard.get('ram_slots')}")
    print("=" * 80)
    
    # Находим комплекты памяти 2x4Gb
    ram_modules = data.get('RAM', [])
    test_ram_kits = []
    
    for ram in ram_modules:
        name = ram.get('name', '')
        if '2x4' in name.lower() or '2x4gb' in name.lower():
            test_ram_kits.append(ram)
    
    if not test_ram_kits:
        print("❌ Не найдены комплекты памяти 2x4Gb")
        return
    
    print(f"📦 Найдено {len(test_ram_kits)} комплектов 2x4Gb:")
    for i, ram in enumerate(test_ram_kits[:3], 1):
        name = ram.get('name', '')
        modules_in_kit = ram.get('modules_in_kit', 0)
        analyzed_modules = analyze_ram_kit(name)
        
        print(f"{i}. {name}")
        print(f"   modules_in_kit в данных: {modules_in_kit}")
        print(f"   Проанализировано: {analyzed_modules}")
        print(f"   Используется: {modules_in_kit or analyzed_modules}")
        print()
    
    # Тестируем логику совместимости
    print("🔍 Тестирование логики совместимости:")
    print("-" * 50)
    
    test_kit = test_ram_kits[0]
    kit_name = test_kit.get('name', '')
    modules_in_kit = test_kit.get('modules_in_kit', 0)
    analyzed_modules = analyze_ram_kit(kit_name)
    used_modules = modules_in_kit or analyzed_modules
    
    max_slots = test_motherboard.get('ram_slots', 4)
    
    print(f"Комплект: {kit_name}")
    print(f"Модулей в комплекте: {used_modules}")
    print(f"Максимум слотов: {max_slots}")
    print()
    
    # Симуляция добавления комплектов
    for i in range(1, 5):
        total_modules = i * used_modules
        can_add = total_modules <= max_slots
        status = "✅ Можно добавить" if can_add else "❌ Превышен лимит"
        
        print(f"{i} комплект{'а' if i > 1 else ''}: {total_modules} модулей из {max_slots} - {status}")
    
    print()
    print("📋 Вывод:")
    print(f"• 1 комплект {kit_name} = {used_modules} модуля")
    print(f"• 2 комплекта = {2 * used_modules} модулей")
    print(f"• Максимум можно поставить: {max_slots // used_modules} комплектов")

if __name__ == "__main__":
    test_ram_compatibility() 