import math
import matplotlib.pyplot as plt

# Файл для хранения данных о скорости
SPEED_DATA_FILE = "speed.txt"  # Файл для хранения данных о скорости

# Данные для моделирования
f = open('altitude.txt', encoding='utf-8').readlines()  # Убедитесь, что файл читается с правильной кодировкой

def read_speed_data(filename):
    """Считывает данные скорости из файла и возвращает список."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            speeds = []
            for line in f:
                try:
                    # Извлекаем значение скорости (первое число после ": ")
                    parts = line.split(': ')
                    if len(parts) > 1:
                        speed = float(parts[1].strip().replace(',', '.').split()[0])
                        speeds.append(speed)
                except (ValueError, IndexError) as e:
                    print(f"Ошибка при обработке строки: {line.strip()}. Причина: {e}")
        return speeds
    except FileNotFoundError:
        print(f"Файл {filename} не найден.")
        return []

# Чтение данных о скорости (хотя они не нужны в этом коде)
speeds = read_speed_data(SPEED_DATA_FILE)

hh = []
for i in f:
    try:
        # Заменяем запятую на точку и убираем лишние символы
        h = float(i.split(': ')[1].strip().replace(',', '.').split()[0])  # Убираем все, что идет после числа
        hh.append(h)
        if h > 116000:
            break
    except (ValueError, IndexError) as e:
        print(f"Ошибка при обработке строки: {i.strip()}. Причина: {e}")

# Константы
G = 6.67430e-11  # Гравитационная постоянная
M_earth = 5.972e24  # Масса Земли
R_earth = 6371000  # Радиус Земли
theta_0 = 90  # Начальный угол в градусах
tau = 87  # Константа времени
t_end = 225  # Конечное время симуляции
dt = 1  # Шаг времени
air_density = 1.225  # Плотность воздуха (кг/м^3) на уровне моря
drag_coefficient = 0.75  # Коэффициент сопротивления
rocket_area = 10.0  # Площадь поперечного сечения ракеты (м^2)

# Параметры ракеты
M0 = 270000  # Начальная масса ракеты (кг)
Mi = 155000  # Масса ракеты после выработки топлива (кг)
ti = 100  # Время работы двигателей (с)
ki = (M0 - Mi) / ti  # Расход топлива за единицу времени (кг/с)

# ---- Расчет силы сопротивления ----
def F_drag(v):
    return 0.5 * air_density * v**2 * drag_coefficient * rocket_area

# ---- Функция тяги ----
def F_t():
    return 6075 * 1000  # Постоянная тяга (Н)

# ---- Угол наклона ----
def theta(t):
    return math.radians(theta_0 - (math.radians(5) * t / tau))  # Угол меняется с течением времени

# ---- Масса ракеты ----
def m(t):
    mass = M0 - ki * t  # Масса ракеты на t-й секунде
    return mass if mass > 0 else 0.01  # Возвращаем минимальную массу, чтобы избежать деления на ноль

# ---- Начальные условия ----
h = 0  # Высота (м)
v_y = 0  # Начальная скорость по оси Y (м/с)
v_x = 0  # Начальная скорость по оси X (м/с)

# ---- Списки для хранения данных ----
heights = [h]

# ---- Симуляция ----
for t in range(0, t_end, dt):
    mass = m(t)  # Масса ракеты
    thrust = F_t()  # Тяга

    # Проверка на нулевую массу
    if mass == 0:
        print("Масса ракеты достигла нуля, симуляция остановлена.")
        break

    # Расчет гравитационного притяжения в зависимости от высоты
    current_g = G * M_earth / ((R_earth + h) ** 2)

    # Угол наклона
    angle = theta(t)

    # Ускорение по осям
    a_0y = (thrust / mass) * math.sin(angle) - current_g - (F_drag(v_y) / mass)  # Учет сопротивления
    a_0x = (thrust / mass) * math.cos(angle)  # Ускорение по оси X

    # Обновление скоростей
    v_y += a_0y * dt
    v_x += a_0x * dt

    # Расчет высоты
    h += v_y * dt + (a_0y / 2) * dt**2  # Высота на текущий момент времени

    heights.append(h)

    if h > 116000:
        break

# ---- Дополнение до нужной длины ----
while len(heights) < len(hh):
    heights.append(heights[-1])

# ---- Расчет относительной ошибки для высоты ----
relative_error_height = sum([abs(heights[i] - hh[i]) / hh[i] for i in range(len(hh)) if hh[i] > 0]) / len([hh[i] for i in range(len(hh)) if hh[i] > 0])
print(f'Относительная ошибка по высоте: {relative_error_height:.4f}')

# ---- Построение графиков ----
fig, axs = plt.subplots(1, 1, figsize=(10, 6))

# ---- График высоты ----
axs.plot(heights, label='Моделирование')
axs.plot(hh, label='KSP симуляция')
axs.set_xlabel('Время (с)')
axs.set_ylabel('Высота (м)')
axs.set_title('Сравнение высоты ракеты Voyager 2')
axs.legend()
axs.grid(True)

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()

