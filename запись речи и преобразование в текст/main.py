import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
from platform import system
import tempfile
import os


"""
Данный код записывает речь через микрофон, преобразует в текст и возвращает егою Данный код кросс-платформенный
подходит для Linux, Windows, Macos, должным образом тестировался только на Linux Manjaro. Требует подключение к интернету.
"""

def record_audio(duration=5, sample_rate=44100, boost_db=10):
    #print(f"Запись в течение {duration} секунд...")
    try:
        # Получаем список доступных устройств
        devices = sd.query_devices()
        default_input = sd.default.device[0]

        if system() == 'Windows':
            channels = 1
            dtype = 'float32'
        elif system() == 'Darwin':  # macOS
            channels = 1
            dtype = 'float32'
        else:  # Linux и другие
            channels = 1
            dtype = 'float32'

        recording = sd.rec(
            int(duration * sample_rate),
            samplerate=sample_rate,
            channels=channels,
            dtype=dtype
        )
        sd.wait()

        # Усиление сигнала
        if boost_db > 0:
            boost_factor = 10 ** (boost_db / 20)
            recording = recording * boost_factor

        return recording, sample_rate

    except Exception as e:
        return None, None


def recognize_speech(audio_data, sample_rate, language='ru-RU'):
    recognizer = sr.Recognizer()

    # Сохраняем во временный файл для обработки
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmpfile:
        wav.write(tmpfile.name, sample_rate, (audio_data * 32767).astype(np.int16))

        with sr.AudioFile(tmpfile.name) as source:
            try:
                audio = recognizer.record(source)
                text = recognizer.recognize_google(audio, language=language)
                #print(f"Распознанный текст: {text}")
                return text
            except sr.UnknownValueError:
                pass
                #print("Речь не распознана")
            except sr.RequestError as e:
                pass
                #print(f"Ошибка сервиса распознавания; {e}")
            except Exception as e:
                pass
                #print(f"Неожиданная ошибка: {e}")
            finally:
                os.unlink(tmpfile.name)
    return None


def process_audio_recognition(duration=5, boost_db=10, save_to_file=True, filename="recorded_audio.wav"):
    """
    Основная функция для записи и распознавания аудио
    :param duration: Длительность записи в секундах
    :param boost_db: Усиление звука в децибелах
    :param save_to_file: Сохранять ли запись в файл
    :param filename: Имя файла для сохранения
    :return: Распознанный текст или None
    """
    audio_data, sample_rate = record_audio(duration=duration, boost_db=boost_db)

    if audio_data is None:
        print("Ошибка: не удалось записать аудио")
        return None

    recognized_text = recognize_speech(audio_data, sample_rate)

    if save_to_file:
        try:
            wav.write(filename, sample_rate, (audio_data * 32767).astype(np.int16))
            #print(f"Аудио сохранено как '{filename}'")
        except Exception as e:
            #print(f"Ошибка при сохранении аудио: {e}")
            pass

    return recognized_text


def main():
    # Параметры записи
    duration = 5  # секунд
    boost = 10  # dB
    text = process_audio_recognition(duration=duration, boost_db=boost)

    if text:
        print("Финальный результат распознавания:", text)


if __name__ == "__main__":
    main()
