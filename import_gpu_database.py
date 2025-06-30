import csv
from dbgpu import GPUDatabase
import datetime
from typing import Dict, Any

def convert_gpu_to_component_format(gpu_spec) -> Dict[str, Any]:
    """Конвертирует спецификацию GPU из dbgpu в формат компонента"""
    
    # Базовые характеристики с безопасным извлечением атрибутов
    component = {
        "name": getattr(gpu_spec, 'name', ''),
        "price": 0,  # Цена будет установлена позже или оставлена 0
        "manufacturer": getattr(gpu_spec, 'manufacturer', ''),
        "architecture": getattr(gpu_spec, 'architecture', ''),
        "foundry": getattr(gpu_spec, 'foundry', ''),
        "process_size": getattr(gpu_spec, 'process_size', ''),
        "transistor_count": getattr(gpu_spec, 'transistor_count', ''),
        "die_size": getattr(gpu_spec, 'die_size', ''),
        "chip_package": getattr(gpu_spec, 'chip_package', ''),
        "release_date": getattr(gpu_spec, 'release_date', ''),
        "generation": getattr(gpu_spec, 'generation', ''),
        "bus_interface": getattr(gpu_spec, 'bus_interface', ''),
        "base_clock": getattr(gpu_spec, 'base_clock', ''),
        "boost_clock": getattr(gpu_spec, 'boost_clock', ''),
        "memory_clock": getattr(gpu_spec, 'memory_clock', ''),
        "memory_size": getattr(gpu_spec, 'memory_size', ''),
        "memory_type": getattr(gpu_spec, 'memory_type', ''),
        "memory_bus": getattr(gpu_spec, 'memory_bus', ''),
        "memory_bandwidth": getattr(gpu_spec, 'memory_bandwidth', ''),
        "shading_units": getattr(gpu_spec, 'shading_units', ''),
        "texture_mapping_units": getattr(gpu_spec, 'texture_mapping_units', ''),
        "render_output_processors": getattr(gpu_spec, 'render_output_processors', ''),
        "streaming_multiprocessors": getattr(gpu_spec, 'streaming_multiprocessors', ''),
        "tensor_cores": getattr(gpu_spec, 'tensor_cores', ''),
        "ray_tracing_cores": getattr(gpu_spec, 'ray_tracing_cores', ''),
        "l1_cache": getattr(gpu_spec, 'l1_cache', ''),
        "l2_cache": getattr(gpu_spec, 'l2_cache', ''),
        "thermal_design_power": getattr(gpu_spec, 'thermal_design_power', ''),
        "board_length": getattr(gpu_spec, 'board_length', ''),
        "board_width": getattr(gpu_spec, 'board_width', ''),
        "board_slot_width": getattr(gpu_spec, 'board_slot_width', ''),
        "suggested_psu": getattr(gpu_spec, 'suggested_psu', ''),
        "power_connectors": getattr(gpu_spec, 'power_connectors', ''),
        "display_connectors": getattr(gpu_spec, 'display_connectors', ''),
        "directx_version": getattr(gpu_spec, 'directx_version', ''),
        "opengl_version": getattr(gpu_spec, 'opengl_version', ''),
        "vulkan_version": getattr(gpu_spec, 'vulkan_version', ''),
        "opencl_version": getattr(gpu_spec, 'opencl_version', ''),
        "cuda_version": getattr(gpu_spec, 'cuda_version', ''),
        "shader_model_version": getattr(gpu_spec, 'shader_model_version', ''),
        "pixel_rate": getattr(gpu_spec, 'pixel_rate_gpixel_s', ''),
        "texture_rate": getattr(gpu_spec, 'texture_rate_gtexel_s', ''),
        "half_float_performance": getattr(gpu_spec, 'half_float_performance_gflop_s', ''),
        "single_float_performance": getattr(gpu_spec, 'single_float_performance_gflop_s', ''),
        "double_float_performance": getattr(gpu_spec, 'double_float_performance_gflop_s', '')
    }
    
    # Удаляем пустые значения
    component = {k: v for k, v in component.items() if v not in [None, '', 'Unknown']}
    
    # Преобразуем все значения типа date в строку
    for k, v in component.items():
        if isinstance(v, datetime.date):
            component[k] = v.isoformat()
    
    return component

def import_gpu_database():
    """Импортирует базу данных видеокарт из dbgpu в CSV файл"""
    
    print("Загружаем базу данных видеокарт из dbgpu...")
    
    try:
        # Загружаем базу данных по умолчанию
        database = GPUDatabase.default()
        
        # Получаем список всех видеокарт
        gpu_names = database.names
        print(f"Найдено {len(gpu_names)} видеокарт в базе данных")
        
        # Конвертируем все видеокарты в наш формат
        gpu_components = []
        
        for gpu_name in gpu_names:
            try:
                gpu_spec = database[gpu_name]
                component = convert_gpu_to_component_format(gpu_spec)
                gpu_components.append(component)
            except Exception as e:
                print(f"Ошибка при конвертации {gpu_name}: {e}")
                continue
        
        print(f"Успешно конвертировано {len(gpu_components)} видеокарт")
        
        # Определяем все возможные поля
        all_fields = set()
        for component in gpu_components:
            all_fields.update(component.keys())
        
        # Сортируем поля для консистентности
        fieldnames = sorted(list(all_fields))
        
        # Сохраняем в CSV файл
        csv_filename = 'gpu-database.csv'
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(gpu_components)
        
        print(f"База данных видеокарт успешно сохранена в {csv_filename}")
        print(f"Добавлено {len(gpu_components)} видеокарт")
        print(f"Количество полей: {len(fieldnames)}")
        
        # Показываем несколько примеров
        print("\nПримеры импортированных видеокарт:")
        for i, gpu in enumerate(gpu_components[:3]):
            print(f"{i+1}. {gpu['name']}")
            print(f"   Производитель: {gpu.get('manufacturer', 'Не указан')}")
            print(f"   Архитектура: {gpu.get('architecture', 'Не указана')}")
            print(f"   Память: {gpu.get('memory_size', 'Не указана')} {gpu.get('memory_type', '')}")
            print()
        
        # Показываем список полей
        print("Поля в CSV файле:")
        for i, field in enumerate(fieldnames, 1):
            print(f"{i:2d}. {field}")
        
    except Exception as e:
        print(f"Ошибка при импорте базы данных: {e}")
        return False
    
    return True

if __name__ == "__main__":
    import_gpu_database() 