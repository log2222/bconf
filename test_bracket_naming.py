import json
import re

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
            r'gtx\s*(\d+)\s*(super|ti|xt)?',
            r'rtx\s*(\d+)\s*(super|ti|xt)?',
            r'gt\s*(\d+)',
            r'rx\s*(\d+)\s*(xt)?',
            r'hd\s*(\d+)',
            r'(\d+)\s*(super|ti|xt)?'
        ]
        for pattern in bracket_patterns:
            match = re.search(pattern, name)
            if match:
                number = match.group(1)
                suffix = match.group(2) if len(match.groups()) > 1 else ""
                if suffix:
                    return f"{number} {suffix}"
                else:
                    return number
    
    # Паттерны для извлечения модели
    patterns = [
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

def test_bracket_naming():
    """Тестирует извлечение модели из названий в скобках"""
    
    print("=== ТЕСТ ИЗВЛЕЧЕНИЯ МОДЕЛИ ИЗ НАЗВАНИЙ В СКОБКАХ ===\n")
    
    test_cases = [
        "(TUF 3-GTX1660S-O6G-GAMING)",
        "(ROG-STRIX-GTX1650S-A4G-GAMING)",
        "(PH-GTX1660S-O6G)",
        "(DUAL-RTX2060S-O8G-EVO)",
        "(TUF 3-GTX1660TI-O6G-GAMING)",
        "(ROG-STRIX-RTX2080TI-O11G-GAMING)",
        "(DUAL-RTX2070S-O8G-EVO)",
        "(TURBO-RTX2080S-8G-EVO)",
        "(DUAL-RTX2080S-O8G-EVO-V2)",
        "(ROG-STRIX-RTX2060S-O8G-EVO-GAMING)"
    ]
    
    for test_name in test_cases:
        model = extract_model_name(test_name)
        print(f"Название: {test_name}")
        print(f"Извлеченная модель: '{model}'")
        print("-" * 50)
    
    # Тестируем на реальных данных
    print("\n=== ПРОВЕРКА РЕАЛЬНЫХ ДАННЫХ ===\n")
    
    try:
        with open('components.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if 'GPU' not in data:
            print("❌ В JSON файле нет секции GPU!")
            return
        
        gpus = data['GPU']
        
        # Ищем видеокарты с названиями в скобках
        bracket_gpus = [gpu for gpu in gpus if gpu.get('name', '').startswith('(') and gpu.get('name', '').endswith(')')]
        
        print(f"Найдено {len(bracket_gpus)} видеокарт с названиями в скобках:\n")
        
        for gpu in bracket_gpus[:10]:  # Показываем первые 10
            name = gpu.get('name', '')
            clean_name = gpu.get('clean_name', '')
            extracted_model = extract_model_name(name)
            
            print(f"Название: {name}")
            print(f"Текущий clean_name: {clean_name}")
            print(f"Извлеченная модель: '{extracted_model}'")
            print("-" * 50)
            
    except Exception as e:
        print(f"❌ Ошибка при чтении файла: {e}")

if __name__ == "__main__":
    test_bracket_naming() 