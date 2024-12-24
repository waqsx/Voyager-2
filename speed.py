import krpc
import time

class FlightSpeedRecorder:
    def __init__(self, connection_name="Voyager-2", filename="speed.txt"):
        self.conn = krpc.connect(name=connection_name)
        self.vessel = self.conn.space_center.active_vessel
        self.space_center = self.conn.space_center
        self.filename = filename
        self.file = None
        self.start_time = None

    def start_recording(self):
        try:
            self.file = open(self.filename, "w")
            self.start_time = self.space_center.ut
            print(f"Начало записи данных о скорости полета в {self.filename}")
            self.record_loop()
        except Exception as e:
            print(f"Ошибка при запуске записи: {e}")
            self.stop_recording()

    def record_loop(self):
        try:
            while True:
                current_time = self.space_center.ut - self.start_time 
                speed = self.vessel.flight(self.vessel.orbit.body.reference_frame).speed 
                altitude = self.vessel.flight().mean_altitude
                self.file.write(f"{current_time:.0f}: {speed:.1f}\n")  
                time.sleep(0.1)  # Запись данных 10 раз в секунду

                if altitude > 116000: 
                    print("\nДостигнута высота 100000 м. Запись данных завершена.")
                    self.stop_recording()
                    break

        except KeyboardInterrupt:
            print("\nЗапись данных прервана пользователем.")
            self.stop_recording()
        except Exception as e:
            print(f"Ошибка во время записи: {e}")
            self.stop_recording()

    def stop_recording(self):
        if self.file:
            self.file.close()
            print("Запись данных завершена и файл закрыт.")

    def run(self):
        self.start_recording()

if __name__ == "__main__":
    try:
        recorder = FlightSpeedRecorder()
        recorder.run()

    except KeyboardInterrupt:
        print("\nЗавершение работы программы.")
    except Exception as e:
        print(f"\nОшибка во время выполнения: {e}")