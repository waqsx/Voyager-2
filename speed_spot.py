import math
import matplotlib.pyplot as plt

# ---- Настройки для сбора данных о скорости  ----
SPEED_DATA_FILE = "speed.txt"  # Файл для хранения данных о скорости

# ---- Функции для считывания данных  ----
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

# ---- Чтение данных о скорости из файла ----
ksp_speeds = read_speed_data(SPEED_DATA_FILE)
if not ksp_speeds:
    print("Данные скорости из KSP не были загружены. Выполнение программы прекращено.")
    exit()


# ---- Константы ----
G = 6.67430e-11  # Гравитационная постоянная
M_earth = 5.972e24  # Масса Земли
R_earth = 6371000  # Радиус Земли
F_thrust = 6075 * 1000  # Тяга (Н)

# ---- Параметры ракеты ----
M0 = 403000  # Начальная масса ракеты (кг)
Mi = 155000  # Масса ракеты после выработки топлива (кг)
ti = 100  # Время работы двигателей (с)
ki = (M0 - Mi) / ti  # Расход топлива за единицу времени (кг/с)

# --- Параметры угла ----
theta_0 = 90  # Начальный угол в градусах
gamma = 5  # Изменение угла за время работы ступени
tau = 87  # Константа времени

# ---- Время симуляции ----
t_end = 360  # Конечное время симуляции
dt = 1  # Шаг времени

# ---- Функции для расчета переменных ----
def calculate_mass(t):
    """Рассчитывает массу ракеты на момент времени t."""
    mass = M0 - ki * t
    return mass if mass > 0 else 0.01 # минимальная масса для избегания деления на ноль

def calculate_gravity(h):
   """Рассчитывает ускорение свободного падения на высоте h."""
   return (G * M_earth) / ((R_earth + h) ** 2)

def calculate_angle(t):
   """Рассчитывает угол наклона ракеты в текущий момент времени."""
   return math.radians(theta_0 - (math.radians(gamma) * t / tau))

def calculate_speed(v_0y, v_0x):
    """Рассчитывает общую скорость ракеты"""
    return math.sqrt(v_0y**2 + v_0x**2)

# --- Расчет ускорения по осям ---
def calculate_acceleration_y(F_thrust,mass, angle, gravity):
    """Рассчитывает ускорение по оси y."""
    return (F_thrust / mass) * math.sin(angle) - gravity

def calculate_acceleration_x(F_thrust, mass, angle):
    """Рассчитывает ускорение по оси x."""
    return (F_thrust / mass) * math.cos(angle)


# ---- Инициализация ----
h = 0  # Высота (м)
v_y = 0  # Вертикальная скорость (м/с)
v_x = 0  # Горизонтальная скорость (м/с)
speeds = [0] # массив скоростей
model_speeds = []

# --- Моделирование ---
for t in range(0, t_end, dt):
    mass = calculate_mass(t)
    gravity = calculate_gravity(h)
    angle = calculate_angle(t)

    # Проверка на нулевую массу
    if mass == 0:
         print("Масса ракеты достигла нуля, симуляция остановлена.")
         break

    # Расчет ускорений
    a_y = calculate_acceleration_y(F_thrust,mass,angle,gravity)
    a_x = calculate_acceleration_x(F_thrust,mass,angle)

    # Расчет скоростей
    v_y += a_y * dt
    v_x += a_x * dt
    speed = calculate_speed(v_y,v_x)
    
    # Расчет высоты (для гравитации)
    h += v_y * dt + (a_y / 2) * dt**2

    model_speeds.append(speed)
    speeds.append(speed)
    if h > 60000:
       break

# --- Дополнение списков до одной длины
while len(model_speeds) < len(ksp_speeds):
    model_speeds.append(model_speeds[-1])
    

# ---- Расчет относительной ошибки для скорости  ----
relative_error_speed = sum([abs(model_speeds[i] - ksp_speeds[i]) / ksp_speeds[i] for i in range(len(ksp_speeds)) if ksp_speeds[i] > 0]) / len([ksp_speeds[i] for i in range(len(ksp_speeds)) if ksp_speeds[i] > 0])
print(f'Относительная ошибка по скорости: {relative_error_speed:.4f}')


# --- Визуализация ----
plt.figure(figsize=(10, 6))
plt.plot(model_speeds, label='Модель')
plt.plot(ksp_speeds, label='KSP')
plt.xlabel('Время (с)')
plt.ylabel('Скорость (м/с)')
plt.title('Сравнение скорости ракеты: Модель vs KSP')
plt.grid(True)
plt.legend()
plt.show()