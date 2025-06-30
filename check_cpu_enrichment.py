#!/usr/bin/env python3
"""
Скрипт для проверки обогащения процессоров в components.json
"""

import json
import os
import re

def check_cpu_enrichment(cpu_name_or_model=None):
    """Проверяет enrichment для конкретного CPU или показывает статистику"""
    
    # Загружаем данные
    with open('components.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if cpu_name_or_model:
        # Поиск конкретного CPU
        cpu_name_or_model = cpu_name_or_model.lower()
        found_cpus = []
        
        for cpu in data['CPU']:
            name = cpu['name'].lower()
            processor_number = cpu.get('ProcessorNumber', '').lower()
            
            if (cpu_name_or_model in name or 
                cpu_name_or_model in processor_number or
                cpu_name_or_model.replace('-', '').replace(' ', '') in name.replace('-', '').replace(' ', '')):
                found_cpus.append(cpu)
        
        if found_cpus:
            print(f"\nНайдено {len(found_cpus)} CPU для '{cpu_name_or_model}':")
            print("=" * 80)
            
            for i, cpu in enumerate(found_cpus, 1):
                print(f"\n{i}. {cpu['name']}")
                print(f"   ProcessorNumber: {cpu.get('ProcessorNumber', 'НЕТ')}")
                print(f"   CoreCount: {cpu.get('CoreCount', 'НЕТ')}")
                print(f"   ThreadCount: {cpu.get('ThreadCount', 'НЕТ')}")
                print(f"   ClockSpeed: {cpu.get('ClockSpeed', 'НЕТ')}")
                print(f"   Cache: {cpu.get('Cache', 'НЕТ')}")
                print(f"   MaxMem: {cpu.get('MaxMem', 'НЕТ')}")
                print(f"   Lithography: {cpu.get('Lithography', 'НЕТ')}")
                
                # Проверяем, обогащен ли CPU
                enrichment_fields = ['ProcessorNumber', 'CoreCount', 'ThreadCount', 'ClockSpeed', 'Cache']
                enriched_count = sum(1 for field in enrichment_fields if cpu.get(field))
                total_fields = len(enrichment_fields)
                
                if enriched_count == total_fields:
                    print(f"   ✅ Полностью обогащен ({enriched_count}/{total_fields})")
                elif enriched_count > 0:
                    print(f"   ⚠️  Частично обогащен ({enriched_count}/{total_fields})")
                else:
                    print(f"   ❌ Не обогащен ({enriched_count}/{total_fields})")
        else:
            print(f"CPU с названием '{cpu_name_or_model}' не найден")
    
    else:
        # Показываем общую статистику
        total_cpus = len(data['CPU'])
        enriched_cpus = 0
        partially_enriched = 0
        not_enriched = 0
        
        enrichment_fields = ['ProcessorNumber', 'CoreCount', 'ThreadCount', 'ClockSpeed', 'Cache']
        
        for cpu in data['CPU']:
            enriched_count = sum(1 for field in enrichment_fields if cpu.get(field))
            total_fields = len(enrichment_fields)
            
            if enriched_count == total_fields:
                enriched_cpus += 1
            elif enriched_count > 0:
                partially_enriched += 1
            else:
                not_enriched += 1
        
        print(f"\nСтатистика enrichment CPU:")
        print("=" * 50)
        print(f"Всего CPU: {total_cpus}")
        print(f"✅ Полностью обогащены: {enriched_cpus}")
        print(f"⚠️  Частично обогащены: {partially_enriched}")
        print(f"❌ Не обогащены: {not_enriched}")
        print(f"Процент обогащения: {((enriched_cpus + partially_enriched) / total_cpus * 100):.1f}%")
        
        # Показываем примеры необогащенных CPU
        if not_enriched > 0:
            print(f"\nПримеры необогащенных CPU:")
            print("-" * 50)
            count = 0
            for cpu in data['CPU']:
                if count >= 5:  # Показываем только первые 5
                    break
                enriched_count = sum(1 for field in enrichment_fields if cpu.get(field))
                if enriched_count == 0:
                    print(f"• {cpu['name']}")
                    count += 1

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # Проверяем конкретный CPU
        cpu_name = " ".join(sys.argv[1:])
        check_cpu_enrichment(cpu_name)
    else:
        # Показываем общую статистику
        check_cpu_enrichment()
        
        print(f"\nПримеры использования:")
        print("python check_cpu_enrichment.py i5-6600")
        print("python check_cpu_enrichment.py ryzen 5 3600")
        print("python check_cpu_enrichment.py core i7") 