def clean_file(input_file, output_file, number):
    """
    Читает файл, удаляет символы * и #, сохраняет результат в новый файл
    :param input_file: путь к исходному файлу
    :param output_file: путь к очищенному файлу
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            content = file.read()

        # Удаляем все * и #
        cleaned_content = content.replace('*', '').replace('#', '')#.replase(f" {number} ", " ")
        cleaned_content=cleaned_content.replace(f" {number} "," ").replace(f" {number}:"," ")
        with open(output_file, 'a', encoding='utf-8') as file:
            file.write(cleaned_content)

        print(f"Файл номер {number} успешно обработан. Результат сохранён в {output_file}")

    except FileNotFoundError:
        print(f"Ошибка:номер {number} файл не найден")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

def clear_file(output_file, number):
    """
    Читает файл, удаляет символы * и #, сохраняет результат в новый файл
    #:param input_file: путь к исходному файлу
    :param output_file: путь к очищенному файлу
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write("")
        print(f"Файл номер {number} успешно очищен. Результат сохранён в {output_file}")

    except FileNotFoundError:
        print(f"Ошибка:номер {number} файл не найден")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


# Пример использования
#input_path = 'input.txt'  # Путь к исходному файлу
output_path = 'output.txt'  # Путь для сохранения результата
clear_file(output_path,0)
clean_file(output_path, output_path, 1)

