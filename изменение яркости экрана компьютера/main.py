import platform
import subprocess
import platform
import subprocess
import os

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

def get_brightness():
    """
    Определяет текущую яркость экрана и возвращает её значение (0-100%).
    """
    system = platform.system().lower()

    try:
        if system == "linux":
            try:
                result = subprocess.run(
                    ["brightnessctl", "get"],
                    capture_output=True,
                    text=True,
                    check=True
                )
                current = int(result.stdout.strip())
                max_result = subprocess.run(
                    ["brightnessctl", "max"],
                    capture_output=True,
                    text=True,
                    check=True
                )
                max_brightness = int(max_result.stdout.strip())
                return int((current / max_brightness) * 100)
            except (FileNotFoundError, subprocess.CalledProcessError):
                pass

            try:
                backlight_path = "/sys/class/backlight/"
                if os.path.exists(backlight_path):
                    device = os.listdir(backlight_path)[0]
                    with open(f"{backlight_path}{device}/brightness", "r") as f:
                        current = int(f.read().strip())
                    with open(f"{backlight_path}{device}/max_brightness", "r") as f:
                        max_brightness = int(f.read().strip())
                    return int((current / max_brightness) * 100)
            except Exception:
                pass

            try:
                result = subprocess.run(
                    ["xrandr", "--verbose"],
                    capture_output=True,
                    text=True,
                    check=True
                )
                for line in result.stdout.splitlines():
                    if "Brightness:" in line:
                        brightness = float(line.split(":")[1].strip())
                        return int(brightness * 100)
            except (FileNotFoundError, subprocess.CalledProcessError):
                pass

        elif system == "windows":
            try:
                import wmi
                c = wmi.WMI(namespace='wmi')
                current = c.WmiMonitorBrightness()[0].CurrentBrightness
                return int(current)
            except Exception:
                pass

        elif system == "darwin": # macOS
            try:
                result = subprocess.run(
                    ["brightness", "-l"],
                    capture_output=True,
                    text=True,
                    check=True
                )
                for line in result.stdout.splitlines():
                    if "display 0" in line.lower():
                        brightness = float(line.split(" ")[-1].strip())
                        return int(brightness * 100)
            except (FileNotFoundError, subprocess.CalledProcessError):
                pass

    except Exception as e:
        print(f"Ошибка при определении яркости: {e}")

    return None  # Если не удалось определить яркость


def increase_brightness(level):
    if (not -100 <= level <= 100):
       return  0
    if (not(0<= get_brightness()+level <=100)):
        return -1
    else :
        set_brightness(get_brightness()+level)
        return 1

print(increase_brightness(int(input())))
