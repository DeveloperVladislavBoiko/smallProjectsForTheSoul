from gtts import gTTS
import os
import platform
import subprocess
import sys

"""
Данный код требует постоянного подключения к интернету, код кросплатформенный, но доджным образом текстиролвался только на Linux manjaro 
"""

def text_to_speech(file_path, lang='ru', slow=False, voice_variant='com'):
    """
    Преобразует текст из файла в речь и воспроизводит её.
    Возвращает:
        True - если озвучивание успешно
        False - если произошла ошибка
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read().strip()

        if not text:
            return False

        tts = gTTS(text=text, lang=lang, slow=slow, tld=voice_variant)
        output_file = "output_voice.mp3"
        tts.save(output_file)

        # Возвращаем статус воспроизведения
        return play_audio(output_file)

    except FileNotFoundError:
        return False
    

def play_audio(file_path):
    """
    Воспроизводит аудиофайл.
    Возвращает:
        True - если воспроизведение успешно
        False - если не удалось воспроизвести
    """
    system = platform.system()

    players = {
        'Windows': [
            ['cmd', '/c', 'start', '/MIN', '', file_path],
            ['powershell', '-c', f"(New-Object Media.SoundPlayer '{file_path}').PlaySync()"]
        ],
        'Darwin': [['afplay']],
        'Linux': [
            ['mpv', '--really-quiet', file_path],
            ['mpg123', '-q', file_path],
            ['ffplay', '-nodisp', '-autoexit', file_path],
            ['vlc', '--play-and-exit', '--quiet', file_path],
            ['paplay', file_path]
        ]
    }.get(system, [])

    for player_cmd in players:
        try:
            # Проверка наличия плеера (Linux/Mac)
            if system in ['Linux', 'Darwin']:
                try:
                    subprocess.run(
                        ['which', player_cmd[0]],
                        check=True,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL
                    )
                except subprocess.CalledProcessError:
                    continue

            # Воспроизведение
            subprocess.run(
                player_cmd,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                shell=(system == 'Windows')
            )
            return True  # Успешное воспроизведение

        except subprocess.CalledProcessError:
            continue
        except Exception as e:
            print(f"Ошибка при воспроизведении: {e}", file=sys.stderr)
            continue

    print("Не удалось воспроизвести аудио. Установите один из плееров:",
          ', '.join(cmd[0] for cmd in players), file=sys.stderr)
    return False


if text_to_speech("example.txt", lang='ru'):
    print("Озвучивание прошло успешно!")
else:
    print("Не удалось выполнить озвучивание.")
