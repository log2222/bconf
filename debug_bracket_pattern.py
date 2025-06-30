import re

def debug_bracket_pattern(name):
    """Отладочная функция для анализа названий в скобках"""
    print(f"Исходное название: '{name}'")
    
    name_lower = name.lower()
    print(f"После lower(): '{name_lower}'")
    
    # Проверяем различные паттерны
    patterns = [
        (r'gtx\s*(\d+)\s*(super|ti|xt|s)?', "GTX с пробелом"),
        (r'rtx\s*(\d+)\s*(super|ti|xt|s)?', "RTX с пробелом"),
        (r'(\d+)\s*(super|ti|xt|s)?', "Общий с пробелом"),
        (r'gtx\s*(\d+)(super|ti|xt|s)\b', "GTX без пробела"),
        (r'rtx\s*(\d+)(super|ti|xt|s)\b', "RTX без пробела"),
        (r'(\d+)(super|ti|xt|s)\b', "Общий без пробела"),
        (r'gtx1660s', "Прямое совпадение GTX1660S"),
        (r'1660s', "Прямое совпадение 1660S"),
        (r'gtx.*?(\d+).*?(super|ti|xt|s)', "GTX с любыми символами"),
        (r'(\d+).*?(super|ti|xt|s)', "Число с любыми символами")
    ]
    
    for pattern, description in patterns:
        match = re.search(pattern, name_lower)
        if match:
            print(f"✅ {description}: {pattern}")
            print(f"   Группы: {match.groups()}")
            print(f"   Полное совпадение: '{match.group(0)}'")
        else:
            print(f"❌ {description}: {pattern}")
    
    print("-" * 50)

# Тестируем проблемные названия
test_names = [
    "(TUF 3-GTX1660S-O6G-GAMING)",
    "(ROG-STRIX-GTX1650S-A4G-GAMING)",
    "(PH-GTX1660S-O6G)",
    "(DUAL-RTX2060S-O8G-EVO)",
    "(TUF 3-GTX1660TI-O6G-GAMING)"
]

for name in test_names:
    debug_bracket_pattern(name) 