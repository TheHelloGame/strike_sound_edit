import socket
import json
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import math

# Получение имени компьютера
pc_name = socket.gethostname()
settings_file_path = "settings.json"
try:
    with open(settings_file_path, "r") as settings_file:
        settings = json.load(settings_file)

except FileNotFoundError:
    print(f"Файл настроек не найден: {settings_file_path}")
except json.JSONDecodeError:
    print(f"Ошибка декодирования JSON в файле настроек: {settings_file_path}")

# Получение устройства воспроизведения по умолчанию с использованием PyCAW
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# Получение текущей громкости левого канала
currentVolumeL = volume.GetChannelVolumeLevelScalar(0)
currentVolumeR = volume.GetChannelVolumeLevelScalar(1)
# Получение громкости правого канала
print(f"Имя компьютера: {pc_name}")
print(f"До коррекции: L= {currentVolumeL*100:.2f}%, R= {currentVolumeR*100:.2f}%")
if pc_name in settings:
    volumeL = settings[pc_name]["L"] / 100
    volumeR = settings[pc_name]["R"] / 100
    volume.SetChannelVolumeLevelScalar(0, volumeL, None)  # Левый канал
    volume.SetChannelVolumeLevelScalar(1, volumeR, None)  # Правый канал
    print(f"После коррекции: L= {volumeL*100}%, R ={volumeR*100}%")
else:
    print(f"Настроек не найдено")

