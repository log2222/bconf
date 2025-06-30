#!/usr/bin/env python3
"""
Скрипт для проверки обогащения видеокарт в components.json
"""

import json
import os

def check_gpu_enrichment():
    """Проверяет обогащение видеокарт в components.json"""
    
    # Путь к файлу
    json_file = "components.json"
    
    if not os.path.exists(json_file):
        print(f"❌ Файл {json_file} не найден!")
        return
    
    print(f"🔍 Проверяю обогащение видеокарт в {json_file}...")
    
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ Ошибка чтения файла: {e}")
        return
    
    # Проверяем наличие секции GPU
    if "GPU" not in data:
        print("❌ Секция 'GPU' не найдена в JSON файле!")
        return
    
    gpus = data["GPU"]
    total_gpus = len(gpus)
    
    print(f"\n📊 Всего видеокарт в JSON: {total_gpus}")
    
    # Поля, которые должны быть добавлены при обогащении
    enrichment_fields = [
        "manufacturer",
        "architecture", 
        "foundry",
        "chip_package",
        "release_date",
        "generation",
        "bus_interface",
        "memory_type",
        "shading_units",
        "texture_mapping_units",
        "render_output_processors"
    ]
    
    enriched_count = 0
    partially_enriched = 0
    not_enriched = 0
    
    enriched_examples = []
    not_enriched_examples = []
    
    for i, gpu in enumerate(gpus):
        name = gpu.get("name", "Без названия")
        
        # Подсчитываем количество полей обогащения
        enrichment_field_count = 0
        for field in enrichment_fields:
            if field in gpu:
                enrichment_field_count += 1
        
        # Определяем статус обогащения
        if enrichment_field_count >= 8:  # Большинство полей заполнено
            enriched_count += 1
            if len(enriched_examples) < 3:
                enriched_examples.append({
                    "name": name,
                    "fields_count": enrichment_field_count,
                    "manufacturer": gpu.get("manufacturer", "Не указан"),
                    "architecture": gpu.get("architecture", "Не указана")
                })
        elif enrichment_field_count > 0:
            partially_enriched += 1
        else:
            not_enriched += 1
            if len(not_enriched_examples) < 3:
                not_enriched_examples.append(name)
    
    # Выводим статистику
    print(f"\n📈 Статистика обогащения:")
    print(f"  ✅ Полностью обогащено: {enriched_count} ({enriched_count/total_gpus*100:.1f}%)")
    print(f"  ⚠️  Частично обогащено: {partially_enriched} ({partially_enriched/total_gpus*100:.1f}%)")
    print(f"  ❌ Не обогащено: {not_enriched} ({not_enriched/total_gpus*100:.1f}%)")
    
    # Примеры обогащенных видеокарт
    if enriched_examples:
        print(f"\n✅ Примеры обогащенных видеокарт:")
        for i, example in enumerate(enriched_examples, 1):
            print(f"  {i}. {example['name']}")
            print(f"     Производитель: {example['manufacturer']}")
            print(f"     Архитектура: {example['architecture']}")
            print(f"     Заполнено полей: {example['fields_count']}/{len(enrichment_fields)}")
    
    # Примеры необогащенных видеокарт
    if not_enriched_examples:
        print(f"\n❌ Примеры необогащенных видеокарт:")
        for i, name in enumerate(not_enriched_examples, 1):
            print(f"  {i}. {name}")
    
    # Детальная проверка полей
    print(f"\n🔍 Детальная проверка полей обогащения:")
    field_stats = {}
    for field in enrichment_fields:
        field_count = sum(1 for gpu in gpus if field in gpu)
        field_stats[field] = field_count
        percentage = field_count / total_gpus * 100
        status = "✅" if percentage > 80 else "⚠️" if percentage > 50 else "❌"
        print(f"  {status} {field}: {field_count}/{total_gpus} ({percentage:.1f}%)")
    
    # Общий вывод
    if enriched_count == total_gpus:
        print(f"\n🎉 Отлично! Все {total_gpus} видеокарт полностью обогащены!")
    elif enriched_count > total_gpus * 0.8:
        print(f"\n👍 Хорошо! Большинство видеокарт обогащены ({enriched_count}/{total_gpus})")
    elif enriched_count > 0:
        print(f"\n⚠️  Частично обогащено: {enriched_count}/{total_gpus} видеокарт")
    else:
        print(f"\n❌ Видеокарты не обогащены!")
    
    return enriched_count, total_gpus

if __name__ == "__main__":
    check_gpu_enrichment() 