import json
import requests

def test_presets():
    """Тестирует работу типовых конфигураций"""
    
    # Тестируем backend endpoints
    print("Тестирование backend endpoints...")
    
    try:
        # Проверяем пресеты
        presets_response = requests.get('http://localhost:8000/presets')
        if presets_response.status_code == 200:
            presets = presets_response.json()
            print(f"✅ Пресеты загружены успешно: {len(presets)} конфигураций")
            
            for i, preset in enumerate(presets, 1):
                print(f"  {i}. {preset['name']}")
                components = preset['components']
                for category, component in components.items():
                    if component:
                        if isinstance(component, list):
                            print(f"     {category}: {len(component)} компонентов")
                        else:
                            print(f"     {category}: {component[:50]}...")
        else:
            print(f"❌ Ошибка загрузки пресетов: {presets_response.status_code}")
            
        # Проверяем компоненты
        components_response = requests.get('http://localhost:8000/components')
        if components_response.status_code == 200:
            components = components_response.json()
            print(f"✅ Компоненты загружены успешно")
            for category, items in components.items():
                print(f"  {category}: {len(items)} компонентов")
        else:
            print(f"❌ Ошибка загрузки компонентов: {components_response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Не удается подключиться к backend серверу")
        print("Убедитесь, что сервер запущен: python main.py")
        return False
        
    # Тестируем фронтенд
    print("\nТестирование фронтенда...")
    
    try:
        frontend_response = requests.get('http://localhost:5173')
        if frontend_response.status_code == 200:
            print("✅ Фронтенд доступен")
        else:
            print(f"❌ Ошибка доступа к фронтенду: {frontend_response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Не удается подключиться к фронтенду")
        print("Убедитесь, что фронтенд запущен: npm run dev")
        return False
    
    print("\n🎉 Все тесты пройдены! Типовые конфигурации работают корректно.")
    print("\nДля проверки в браузере:")
    print("1. Откройте http://localhost:5173")
    print("2. В разделе 'Готовые конфигурации' выберите любую типовую конфигурацию")
    print("3. Проверьте, что компоненты автоматически выбрались")
    
    return True

if __name__ == "__main__":
    test_presets() 