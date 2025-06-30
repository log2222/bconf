import json
import re
from collections import defaultdict

def auto_check_all_cpus():
    """Автоматическая проверка enrichment всех CPU с детальным отчетом"""
    
    # Загружаем данные
    with open('components.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    total_cpus = len(data['CPU'])
    enrichment_fields = ['ProcessorNumber', 'CoreCount', 'ThreadCount', 'ClockSpeed', 'Cache']
    
    # Статистика
    stats = {
        'total': total_cpus,
        'fully_enriched': 0,
        'partially_enriched': 0,
        'not_enriched': 0,
        'by_brand': defaultdict(lambda: {'total': 0, 'enriched': 0, 'partial': 0, 'not_enriched': 0}),
        'missing_fields': defaultdict(int),
        'examples': {
            'fully_enriched': [],
            'partially_enriched': [],
            'not_enriched': []
        }
    }
    
    print("🔍 Автоматическая проверка enrichment всех CPU...")
    print("=" * 80)
    
    for cpu in data['CPU']:
        name = cpu['name']
        enriched_count = sum(1 for field in enrichment_fields if cpu.get(field))
        total_fields = len(enrichment_fields)
        
        # Определяем бренд
        brand = "Unknown"
        if "intel" in name.lower():
            brand = "Intel"
        elif "amd" in name.lower():
            brand = "AMD"
        
        stats['by_brand'][brand]['total'] += 1
        
        # Подсчитываем статистику
        if enriched_count == total_fields:
            stats['fully_enriched'] += 1
            stats['by_brand'][brand]['enriched'] += 1
            if len(stats['examples']['fully_enriched']) < 3:
                stats['examples']['fully_enriched'].append(name)
        elif enriched_count > 0:
            stats['partially_enriched'] += 1
            stats['by_brand'][brand]['partial'] += 1
            if len(stats['examples']['partially_enriched']) < 3:
                stats['examples']['partially_enriched'].append(name)
        else:
            stats['not_enriched'] += 1
            stats['by_brand'][brand]['not_enriched'] += 1
            if len(stats['examples']['not_enriched']) < 3:
                stats['examples']['not_enriched'].append(name)
        
        # Подсчитываем отсутствующие поля
        for field in enrichment_fields:
            if not cpu.get(field):
                stats['missing_fields'][field] += 1
    
    # Выводим общую статистику
    print(f"\n📊 ОБЩАЯ СТАТИСТИКА:")
    print(f"Всего CPU: {stats['total']}")
    print(f"✅ Полностью обогащены: {stats['fully_enriched']} ({stats['fully_enriched']/stats['total']*100:.1f}%)")
    print(f"⚠️  Частично обогащены: {stats['partially_enriched']} ({stats['partially_enriched']/stats['total']*100:.1f}%)")
    print(f"❌ Не обогащены: {stats['not_enriched']} ({stats['not_enriched']/stats['total']*100:.1f}%)")
    print(f"Общий процент обогащения: {((stats['fully_enriched'] + stats['partially_enriched']) / stats['total'] * 100):.1f}%")
    
    # Статистика по брендам
    print(f"\n🏷️  СТАТИСТИКА ПО БРЕНДАМ:")
    for brand, brand_stats in stats['by_brand'].items():
        if brand_stats['total'] > 0:
            enriched_pct = brand_stats['enriched'] / brand_stats['total'] * 100
            partial_pct = brand_stats['partial'] / brand_stats['total'] * 100
            not_enriched_pct = brand_stats['not_enriched'] / brand_stats['total'] * 100
            
            print(f"\n{brand}:")
            print(f"  Всего: {brand_stats['total']}")
            print(f"  ✅ Полностью обогащены: {brand_stats['enriched']} ({enriched_pct:.1f}%)")
            print(f"  ⚠️  Частично обогащены: {brand_stats['partial']} ({partial_pct:.1f}%)")
            print(f"  ❌ Не обогащены: {brand_stats['not_enriched']} ({not_enriched_pct:.1f}%)")
    
    # Анализ отсутствующих полей
    print(f"\n🔍 АНАЛИЗ ОТСУТСТВУЮЩИХ ПОЛЕЙ:")
    for field, count in sorted(stats['missing_fields'].items(), key=lambda x: x[1], reverse=True):
        percentage = count / stats['total'] * 100
        status = "✅" if percentage < 20 else "⚠️" if percentage < 50 else "❌"
        print(f"  {status} {field}: отсутствует у {count} CPU ({percentage:.1f}%)")
    
    # Примеры
    print(f"\n📋 ПРИМЕРЫ:")
    
    if stats['examples']['fully_enriched']:
        print(f"\n✅ Примеры полностью обогащенных CPU:")
        for i, name in enumerate(stats['examples']['fully_enriched'], 1):
            print(f"  {i}. {name}")
    
    if stats['examples']['partially_enriched']:
        print(f"\n⚠️  Примеры частично обогащенных CPU:")
        for i, name in enumerate(stats['examples']['partially_enriched'], 1):
            print(f"  {i}. {name}")
    
    if stats['examples']['not_enriched']:
        print(f"\n❌ Примеры необогащенных CPU:")
        for i, name in enumerate(stats['examples']['not_enriched'], 1):
            print(f"  {i}. {name}")
    
    # Рекомендации
    print(f"\n💡 РЕКОМЕНДАЦИИ:")
    if stats['not_enriched'] > 0:
        print(f"• {stats['not_enriched']} CPU требуют enrichment")
        if stats['missing_fields']['ProcessorNumber'] > stats['total'] * 0.5:
            print("• Много CPU без ProcessorNumber - проверьте CSV файлы")
        if stats['missing_fields']['CoreCount'] > stats['total'] * 0.5:
            print("• Много CPU без CoreCount - проверьте логику извлечения")
    else:
        print("• Все CPU обогащены! 🎉")
    
    # Сохраняем отчет в файл
    report_file = "cpu_enrichment_report.txt"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("ОТЧЕТ ПО ENRICHMENT CPU\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Всего CPU: {stats['total']}\n")
        f.write(f"Полностью обогащены: {stats['fully_enriched']}\n")
        f.write(f"Частично обогащены: {stats['partially_enriched']}\n")
        f.write(f"Не обогащены: {stats['not_enriched']}\n")
        f.write(f"Процент обогащения: {((stats['fully_enriched'] + stats['partially_enriched']) / stats['total'] * 100):.1f}%\n")
    
    print(f"\n📄 Подробный отчет сохранен в: {report_file}")
    
    return stats

if __name__ == "__main__":
    auto_check_all_cpus() 