#!/usr/bin/env python3
"""
Скрипт для копирования components.json в папку data
"""

import shutil
import os
from datetime import datetime

def copy_components_to_data():
    """Копирует components.json в папку data"""
    
    source_file = "components.json"
    data_dir = "data"
    target_file = os.path.join(data_dir, "components.json")
    
    print(f"📁 Копирование {source_file} в папку {data_dir}...")
    
    # Проверяем существование исходного файла
    if not os.path.exists(source_file):
        print(f"❌ Исходный файл {source_file} не найден!")
        return False
    
    # Создаем папку data, если её нет
    if not os.path.exists(data_dir):
        print(f"📁 Создаю папку {data_dir}...")
        os.makedirs(data_dir)
    
    # Создаем резервную копию, если файл уже существует
    if os.path.exists(target_file):
        backup_name = f"components_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        backup_path = os.path.join(data_dir, backup_name)
        print(f"💾 Создаю резервную копию: {backup_name}")
        shutil.copy2(target_file, backup_path)
    
    try:
        # Копируем файл
        shutil.copy2(source_file, target_file)
        
        # Проверяем размеры файлов
        source_size = os.path.getsize(source_file)
        target_size = os.path.getsize(target_file)
        
        print(f"✅ Файл успешно скопирован!")
        print(f"📊 Размер исходного файла: {source_size:,} байт")
        print(f"📊 Размер скопированного файла: {target_size:,} байт")
        
        if source_size == target_size:
            print(f"✅ Размеры файлов совпадают - копирование прошло успешно!")
        else:
            print(f"⚠️  Размеры файлов не совпадают!")
            return False
        
        # Проверяем, что файл можно прочитать как JSON
        try:
            import json
            with open(target_file, 'r', encoding='utf-8') as f:
                data = json.load(f)  # Используем json.load для проверки JSON структуры
            
            # Проверяем наличие основных секций
            sections = list(data.keys())
            print(f"📋 Найдены секции: {', '.join(sections)}")
            
            # Проверяем количество элементов в каждой секции
            for section in sections:
                if isinstance(data[section], list):
                    count = len(data[section])
                    print(f"  📊 {section}: {count} элементов")
            
        except Exception as e:
            print(f"⚠️  Предупреждение: не удалось проверить структуру JSON: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при копировании: {e}")
        return False

if __name__ == "__main__":
    success = copy_components_to_data()
    if success:
        print(f"\n🎉 Копирование завершено успешно!")
    else:
        print(f"\n❌ Копирование не удалось!") 