import platform
import subprocess

"""
Данная функция кросс-платформенная поддерживается на Linux, Macos, Windows
Должным образом тестировалась только на Linux Manjaro
"""

def set_brightness(level):

    if not 0 <= level <= 100:
        return False

    system = platform.system().lower()

    try:
        if system == "linux":
            try:
                subprocess.run(
                    ["brightnessctl", "set", f"{level}%"],
                    check=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                return True
            except (FileNotFoundError, subprocess.CalledProcessError):
                pass

            try:
                result = subprocess.run(
                    ["xrandr", "--verbose"],
                    capture_output=True,
                    text=True
                )
                monitor = result.stdout.split(" connected")[0].split()[-1]

                subprocess.run(
                    ["xrandr", "--output", monitor, "--brightness", str(level / 100)],
                    check=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                return True
            except (FileNotFoundError, subprocess.CalledProcessError):
                return False

        elif system == "windows":
            try:
                import wmi
                c = wmi.WMI(namespace='wmi')
                methods = c.WmiMonitorBrightnessMethods()[0]
                methods.WmiSetBrightness(level, 0)
                return True
            except Exception as e:
                return False

        elif system == "darwin": # macOS
            try:
                subprocess.run(
                    ["brightness", str(level / 100)],
                    check=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                return True
            except (FileNotFoundError, subprocess.CalledProcessError):
                return False

        else:
            return False

    except Exception as e:
        return False

set_brightness(50)
