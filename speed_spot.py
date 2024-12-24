import matplotlib.pyplot as plt
import numpy as np

# Чтение данных о скорости ракеты из файла
times = []
speeds = []

# Открываем файл и считываем данные
with open('speed.txt', 'r') as file:
    for line in file:
        index, speed = line.split(':')
        times.append(int(index.strip()))
        speeds.append(float(speed.strip()))

# Нормализация значений скорости для соответствия модели
max_real_speed = max(speeds)
scaling_factor = 1150 / max_real_speed  # Приведение максимальной скорости к 1150 м/с

normalized_speeds = [speed * scaling_factor for speed in speeds]

# Создание математической модели скорости
def voyager_speed_model(t):
    max_speed = 1150  # Максимальная скорость (м/с)
    decay_time = 100  # Время (с), после которого начинается спад скорости
    return max_speed * (1 - np.exp(-t / decay_time))  # Модель скорости

# Создание массива времени для модели
model_times = np.linspace(0, max(times), 100)
model_speeds = voyager_speed_model(model_times)

# Построение графиков
plt.figure(figsize=(12, 6))

# График нормализованных данных
plt.plot(times, normalized_speeds, label='Скорость ракеты (KSP)', color='blue')

# График математической модели
plt.plot(model_times, model_speeds, label='Модель скорости (Voyager 2)', color='orange', linestyle='--')

plt.xlabel('Время (с)')
plt.ylabel('Скорость (м/с)')
plt.title('Сравнение нормализованной скорости ракеты из KSP и модели Voyager 2')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

