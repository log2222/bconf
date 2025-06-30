import re

def extract_model_name(name: str) -> str:
    """Извлекает название модели из полного названия видеокарты и нормализует суффиксы (SUPER, TI, XT) с пробелом"""
    if not name:
        return ""
    name = name.lower()
    name = re.sub(r'\s+', ' ', name).strip()
    
    print(f"Обрабатываем: '{name}'")
    
    # Паттерн: вставить пробел перед суффиксами, если его нет
    name = re.sub(r'(\d)(super|ti|xt|m)\b', r'\1 \2', name)
    
    # Специальная обработка для названий в скобках (артикулы)
    if name.startswith('(') and name.endswith(')'):
        print("  Найдено название в скобках")
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
        for i, pattern in enumerate(bracket_patterns):
            match = re.search(pattern, name)
            if match:
                number = match.group(1)
                suffix = match.group(2) if len(match.groups()) > 1 else ""
                print(f"    Паттерн {i}: {pattern}")
                print(f"    Найдено: number='{number}', suffix='{suffix}'")
                if suffix:
                    # Преобразуем 'S' в 'SUPER' для лучшего сопоставления
                    if suffix.lower() == 's':
                        suffix = 'super'
                    result = f"{number} {suffix}"
                    print(f"    Возвращаем: '{result}'")
                    return result
                print(f"    Суффикс не найден, продолжаем поиск")
        print("  Ни один паттерн в скобках не дал суффикс")
    
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
    for i, pattern in enumerate(patterns):
        match = re.search(pattern, name)
        if match:
            model = match.group(1).strip()
            print(f"  Основной паттерн {i}: {pattern}")
            print(f"  Найдено: '{model}'")
            # Убираем лишние слова
            model = re.sub(r'\b(geforce|radeon|pro|wx|w|v|e|s|d|u|z|vega|fe|56|64|liquid|air|limited|edition|cooled)\b', '', model).strip()
            model = re.sub(r'\s+', ' ', model).strip()
            if model and len(model) > 2:
                print(f"  Возвращаем: '{model}'")
                return model
    print("  Ничего не найдено")
    return ""

# Тестируем проблемные названия
test_names = [
    "(TUF 3-GTX1660S-O6G-GAMING)",
    "(ROG-STRIX-GTX1650S-A4G-GAMING)",
    "(PH-GTX1660S-O6G)"
]

for name in test_names:
    print("=" * 60)
    result = extract_model_name(name)
    print(f"ИТОГОВЫЙ РЕЗУЛЬТАТ: '{result}'")
    print() 