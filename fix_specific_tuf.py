import json
import csv
import re
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
    if name.startswith('(') and name.endswith(')'):
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
            match = re.search(pattern, name)
            if match:
                number = match.group(1)
                suffix = match.group(2) if len(match.groups()) > 1 else ""
                if suffix:
                    # Преобразуем 'S' в 'SUPER' для лучшего сопоставления
                    if suffix.lower() == 's':
                        suffix = 'super'
                    return f"{number} {suffix}"
                # Если суффикс не найден, продолжаем поиск по основным паттернам
    
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
    
    matches = []
    # 2. Затем ищем точное совпадение по модели
    if model_name:
        for gpu in gpu_database:
            db_name = normalize_gpu_name(gpu.get('name', ''))
            db_model = extract_model_name(gpu.get('name', ''))
            # Точное совпадение модели
            if model_name == db_model:
                matches.append((gpu, 100, 'exact_model'))
            # Частичное совпадение модели
            elif model_name in db_name or model_name in db_model:
                matches.append((gpu, 80, 'partial_model'))
    # 3. Если нет точных совпадений, ищем частичные
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
        elif match_type == 'partial_model':
            priority += 50
        priority += score
        priority -= len(csv_name) * 0.1
        return priority
    matches.sort(key=lambda x: get_priority(x[0], x[1], x[2]), reverse=True)
    return matches[0][0]

def enrich_gpu_data(gpu_component: Dict[str, Any], gpu_spec: Dict[str, Any]) -> Dict[str, Any]:
    """Обогащает данные видеокарты информацией из базы данных (ПРИНУДИТЕЛЬНО)"""
    
    # Сохраняем ТОЛЬКО оригинальные поля из Excel
    original_fields = {
        "name": gpu_component.get("name"),
        "price": gpu_component.get("price"),
        "code": gpu_component.get("code"),
        "article": gpu_component.get("article"),
        "memory_size_gb": gpu_component.get("memory_size_gb"),
        "memory_size_raw": gpu_component.get("memory_size_raw")
    }
    
    # Создаем НОВЫЙ словарь только с оригинальными полями
    enriched_gpu = original_fields.copy()
    
    # Добавляем чистое название модели из CSV базы данных
    csv_name = gpu_spec.get('name', '')
    if csv_name:
        enriched_gpu['clean_name'] = csv_name
    
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
    
    return enriched_gpu

def fix_specific_tuf():
    """Исправляет конкретную видеокарту (TUF 3-GTX1660S-O6G-GAMING)"""
    
    print("🔧 Исправляем конкретную видеокарту (TUF 3-GTX1660S-O6G-GAMING)...")
    
    # Загружаем CSV базу данных
    gpu_database = []
    try:
        with open('gpu-database.csv', 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            gpu_database = list(reader)
        print(f"📊 Загружено {len(gpu_database)} видеокарт из CSV базы данных")
    except FileNotFoundError:
        print("❌ Файл gpu-database.csv не найден!")
        return False
    
    # Загружаем JSON файл
    print("📁 Загружаем components.json...")
    try:
        with open('components.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("❌ Файл components.json не найден!")
        return False
    
    # Проверяем наличие видеокарт в JSON
    if 'GPU' not in data:
        print("❌ В JSON файле нет секции GPU!")
        return False
    
    gpus = data['GPU']
    target_name = "(TUF 3-GTX1660S-O6G-GAMING)"
    
    # Ищем конкретную видеокарту
    target_index = None
    for i, gpu in enumerate(gpus):
        if gpu.get('name') == target_name:
            target_index = i
            break
    
    if target_index is None:
        print(f"❌ Видеокарта '{target_name}' не найдена в JSON файле")
        return False
    
    print(f"✅ Найдена видеокарта на позиции {target_index + 1}")
    print(f"   Текущее clean_name: {gpus[target_index].get('clean_name', 'Не указано')}")
    
    # Ищем соответствующую видеокарту в базе данных
    matching_gpu = find_matching_gpu(target_name, gpu_database)
    
    if matching_gpu:
        print(f"✅ Найдено правильное совпадение: {matching_gpu.get('name', 'Неизвестно')}")
        
        # Принудительно обогащаем данные
        enriched_gpu = enrich_gpu_data(gpus[target_index], matching_gpu)
        gpus[target_index] = enriched_gpu
        
        print(f"✅ Видеокарта исправлена:")
        print(f"   Новое clean_name: {enriched_gpu.get('clean_name', 'Не указано')}")
        print(f"   Производитель: {enriched_gpu.get('manufacturer', 'Не указан')}")
        print(f"   Архитектура: {enriched_gpu.get('architecture', 'Не указана')}")
        
        # Сохраняем обновленный JSON
        print("\n💾 Сохраняем обновленный JSON файл...")
        try:
            with open('components.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print("✅ JSON файл успешно обновлен")
        except Exception as e:
            print(f"❌ Ошибка при сохранении JSON файла: {e}")
            return False
        
        return True
    else:
        print(f"❌ Не найдено соответствие в базе данных")
        return False

if __name__ == "__main__":
    fix_specific_tuf() 