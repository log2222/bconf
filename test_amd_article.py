import csv
import re

def load_csv_data(csv_file: str) -> list:
    """Загружает данные из CSV файла"""
    data = []
    try:
        encodings = ['utf-8', 'cp1252', 'latin-1', 'iso-8859-1']
        for encoding in encodings:
            try:
                with open(csv_file, 'r', encoding=encoding) as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        data.append(row)
                print(f"Загружено {len(data)} записей из {csv_file} (кодировка: {encoding})")
                return data
            except UnicodeDecodeError:
                continue
        print(f"Не удалось загрузить {csv_file} ни с одной кодировкой")
    except Exception as e:
        print(f"Ошибка при загрузке {csv_file}: {e}")
    return data

def test_amd_article_search():
    """Тестирует поиск AMD CPU по article"""
    amd_csv = load_csv_data('amd-cpus.csv')
    
    if not amd_csv:
        print("Не удалось загрузить AMD CSV")
        return
    
    # Показываем первые несколько записей
    print("\nПервые 3 записи:")
    for i, row in enumerate(amd_csv[:3]):
        print(f"\nЗапись {i+1}:")
        for key, value in row.items():
            if value:  # Показываем только непустые значения
                print(f"  {key}: {value}")
    
    # Ищем конкретный article
    target_article = "YD1200BBM4KAE"
    print(f"\nИщем article: {target_article}")
    
    found = False
    for row in amd_csv:
        # Проверяем все возможные поля с article
        for key, value in row.items():
            if "Product ID" in key and value == target_article:
                print(f"Найдено в поле '{key}': {value}")
                print(f"Модель: {row.get('Model', 'НЕТ')}")
                found = True
                break
        if found:
            break
    
    if not found:
        print(f"Article {target_article} не найден")
        
        # Показываем все поля, содержащие "Product ID"
        print("\nПоля с 'Product ID':")
        for key in amd_csv[0].keys():
            if "Product ID" in key:
                print(f"  {key}")
        
        # Показываем несколько примеров Product ID
        print("\nПримеры Product ID:")
        for i, row in enumerate(amd_csv[:5]):
            for key, value in row.items():
                if "Product ID" in key and value:
                    print(f"  {key}: {value}")

if __name__ == "__main__":
    test_amd_article_search() 