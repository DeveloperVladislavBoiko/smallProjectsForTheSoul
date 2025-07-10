import os
import platform
import subprocess
from pathlib import Path


def show_file_as_notification(filename):
    """
    Читает содержимое файла и показывает его в виде уведомления.
    Поддерживает Windows, Linux и macOS.
    Должным образом тестировал только на linux manjaro
    """
    try:
        # Проверяем существование файла
        if not Path(filename).is_file():
            raise FileNotFoundError(f"Файл '{filename}' не найден")

        # Читаем содержимое файла
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read().strip()

            # Обрезаем слишком длинный текст
            if len(content) > 500:
                content = content[:500] + "... [текст обрезан]"

        # Определяем ОС и выбираем способ уведомления
        system = platform.system().lower()

        if system == 'linux':
            # Уведомления через notify-send (требуется libnotify-bin)
            try:
                subprocess.run(['notify-send', "Voice help", content])
            except FileNotFoundError:
                print("Ошибка: для уведомлений в Linux требуется 'notify-send'")
                print("Установите: sudo apt install libnotify-bin")
                print("Voice help:\n", content)

        elif system == 'windows':
            # Уведомления через win10toast
            try:
                from win10toast import ToastNotifier
                toaster = ToastNotifier()
                toaster.show_toast("Voice help", content, duration=10)
            except ImportError:
                print("Ошибка: для уведомлений в Windows требуется 'win10toast'")
                print("Установите: pip install win10toast")
                print("Содержимое файла:\n", content)

        elif system == 'darwin':  # macOS
            try:
                script = f'display notification "{content}" with title ""Voice help""'
                subprocess.run(['osascript', '-e', script])
            except Exception as e:
                print("Ошибка при показе уведомления в macOS:", e)
                print("Содержимое файла:\n", content)

        else:
            print(f"Неподдерживаемая ОС: {system}")
            print("Содержимое файла:\n", content)

    except Exception as e:
        print(f"Ошибка при отображении уведомления: {e}")

show_file_as_notification("sistem.txt")
