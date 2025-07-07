import os


def find_file_path(filename, search_path=None):
    """
    Находит полный путь к файлу во всей файловой системе

    :param filename: Имя файла для поиска (например, "file.txt")
    :param search_path: Корневая директория для поиска (None - корень системы)
    :return: Полный путь к файлу или None, если не найден
    код кросплотфоменный, linux, Macos, Windows, но протекстирован только на linux Manjaro
    """
    if search_path is None:
        search_path = 'C:\\' if os.name == 'nt' else '/'

    search_path = os.path.abspath(os.path.normpath(search_path))

    for root, dirs, files in os.walk(search_path):
        try:  # Добавляем обработку исключений для защищенных директорий
            for file in files:
                if file == filename:
                    return os.path.join(root, file)
        except PermissionError:
            continue
        except Exception as e:
            print(f"Ошибка при доступе к {root}: {e}")
            continue

    return None


file_to_find=input()
print(f"Ищем файл '{file_to_find}' во всей файловой системе...")
found_path = find_file_path(file_to_find)

if found_path:
    print(f"Файл найден: {found_path}")
else:
    print(f"Файл '{file_to_find}' не найден")
