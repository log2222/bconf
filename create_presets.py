import json
import re
from typing import Dict, List, Any

def load_components():
    """Загружает компоненты из JSON файла"""
    with open('data/components.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def find_component_by_pattern(components: List[Dict], patterns: List[str], category: str) -> str:
    """Находит компонент по паттернам в названии"""
    for pattern in patterns:
        for component in components:
            name = component.get('name', '').lower()
            if pattern.lower() in name:
                return component['name']
    return ""

def find_cpu_by_generation(components: List[Dict], generation: str, cores: str = "") -> str:
    """Находит CPU по поколению и количеству ядер"""
    for component in components:
        name = component.get('name', '').lower()
        if generation.lower() in name:
            if cores and cores in name:
                return component['name']
            elif not cores:
                return component['name']
    return ""

def find_gpu_by_model(components: List[Dict], model: str) -> str:
    """Находит GPU по модели"""
    for component in components:
        name = component.get('name', '').lower()
        if model.lower() in name:
            return component['name']
    return ""

def find_ram_by_specs(components: List[Dict], capacity: str, type: str = "DDR4") -> str:
    """Находит RAM по объему и типу"""
    for component in components:
        name = component.get('name', '').lower()
        if capacity.lower() in name and type.lower() in name:
            return component['name']
    return ""

def find_ssd_by_capacity(components: List[Dict], capacity: str) -> str:
    """Находит SSD по объему"""
    for component in components:
        name = component.get('name', '').lower()
        if capacity.lower() in name:
            return component['name']
    return ""

def find_motherboard_by_chipset(components: List[Dict], chipset: str) -> str:
    """Находит материнскую плату по чипсету"""
    for component in components:
        name = component.get('name', '').lower()
        if chipset.lower() in name:
            return component['name']
    return ""

def find_psu_by_power(components: List[Dict], power: str) -> str:
    """Находит блок питания по мощности"""
    for component in components:
        name = component.get('name', '').lower()
        if power.lower() in name:
            return component['name']
    return ""

def find_case_by_type(components: List[Dict], case_type: str) -> str:
    """Находит корпус по типу"""
    for component in components:
        name = component.get('name', '').lower()
        if case_type.lower() in name:
            return component['name']
    return ""

def create_realistic_presets():
    """Создает реалистичные типовые конфигурации"""
    components = load_components()
    
    presets = []
    
    # 1. Бюджетная офисная конфигурация
    office_budget = {
        "name": "Офисная (бюджетная)",
        "components": {}
    }
    
    # CPU - Intel Core i3
    cpu = find_cpu_by_generation(components['CPU'], 'i3-12100')
    if not cpu:
        cpu = find_cpu_by_generation(components['CPU'], 'i3-10100')
    if not cpu:
        cpu = find_cpu_by_generation(components['CPU'], 'i3')
    office_budget["components"]["CPU"] = cpu
    
    # GPU - встроенная графика или GT 710
    gpu = find_gpu_by_model(components['GPU'], 'GT 710')
    if not gpu:
        gpu = find_gpu_by_model(components['GPU'], 'GT 730')
    office_budget["components"]["GPU"] = gpu
    
    # RAM - 8GB DDR4
    ram = find_ram_by_specs(components['RAM'], '8gb', 'ddr4')
    if not ram:
        ram = find_ram_by_specs(components['RAM'], '8g', 'ddr4')
    office_budget["components"]["RAM"] = [ram] if ram else []
    
    # SSD - 240GB
    ssd = find_ssd_by_capacity(components['SSD'], '240gb')
    if not ssd:
        ssd = find_ssd_by_capacity(components['SSD'], '256gb')
    office_budget["components"]["SSD"] = [ssd] if ssd else []
    
    # Motherboard - H510
    mb = find_motherboard_by_chipset(components['Motherboard'], 'H510')
    if not mb:
        mb = find_motherboard_by_chipset(components['Motherboard'], 'H410')
    office_budget["components"]["Motherboard"] = mb
    
    # PSU - 400W
    psu = find_psu_by_power(components['PSU'], '400w')
    if not psu:
        psu = find_psu_by_power(components['PSU'], '450w')
    office_budget["components"]["PSU"] = psu
    
    # Case - MicroATX
    case = find_case_by_type(components['Case'], 'microatx')
    if not case:
        case = find_case_by_type(components['Case'], 'mini tower')
    office_budget["components"]["Case"] = case
    
    presets.append(office_budget)
    
    # 2. Игровая конфигурация среднего уровня
    gaming_mid = {
        "name": "Игровая (средний уровень)",
        "components": {}
    }
    
    # CPU - Intel Core i5
    cpu = find_cpu_by_generation(components['CPU'], 'i5-12400')
    if not cpu:
        cpu = find_cpu_by_generation(components['CPU'], 'i5-11400')
    if not cpu:
        cpu = find_cpu_by_generation(components['CPU'], 'i5')
    gaming_mid["components"]["CPU"] = cpu
    
    # GPU - GTX 1650 или RTX 3050
    gpu = find_gpu_by_model(components['GPU'], 'GTX 1650')
    if not gpu:
        gpu = find_gpu_by_model(components['GPU'], 'RTX 3050')
    if not gpu:
        gpu = find_gpu_by_model(components['GPU'], 'GTX 1660')
    gaming_mid["components"]["GPU"] = gpu
    
    # RAM - 16GB DDR4
    ram = find_ram_by_specs(components['RAM'], '16gb', 'ddr4')
    if not ram:
        ram = find_ram_by_specs(components['RAM'], '16g', 'ddr4')
    gaming_mid["components"]["RAM"] = [ram] if ram else []
    
    # SSD - 500GB
    ssd = find_ssd_by_capacity(components['SSD'], '500gb')
    if not ssd:
        ssd = find_ssd_by_capacity(components['SSD'], '480gb')
    gaming_mid["components"]["SSD"] = [ssd] if ssd else []
    
    # Motherboard - B660
    mb = find_motherboard_by_chipset(components['Motherboard'], 'B660')
    if not mb:
        mb = find_motherboard_by_chipset(components['Motherboard'], 'B560')
    gaming_mid["components"]["Motherboard"] = mb
    
    # PSU - 550W
    psu = find_psu_by_power(components['PSU'], '550w')
    if not psu:
        psu = find_psu_by_power(components['PSU'], '600w')
    gaming_mid["components"]["PSU"] = psu
    
    # Case - ATX Mid Tower
    case = find_case_by_type(components['Case'], 'atx mid tower')
    if not case:
        case = find_case_by_type(components['Case'], 'mid tower')
    gaming_mid["components"]["Case"] = case
    
    presets.append(gaming_mid)
    
    # 3. Профессиональная конфигурация для 1С
    professional_1c = {
        "name": "Профессиональная (1С)",
        "components": {}
    }
    
    # CPU - Intel Core i5 или AMD Ryzen 5
    cpu = find_cpu_by_generation(components['CPU'], 'i5-12400')
    if not cpu:
        cpu = find_cpu_by_generation(components['CPU'], 'ryzen 5 5600')
    if not cpu:
        cpu = find_cpu_by_generation(components['CPU'], 'i5')
    professional_1c["components"]["CPU"] = cpu
    
    # GPU - GTX 1650 или встроенная графика
    gpu = find_gpu_by_model(components['GPU'], 'GTX 1650')
    if not gpu:
        gpu = find_gpu_by_model(components['GPU'], 'GT 1030')
    professional_1c["components"]["GPU"] = gpu
    
    # RAM - 16GB DDR4
    ram = find_ram_by_specs(components['RAM'], '16gb', 'ddr4')
    if not ram:
        ram = find_ram_by_specs(components['RAM'], '16g', 'ddr4')
    professional_1c["components"]["RAM"] = [ram] if ram else []
    
    # SSD - 500GB
    ssd = find_ssd_by_capacity(components['SSD'], '500gb')
    if not ssd:
        ssd = find_ssd_by_capacity(components['SSD'], '480gb')
    professional_1c["components"]["SSD"] = [ssd] if ssd else []
    
    # Motherboard - B660 или B550
    mb = find_motherboard_by_chipset(components['Motherboard'], 'B660')
    if not mb:
        mb = find_motherboard_by_chipset(components['Motherboard'], 'B550')
    professional_1c["components"]["Motherboard"] = mb
    
    # PSU - 550W
    psu = find_psu_by_power(components['PSU'], '550w')
    if not psu:
        psu = find_psu_by_power(components['PSU'], '600w')
    professional_1c["components"]["PSU"] = psu
    
    # Case - ATX Mid Tower
    case = find_case_by_type(components['Case'], 'atx mid tower')
    if not case:
        case = find_case_by_type(components['Case'], 'mid tower')
    professional_1c["components"]["Case"] = case
    
    presets.append(professional_1c)
    
    # 4. Игровая конфигурация высокого уровня
    gaming_high = {
        "name": "Игровая (высокий уровень)",
        "components": {}
    }
    
    # CPU - Intel Core i7 или AMD Ryzen 7
    cpu = find_cpu_by_generation(components['CPU'], 'i7-12700')
    if not cpu:
        cpu = find_cpu_by_generation(components['CPU'], 'ryzen 7 5800')
    if not cpu:
        cpu = find_cpu_by_generation(components['CPU'], 'i7')
    gaming_high["components"]["CPU"] = cpu
    
    # GPU - RTX 3060 или RTX 4060
    gpu = find_gpu_by_model(components['GPU'], 'RTX 3060')
    if not gpu:
        gpu = find_gpu_by_model(components['GPU'], 'RTX 4060')
    if not gpu:
        gpu = find_gpu_by_model(components['GPU'], 'RTX 3070')
    gaming_high["components"]["GPU"] = gpu
    
    # RAM - 32GB DDR4
    ram = find_ram_by_specs(components['RAM'], '32gb', 'ddr4')
    if not ram:
        ram = find_ram_by_specs(components['RAM'], '32g', 'ddr4')
    gaming_high["components"]["RAM"] = [ram] if ram else []
    
    # SSD - 1TB
    ssd = find_ssd_by_capacity(components['SSD'], '1tb')
    if not ssd:
        ssd = find_ssd_by_capacity(components['SSD'], '1000gb')
    gaming_high["components"]["SSD"] = [ssd] if ssd else []
    
    # Motherboard - B660 или X570
    mb = find_motherboard_by_chipset(components['Motherboard'], 'B660')
    if not mb:
        mb = find_motherboard_by_chipset(components['Motherboard'], 'X570')
    gaming_high["components"]["Motherboard"] = mb
    
    # PSU - 650W
    psu = find_psu_by_power(components['PSU'], '650w')
    if not psu:
        psu = find_psu_by_power(components['PSU'], '700w')
    gaming_high["components"]["PSU"] = psu
    
    # Case - ATX Full Tower
    case = find_case_by_type(components['Case'], 'full tower')
    if not case:
        case = find_case_by_type(components['Case'], 'atx mid tower')
    gaming_high["components"]["Case"] = case
    
    presets.append(gaming_high)
    
    # 5. Домашняя мультимедиа конфигурация
    home_media = {
        "name": "Домашняя (мультимедиа)",
        "components": {}
    }
    
    # CPU - Intel Core i3 или AMD Ryzen 3
    cpu = find_cpu_by_generation(components['CPU'], 'i3-12100')
    if not cpu:
        cpu = find_cpu_by_generation(components['CPU'], 'ryzen 3 5300')
    if not cpu:
        cpu = find_cpu_by_generation(components['CPU'], 'i3')
    home_media["components"]["CPU"] = cpu
    
    # GPU - GTX 1650 или встроенная графика
    gpu = find_gpu_by_model(components['GPU'], 'GTX 1650')
    if not gpu:
        gpu = find_gpu_by_model(components['GPU'], 'GT 1030')
    home_media["components"]["GPU"] = gpu
    
    # RAM - 8GB DDR4
    ram = find_ram_by_specs(components['RAM'], '8gb', 'ddr4')
    if not ram:
        ram = find_ram_by_specs(components['RAM'], '8g', 'ddr4')
    home_media["components"]["RAM"] = [ram] if ram else []
    
    # SSD - 500GB
    ssd = find_ssd_by_capacity(components['SSD'], '500gb')
    if not ssd:
        ssd = find_ssd_by_capacity(components['SSD'], '480gb')
    home_media["components"]["SSD"] = [ssd] if ssd else []
    
    # Motherboard - H510 или A520
    mb = find_motherboard_by_chipset(components['Motherboard'], 'H510')
    if not mb:
        mb = find_motherboard_by_chipset(components['Motherboard'], 'A520')
    home_media["components"]["Motherboard"] = mb
    
    # PSU - 450W
    psu = find_psu_by_power(components['PSU'], '450w')
    if not psu:
        psu = find_psu_by_power(components['PSU'], '500w')
    home_media["components"]["PSU"] = psu
    
    # Case - MicroATX
    case = find_case_by_type(components['Case'], 'microatx')
    if not case:
        case = find_case_by_type(components['Case'], 'mini tower')
    home_media["components"]["Case"] = case
    
    presets.append(home_media)
    
    return presets

def save_presets(presets):
    """Сохраняет пресеты в JSON файл"""
    with open('data/presets.json', 'w', encoding='utf-8') as f:
        json.dump(presets, f, ensure_ascii=False, indent=2)
    print(f"Создано {len(presets)} типовых конфигураций")

def main():
    print("Создание типовых конфигураций на основе реальных компонентов...")
    presets = create_realistic_presets()
    save_presets(presets)
    
    # Выводим созданные конфигурации
    for preset in presets:
        print(f"\n{preset['name']}:")
        for category, component in preset['components'].items():
            if isinstance(component, list):
                print(f"  {category}: {', '.join(component) if component else 'Не найдено'}")
            else:
                print(f"  {category}: {component if component else 'Не найдено'}")

if __name__ == "__main__":
    main() 