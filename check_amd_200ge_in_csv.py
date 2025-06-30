import csv
import re

def check_amd_200ge_in_csv():
    """Проверяет наличие Athlon 200GE в CSV файле AMD"""
    encodings = ['utf-8', 'cp1252', 'latin-1', 'iso-8859-1']
    
    for encoding in encodings:
        try:
            with open('amd-cpus.csv', 'r', encoding=encoding) as f:
                lines = f.readlines()
                
            print(f"Успешно прочитан файл с кодировкой: {encoding}")
            print(f"Всего строк в amd-cpus.csv: {len(lines)}")
            
            # Ищем Athlon 200GE
            athlon_200ge_found = False
            for i, line in enumerate(lines):
                if "200GE" in line or "200 GE" in line:
                    print(f"Строка {i+1}: {line.strip()}")
                    athlon_200ge_found = True
            
            if not athlon_200ge_found:
                print("Athlon 200GE не найден в CSV файле!")
            
            # Ищем по артикулу YD200GC6M2OFB
            article_found = False
            for i, line in enumerate(lines):
                if "YD200GC6M2OFB" in line:
                    print(f"Артикул YD200GC6M2OFB найден в строке {i+1}: {line.strip()}")
                    article_found = True
            
            if not article_found:
                print("Артикул YD200GC6M2OFB не найден в CSV файле!")
            
            # Показываем первые несколько строк для понимания структуры
            print("\nПервые 5 строк файла:")
            for i in range(min(5, len(lines))):
                print(f"{i+1}: {lines[i].strip()}")
            
            break  # Если успешно прочитали, выходим из цикла
                
        except UnicodeDecodeError:
            print(f"Не удалось прочитать с кодировкой: {encoding}")
            continue
        except Exception as e:
            print(f"Ошибка при чтении файла с кодировкой {encoding}: {e}")
            continue

if __name__ == "__main__":
    check_amd_200ge_in_csv() 