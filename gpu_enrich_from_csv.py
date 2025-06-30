import json
import csv
import re
import os
from typing import Dict, List, Any, Optional

def extract_model_name(name: str) -> str:
    """Извлекает название модели из полного названия видеокарты и нормализует суффиксы (SUPER, TI, XT) с пробелом"""
    if not name:
        return ""
    name = name.lower()
    name = re.sub(r'\s+', ' ', name).strip()
    
    # Паттерн: вставить пробел перед суффиксами, если его нет
    name = re.sub(r'(\d)(super|ti|xt|m)\b', r'\1 \2', name)
    
    # Специальная обработка для названий в скобках (артикулы)
    if '(' in name and ')' in name:
        # Извлекаем содержимое скобок
        bracket_match = re.search(r'\(([^)]+)\)', name)
        if bracket_match:
            bracket_content = bracket_match.group(1)
            
            # Ищем модель в артикуле, например: TUF 3-GTX1660S-O6G-GAMING
            bracket_patterns = [
                r'gtx\s*(\d+)\s*(super|ti|xt|s)?',
                r'rtx\s*(\d+)\s*(super|ti|xt|s)?',
                r'gt\s*(\d+)',
                r'rx\s*(\d+)\s*(xt)?',
                r'hd\s*(\d+)',
                r'(\d+)\s*(super|ti|xt|s)?',
                # Паттерны без пробела между числом и суффиксом
                r'gtx\s*(\d+)(super|ti|xt|s)\b',
                r'rtx\s*(\d+)(super|ti|xt|s)\b',
                r'(\d+)(super|ti|xt|s)\b'
            ]
            for pattern in bracket_patterns:
                match = re.search(pattern, bracket_content)
                if match:
                    number = match.group(1)
                    suffix = match.group(2) if len(match.groups()) > 1 else ""
                    if suffix:
                        # Преобразуем 'S' в 'SUPER' для лучшего сопоставления
                        if suffix.lower() == 's':
                            suffix = 'super'
                        return f"{number} {suffix}"
                    # Если суффикс не найден, продолжаем поиск по основным паттернам
                    return number
    
    # Паттерны для извлечения модели
    patterns = [
        # Специфичные паттерны с суффиксами (высший приоритет)
        r'(geforce\s+(?:gtx|rtx)\s+\d+\s*(?:ti|super)?)',
        r'(gtx\s+\d+\s*(?:ti|super)?)',
        r'(rtx\s+\d+\s*(?:ti|super)?)',
        r'(geforce\s+gt\s+\d+)',
        r'(gt\s+\d+)',
        r'(geforce\s+gts\s+\d+)',
        r'(gts\s+\d+)',
        r'(geforce\s+gs\s+\d+)',
        r'(gs\s+\d+)',
        r'(geforce\s+g\s+\d+)',
        r'(g\s+\d+)',
        r'(radeon\s+rx\s+\d+\s*(?:xt)?)',
        r'(rx\s+\d+\s*(?:xt)?)',
        r'(radeon\s+hd\s+\d+)',
        r'(hd\s+\d+)',
        r'(radeon\s+r\d+\s+\d+)',
        r'(r\d+\s+\d+)',
        r'(radeon\s+pro\s+wx\s+\d+)',
        r'(pro\s+wx\s+\d+)',
        r'(quadro\s+\w+\s+\d+)',
        r'(quadro\s+\d+)',
        r'(radeon\s+pro\s+wx\s+\d+)',
        r'(pro\s+wx\s+\d+)',
        r'(radeon\s+pro\s+w\s+\d+)',
        r'(pro\s+w\s+\d+)',
        r'(radeon\s+pro\s+v\s+\d+)',
        r'(pro\s+v\s+\d+)',
        r'(radeon\s+pro\s+e\s+\d+)',
        r'(pro\s+e\s+\d+)',
        r'(radeon\s+pro\s+s\s+\d+)',
        r'(pro\s+s\s+\d+)',
        # Общий паттерн для цифр (низший приоритет)
        r'(\d+\s*(?:ti|super|xt)?)',
    ]
    for pattern in patterns:
        match = re.search(pattern, name)
        if match:
            model = match.group(1).strip()
            # Убираем лишние слова
            model = re.sub(r'\b(geforce|radeon|pro|wx|w|v|e|s|d|u|z|vega|fe|56|64|liquid|air|limited|edition|cooled)\b', '', model).strip()
            model = re.sub(r'\s+', ' ', model).strip()
            if model and len(model) > 2:
                return model
    return ""

