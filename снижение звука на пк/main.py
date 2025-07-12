import platform
import subprocess
from typing import Union


"""
Данная функция кросс-платформенная подходит под Linux, Windows, Macos
Функция должным образом тестировалась только на Linux Manjaro
"""


def decrease_volume(percent: Union[int, float]) -> bool:
    system = platform.system().lower()
    percent = float(percent)

    try:
        if system == "windows":
            from ctypes import cast, POINTER
            from comtypes import CLSCTX_ALL
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            current_volume = volume.GetMasterVolumeLevelScalar()
            new_volume = max(0.0, current_volume - percent / 100.0)
            volume.SetMasterVolumeLevelScalar(new_volume, None)
            return True

        elif system == "linux":
            import alsaaudio

            mixer = alsaaudio.Mixer()
            current_volume = mixer.getvolume()[0]  # У ALSA может быть несколько каналов
            new_volume = max(0, int(current_volume - percent))
            mixer.setvolume(new_volume)
            return True

        elif system == "darwin":  # macOS
            current_volume = float(subprocess.check_output(["osascript", "-e", "output volume of (get volume settings)"]))
            new_volume = max(0, current_volume - percent)
            subprocess.run(["osascript", "-e", f"set volume output volume {new_volume}"])
            return True

        else:
            return False

    except Exception as e:
        return False

# Пример использования
decrease_volume(10)  # Уменьшает громкость на 10%
