def clean_file(input_file, output_file, char):
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
        #cleaned_content=cleaned_content.replace(f" {number} "," ").replace(f" {number}:"," ")
        with open(output_file, char, encoding='utf-8') as file:
            file.write(cleaned_content)

        print(f"Файл успешно обработан. Результат сохранён в {output_file}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

def clear_file(output_file, char):
    clear_file(output_file, output_file, char)

# Пример использования
input_path = 'input.txt'  # Путь к исходному файлу
output_path = 'output.txt'  # Путь для сохранения результата
print("введите 'a' если хотите дописать, если хотите перезаписать файл введите 'w' ")
char=input()
clean_file(input_path, output_path, char)