def normalize_gpu_name(name: str) -> str:
    """Нормализует название видеокарты для лучшего сопоставления"""
    if not name:
        return ""
    
    # Приводим к нижнему регистру
    name = name.lower()
    
    # Удаляем лишние пробелы
    name = re.sub(r'\s+', ' ', name).strip()
    
    # Удаляем специальные символы, но оставляем цифры и буквы
    name = re.sub(r'[^\w\s\d]', ' ', name)
    
    # Удаляем лишние пробелы снова
    name = re.sub(r'\s+', ' ', name).strip()
    
    return name

def find_matching_gpu(gpu_name: str, gpu_database: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """Находит соответствующую видеокарту в базе данных с приоритетом десктопных версий и точного совпадения"""
    
    # Извлекаем модель из названия
    model_name = extract_model_name(gpu_name)
    normalized_name = normalize_gpu_name(gpu_name)
    
    if not model_name and not normalized_name:
        return None
    
    # 1. Сначала ищем точное совпадение по нормализованному названию (например, 'geforce gtx 1650 super')
    for gpu in gpu_database:
        db_name = normalize_gpu_name(gpu.get('name', ''))
        if normalized_name == db_name:
            return gpu
    
    # 2. Ищем точное совпадение по clean_name (например, 'geforce 210')
    for gpu in gpu_database:
        db_clean_name = gpu.get('name', '').lower()
        if 'geforce' in gpu_name.lower() and 'geforce' in db_clean_name:
            # Проверяем точное совпадение модели
            if model_name and model_name in db_clean_name:
                # Дополнительная проверка: если модель только цифры, ищем точное совпадение
                if model_name.isdigit():
                    # Ищем точное совпадение как отдельное слово
                    if re.search(rf'\b{re.escape(model_name)}\b', db_clean_name):
                        return gpu
                else:
                    return gpu
    
    matches = []
    # 3. Затем ищем точное совпадение по модели (строгое совпадение как отдельное слово)
    if model_name:
        for gpu in gpu_database:
            db_name = normalize_gpu_name(gpu.get('name', ''))
            db_model = extract_model_name(gpu.get('name', ''))
            # Точное совпадение модели
            if model_name == db_model:
                # Строгая проверка: если модель состоит только из цифр, не совпадать с другими по вхождению
                if model_name.isdigit() and db_model.isdigit() and model_name != db_model:
                    continue
                matches.append((gpu, 100, 'exact_model'))
            # Совпадение как отдельное слово (например, '210' не совпадает с '4090')
            elif model_name.isdigit():
                # Проверяем, что модель встречается как отдельное слово
                if re.search(rf'\b{re.escape(model_name)}\b', db_name):
                    matches.append((gpu, 90, 'word_model'))
            # Частичное совпадение модели (только если не только цифры)
            elif model_name in db_name or model_name in db_model:
                matches.append((gpu, 80, 'partial_model'))
    # 4. Если нет точных совпадений, ищем частичные
    if not matches:
        # Определяем бренд исходной видеокарты
        brand = None
        if 'nvidia' in gpu_name.lower():
            brand = 'nvidia'
        elif 'amd' in gpu_name.lower() or 'radeon' in gpu_name.lower():
            brand = 'amd'
        elif 'intel' in gpu_name.lower():
            brand = 'intel'
        for gpu in gpu_database:
            db_name = normalize_gpu_name(gpu.get('name', ''))
            db_brand = gpu.get('manufacturer', '').lower()
            if brand and brand not in db_brand:
                continue
            if not db_name:
                continue
            name_parts = normalized_name.split()
            db_parts = db_name.split()
            matches_count = 0
            for part in name_parts:
                # Только если part не является подстрокой другого числа
                if part.isdigit():
                    if any(part == db_part for db_part in db_parts):
                        matches_count += 1
                else:
                    if any(part in db_part or db_part in part for db_part in db_parts):
                        matches_count += 1
            if name_parts:
                score = matches_count / len(name_parts) * 60
                if score > 0.3 * 60:
                    matches.append((gpu, score, 'partial_name'))
    if not matches:
        return None
    def get_priority(gpu, score, match_type):
        csv_name = gpu.get('name', '').lower()
        if not csv_name.endswith('m'):
            priority = 1000
        else:
            priority = 0
        if match_type == 'exact_model':
            priority += 100
        elif match_type == 'word_model':
            priority += 90
        elif match_type == 'partial_model':
            priority += 50
        priority += score
        priority -= len(csv_name) * 0.1
        return priority
    matches.sort(key=lambda x: get_priority(x[0], x[1], x[2]), reverse=True)
    return matches[0][0]

def extract_memory_from_name(name):
    """Извлекает размер памяти из названия GPU"""
    if not name:
        return None
    
    name_lower = name.lower()
    
    # Специальные случаи для известных моделей
    known_memory = {
        'rx 5700 xt': 8,
        'rtx 2080 ti': 11,
        'rtx 2080': 8,
        'rtx 2070': 8,
        'rtx 2060': 6,
        'gtx 1660 super': 6,
        'gtx 1650 super': 4,
        'gtx 1650': 4,
        'gtx 1660': 6,
        'gtx 1070': 8,
        'gtx 1080': 8,
        'gtx 1080 ti': 11,
        'rx 580': 8,
        'rx 570': 4,
        'gt 1030': 2,
        'gt 710': 1,
    }
    
    # Проверяем известные модели
    for model, memory in known_memory.items():
        if model in name_lower:
            return memory
    
    # Паттерны для извлечения размера памяти
    patterns = [
        # Паттерны с G в конце (например, O2G, A4G, O6G, O8G, A11G)
        r'[ao](\d+)g\b',
        # Паттерны с G в середине (например, 1GD5, 8GC)
        r'(\d+)g[dch]\d*',
        # Паттерны с пробелом (например, 8G , 4G)
        r'(\d+)g\s*[,]',
        # Паттерны с Mb/MB
        r'(\d+)\s*mb\b',
        # Паттерны с Gb/GB
        r'(\d+)\s*gb\b',
        # Паттерны с G в конце слова
        r'(\d+)g\b',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, name_lower)
        if match:
            value = int(match.group(1))
            # Если значение больше 100, скорее всего это MB, конвертируем в GB
            if value > 100:
                return value // 1024
            # Проверяем, что значение разумное (1-24 GB)
            if 1 <= value <= 24:
                return value
    
    return None

def enrich_gpu_data(gpu_component: Dict[str, Any], gpu_spec: Dict[str, Any]) -> Dict[str, Any]:
    """Обогащает данные видеокарты информацией из базы данных"""
    
    # Сохраняем оригинальные поля из Excel
    original_fields = {
        "name": gpu_component.get("name"),
        "price": gpu_component.get("price"),
        "code": gpu_component.get("code"),
        "article": gpu_component.get("article"),
        "memory_size_gb": gpu_component.get("memory_size_gb"),
        "memory_size_raw": gpu_component.get("memory_size_raw")
    }
    
    # Копируем существующие данные
    enriched_gpu = gpu_component.copy()
    
    # Добавляем чистое название модели из CSV базы данных
    csv_name = gpu_spec.get('name', '')
    if csv_name:
        enriched_gpu['clean_name'] = csv_name
    
    # Добавляем поле name_gb на основе memory_size_gb
    memory_size_gb = gpu_component.get('memory_size_gb')
    if memory_size_gb is not None and memory_size_gb > 0:
        enriched_gpu['name_gb'] = f"{int(memory_size_gb)}Gb"
    else:
        # Пытаемся извлечь размер памяти из названия
        extracted_memory = extract_memory_from_name(gpu_component.get('name', ''))
        if extracted_memory:
            enriched_gpu['name_gb'] = f"{extracted_memory}Gb"
            # Также обновляем memory_size_gb если он был None
            if memory_size_gb is None:
                enriched_gpu['memory_size_gb'] = extracted_memory
        else:
            # Пытаемся извлечь размер памяти из базы данных
            memory_size = gpu_spec.get('memory_size')
            if memory_size and memory_size != 'Unknown':
                try:
                    # Пытаемся извлечь число из строки
                    memory_match = re.search(r'(\d+)', str(memory_size))
                    if memory_match:
                        memory_gb = int(memory_match.group(1))
                        enriched_gpu['name_gb'] = f"{memory_gb}Gb"
                        # Также обновляем memory_size_gb если он был None
                        if memory_size_gb is None:
                            enriched_gpu['memory_size_gb'] = memory_gb
                except:
                    pass
    
    # Добавляем поля из базы данных, если они не пустые
    fields_to_add = [
        'manufacturer', 'architecture', 'foundry', 'process_size', 
        'transistor_count', 'die_size', 'chip_package', 'release_date',
        'generation', 'bus_interface', 'base_clock', 'boost_clock',
        'memory_clock', 'memory_size', 'memory_type', 'memory_bus',
        'memory_bandwidth', 'shading_units', 'texture_mapping_units',
        'render_output_processors', 'streaming_multiprocessors',
        'tensor_cores', 'ray_tracing_cores', 'l1_cache', 'l2_cache',
        'thermal_design_power', 'board_length', 'board_width',
        'board_slot_width', 'suggested_psu', 'power_connectors',
        'display_connectors', 'directx_version', 'opengl_version',
        'vulkan_version', 'opencl_version', 'cuda_version',
        'shader_model_version', 'pixel_rate', 'texture_rate',
        'half_float_performance', 'single_float_performance',
        'double_float_performance'
    ]
    
    for field in fields_to_add:
        value = gpu_spec.get(field)
        if value and value not in ['', 'Unknown', '0', '0.0']:
            enriched_gpu[field] = value
    
    # Восстанавливаем оригинальные поля
    for key, value in original_fields.items():
        if value is not None:
            enriched_gpu[key] = value
    
    return enriched_gpu

def gpu_enrich_from_csv():
    """Обогащает данные видеокарт из JSON файла, используя CSV базу данных"""
    
    print("Загружаем базу данных видеокарт из CSV...")
    
    # Загружаем CSV базу данных
    gpu_database = []
    try:
        with open('gpu-database.csv', 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            gpu_database = list(reader)
        print(f"Загружено {len(gpu_database)} видеокарт из CSV базы данных")
    except FileNotFoundError:
        print("❌ Файл gpu-database.csv не найден!")
        print("Сначала запустите import_gpu_database.py для создания CSV файла")
        return False
    except Exception as e:
        print(f"❌ Ошибка при чтении CSV файла: {e}")
        return False
    
    # Загружаем JSON файл
    print("Загружаем components.json...")
    json_file = "components.json"
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("❌ Файл components.json не найден!")
        return False
    except Exception as e:
        print(f"❌ Ошибка при чтении JSON файла: {e}")
        return False
    
    # Проверяем наличие видеокарт в JSON
    if 'GPU' not in data:
        print("❌ В JSON файле нет секции GPU!")
        return False
    
    gpus = data['GPU']
    print(f"Найдено {len(gpus)} видеокарт в JSON файле")
    
    # Обогащаем данные
    enriched_count = 0
    not_found_count = 0
    
    for i, gpu in enumerate(gpus):
        gpu_name = gpu.get('name', '')
        model_name = extract_model_name(gpu_name)
        print(f"Обрабатываем {i+1}/{len(gpus)}: {gpu_name}")
        if model_name:
            print(f"  Извлечена модель: {model_name}")
        
        # Ищем соответствующую видеокарту в базе данных
        matching_gpu = find_matching_gpu(gpu_name, gpu_database)
        
        if matching_gpu:
            # Обогащаем данные
            enriched_gpu = enrich_gpu_data(gpu, matching_gpu)
            gpus[i] = enriched_gpu
            enriched_count += 1
            print(f"  ✅ Обогащено данными из: {matching_gpu.get('name', 'Неизвестно')}")
        else:
            not_found_count += 1
            print(f"  ❌ Не найдено соответствие в базе данных")
    
    # Сохраняем обновленный JSON
    print("\nСохраняем обновленный JSON файл...")
    try:
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("✅ JSON файл успешно обновлен")
    except Exception as e:
        print(f"❌ Ошибка при сохранении JSON файла: {e}")
        return False
    
    # Выводим статистику
    print(f"\n📊 Статистика обогащения:")
    print(f"  Всего видеокарт в JSON: {len(gpus)}")
    print(f"  Обогащено: {enriched_count}")
    print(f"  Не найдено соответствий: {not_found_count}")
    print(f"  Процент обогащения: {(enriched_count/len(gpus)*100):.1f}%")
    
    # Показываем примеры обогащенных видеокарт
    if enriched_count > 0:
        print(f"\nПримеры обогащенных видеокарт:")
        enriched_examples = [gpu for gpu in gpus if len(gpu) > 3]  # Более 3 полей = обогащенная
        for i, gpu in enumerate(enriched_examples[:3]):
            print(f"{i+1}. {gpu.get('name', 'Неизвестно')}")
            print(f"   Производитель: {gpu.get('manufacturer', 'Не указан')}")
            print(f"   Архитектура: {gpu.get('architecture', 'Не указана')}")
            print(f"   Память: {gpu.get('memory_size', 'Не указана')} {gpu.get('memory_type', '')}")
            print(f"   TDP: {gpu.get('thermal_design_power', 'Не указан')}")
            print()
    
    return True

if __name__ == "__main__":
    gpu_enrich_from_csv() 