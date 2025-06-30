#!/usr/bin/env python3
"""
Скрипт для гарантированного извлечения полей памяти GPU из имен.
Обеспечивает, что memory_size_gb и memory_size_raw всегда присутствуют в каждом GPU.
"""

import json
import re
import os

def extract_memory_from_name(name):
    """
    Извлекает объем памяти из имени GPU.
    Возвращает (memory_size_gb, memory_size_raw) или (None, None) если не найдено.
    """
    if not name:
        return None, None
    
    # Паттерны для поиска объема памяти
    patterns = [
        r'(\d+)\s*GB',  # 8GB, 16 GB
        r'(\d+)\s*TB',  # 1TB, 2 TB
        r'(\d+)\s*MB',  # 512MB, 1024 MB
        r'(\d+)GB',     # 8GB, 16GB
        r'(\d+)TB',     # 1TB, 2TB
        r'(\d+)MB',     # 512MB, 1024MB
    ]
    
    for pattern in patterns:
        match = re.search(pattern, name, re.IGNORECASE)
        if match:
            size = int(match.group(1))
            unit = match.group(0).upper()
            
            # Конвертируем в GB
            if 'TB' in unit:
                memory_gb = size * 1024
                memory_raw = f"{size}TB"
            elif 'GB' in unit:
                memory_gb = size
                memory_raw = f"{size}GB"
            elif 'MB' in unit:
                memory_gb = size / 1024
                memory_raw = f"{size}MB"
            else:
                continue
                
            return memory_gb, memory_raw
    
    return None, None

def ensure_gpu_memory_fields():
    """
    Обеспечивает наличие полей memory_size_gb и memory_size_raw для всех GPU.
    """
    # Загружаем components.json
    try:
        with open('components.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Ошибка: файл components.json не найден в текущей директории")
        return
    except json.JSONDecodeError as e:
        print(f"Ошибка при парсинге JSON: {e}")
        return
    
    # Проверяем наличие секции GPU
    if 'GPU' not in data:
        print("Секция 'GPU' не найдена в components.json")
        return
    
    gpus = data['GPU']
    updated_count = 0
    total_count = len(gpus)
    
    print(f"Обрабатываем {total_count} GPU...")
    
    for gpu in gpus:
        name = gpu.get('name', '')
        
        # Проверяем, есть ли уже поля памяти
        current_memory_gb = gpu.get('memory_size_gb')
        current_memory_raw = gpu.get('memory_size_raw')
        
        # Если поля отсутствуют или пустые, извлекаем из имени
        if current_memory_gb is None or current_memory_raw is None:
            memory_gb, memory_raw = extract_memory_from_name(name)
            
            if memory_gb is not None:
                gpu['memory_size_gb'] = memory_gb
                gpu['memory_size_raw'] = memory_raw
                updated_count += 1
                print(f"  Обновлен: {name} -> {memory_raw} ({memory_gb}GB)")
            else:
                # Если не удалось извлечь, устанавливаем значения по умолчанию
                gpu['memory_size_gb'] = None
                gpu['memory_size_raw'] = None
                print(f"  Не удалось извлечь память: {name}")
    
    # Сохраняем обновленные данные
    try:
        with open('components.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"\nГотово! Обновлено {updated_count} из {total_count} GPU")
        print("Файл components.json сохранен")
        
    except Exception as e:
        print(f"Ошибка при сохранении файла: {e}")

if __name__ == "__main__":
    print("=== Обеспечение полей памяти GPU ===")
    ensure_gpu_memory_fields() 