import json
import re

def test_enrichment_quality():
    """Автоматический тест качества обогащения процессоров"""
    
    # Загружаем данные
    with open('components.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print("🔍 АВТОМАТИЧЕСКИЙ ТЕСТ ОБОГАЩЕНИЯ ПРОЦЕССОРОВ")
    print("=" * 60)
    
    errors = []
    warnings = []
    success_count = 0
    
    for cpu in data['CPU']:
        name = cpu.get('name', '')
        article = cpu.get('article', '')
        clean_name = cpu.get('clean_name', '')
        enriched = cpu.get('enriched', False)
        enrichment_data = cpu.get('enrichment_data', {})
        
        # Пропускаем необогащенные
        if not enriched:
            continue
            
        success_count += 1
        
        # Тест 1: Проверка clean_name для AMD Athlon 200GE
        if '200GE' in name or '200GE' in article:
            expected_clean_name = 'AMD Athlon 200GE'
            if clean_name != expected_clean_name:
                errors.append(f"❌ 200GE: {name} | clean_name='{clean_name}' должен быть '{expected_clean_name}'")
            else:
                print(f"✅ 200GE: {name} | clean_name='{clean_name}'")
        
        # Тест 2: Проверка серии процессора в clean_name
        if 'AMD' in name:
            if 'Athlon' in name and 'Ryzen' in clean_name:
                errors.append(f"❌ СЕРИЯ: {name} | clean_name='{clean_name}' - Athlon получил Ryzen")
            elif 'Ryzen' in name and 'Athlon' in clean_name:
                errors.append(f"❌ СЕРИЯ: {name} | clean_name='{clean_name}' - Ryzen получил Athlon")
        
        # Тест 3: Проверка Family в enrichment_data
        family = enrichment_data.get('Family', '')
        if family:
            if 'Athlon' in name and 'Ryzen' in family:
                errors.append(f"❌ FAMILY: {name} | Family='{family}' - Athlon получил Ryzen Family")
            elif 'Ryzen' in name and 'Athlon' in family:
                errors.append(f"❌ FAMILY: {name} | Family='{family}' - Ryzen получил Athlon Family")
        
        # Тест 4: Проверка Model в enrichment_data (не должен быть "on" для Athlon)
        model = enrichment_data.get('Model', '')
        if 'Athlon' in name and model == 'on':
            warnings.append(f"⚠️ MODEL: {name} | Model='{model}' - Athlon имеет Model='on'")
        
        # Тест 5: Проверка артикула в enrichment_data
        product_id_tray = enrichment_data.get('Product ID Tray', '')
        product_id_boxed = enrichment_data.get('Product ID Boxed', '')
        if article and article not in (product_id_tray + product_id_boxed):
            warnings.append(f"⚠️ АРТИКУЛ: {name} | article='{article}' не найден в Product ID")
    
    # Вывод результатов
    print(f"\n📊 РЕЗУЛЬТАТЫ ТЕСТА:")
    print(f"✅ Обогащено процессоров: {success_count}")
    print(f"❌ Ошибок: {len(errors)}")
    print(f"⚠️ Предупреждений: {len(warnings)}")
    
    if errors:
        print(f"\n❌ ОШИБКИ:")
        for error in errors:
            print(f"  {error}")
    
    if warnings:
        print(f"\n⚠️ ПРЕДУПРЕЖДЕНИЯ:")
        for warning in warnings:
            print(f"  {warning}")
    
    if not errors and not warnings:
        print(f"\n🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
    
    # Дополнительная статистика
    print(f"\n📈 СТАТИСТИКА:")
    amd_count = len([cpu for cpu in data['CPU'] if 'AMD' in cpu.get('name', '') and cpu.get('enriched', False)])
    intel_count = len([cpu for cpu in data['CPU'] if 'Intel' in cpu.get('name', '') and cpu.get('enriched', False)])
    print(f"  AMD обогащено: {amd_count}")
    print(f"  Intel обогащено: {intel_count}")
    
    return len(errors) == 0

if __name__ == "__main__":
    success = test_enrichment_quality()
    exit(0 if success else 1) 