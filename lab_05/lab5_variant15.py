import tkinter as tk
from tkinter import ttk, messagebox
import datetime

# ==============================================================================
# 1. КЛАССЫ МОДЕЛИ (Бизнес-логика, полностью отделенная от tkinter)
# ==============================================================================

class Zone:
    """Базовый класс зоны безопасности."""
    def __init__(self, name: str, x1: float, y1: float, x2: float, y2: float):
        self.name = name
        self.x1 = min(x1, x2)
        self.y1 = min(y1, y2)
        self.x2 = max(x1, x2)
        self.y2 = max(y1, y2)

    def contains(self, rx: float, ry: float) -> bool:
        """Проверяет, находится ли точка (rx, ry) внутри зоны."""
        return self.x1 <= rx <= self.x2 and self.y1 <= ry <= self.y2

    def get_status(self) -> str:
        """Возвращает статус безопасности (переопределяется в потомках)."""
        return "SAFE"


class WarningZone(Zone):
    """Класс зоны предупреждения (Желтая зона)."""
    def get_status(self) -> str:
        return "WARNING"


class StopZone(Zone):
    """Класс зоны остановки (Красная зона)."""
    def get_status(self) -> str:
        return "STOP"


class SafetyController:
    """Контроллер безопасности, управляющий роботом и зонами."""
    def __init__(self, field_width=10.0, field_height=10.0):
        self.width = field_width
        self.height = field_height
        self._robot_x = 1.0
        self._robot_y = 1.0
        self.zones = []

    @property
    def robot_x(self) -> float:
        return self._robot_x

    @robot_x.setter
    def robot_x(self, value: float):
        if not 0.0 <= value <= self.width:
            raise ValueError(f"Координата X должна быть в пределах 0...{self.width} м")
        self._robot_x = value

    @property
    def robot_y(self) -> float:
        return self._robot_y

    @robot_y.setter
    def robot_y(self, value: float):
        if not 0.0 <= value <= self.height:
            raise ValueError(f"Координата Y должна быть в пределах 0...{self.height} м")
        self._robot_y = value

    def add_zone(self, zone: Zone):
        """Добавление зоны в контроллер."""
        self.zones.append(zone)

    def check_safety(self) -> tuple[str, str]:
        """Проверяет положение робота относительно всех зон."""
        current_status = "SAFE"
        triggering_zone = "Нет нарушений"
        
        for zone in self.zones:
            if zone.contains(self._robot_x, self._robot_y):
                if zone.get_status() == "STOP":
                    return "STOP", zone.name
                elif zone.get_status() == "WARNING":
                    current_status = "WARNING"
                    triggering_zone = zone.name
                    
        return current_status, triggering_zone

    def move_robot(self, dx: float, dy: float):
        """Перемещает робота на смещение dx, dy с проверкой границ."""
        self.robot_x = self._robot_x + dx
        self.robot_y = self._robot_y + dy

    def __str__(self) -> str:
        """Строковое представление состояния контроллера."""
        status, zone_name = self.check_safety()
        return f"Робот: X={self._robot_x:.2f}м, Y={self._robot_y:.2f}м | Статус: {status} ({zone_name})"


# ==============================================================================
# 2. КЛАСС ИНТЕРФЕЙСА ПРИЛОЖЕНИЯ (Tkinter)
# ==============================================================================

class SafetyApp(tk.Tk):
    """Главное окно графического интерфейса приложения."""
    SCALE = 50  # 1 метр = 50 пикселей

    def __init__(self, controller: SafetyController):
        super().__init__()
        self.controller = controller
        
        self.title("Система контроля зон безопасности мехатронного объекта")
        self.resizable(False, False)
        self.status_text = tk.StringVar()
        
        self._build_widgets()
        self._refresh_ui()
        self.bind("<KeyPress>", self._on_key_press)

    def _build_widgets(self):
        """Создание и размещение элементов управления."""
        canvas_w = int(self.controller.width * self.SCALE)
        canvas_h = int(self.controller.height * self.SCALE)
        
        self.canvas = tk.Canvas(self, width=canvas_w, height=canvas_h, bg="#f0f0f0", relief="sunken", bd=2)
        self.canvas.grid(row=0, column=0, padx=10, pady=10, rowspan=2)
        
        right_panel = ttk.Frame(self)
        right_panel.grid(row=0, column=1, padx=10, pady=10, sticky="n")
        
        control_frame = ttk.LabelFrame(right_panel, text="Управление роботом")
        control_frame.pack(fill="x", pady=5)
        
        btn_grid = ttk.Frame(control_frame)
        btn_grid.pack(pady=5, padx=5)
        
        ttk.Button(btn_grid, text="▲", command=lambda: self._move(0, -0.5)).grid(row=0, column=1, pady=2)
        ttk.Button(btn_grid, text="◀", command=lambda: self._move(-0.5, 0)).grid(row=1, column=0, padx=2)
        ttk.Button(btn_grid, text="▶", command=lambda: self._move(0.5, 0)).grid(row=1, column=2, padx=2)
        ttk.Button(btn_grid, text="▼", command=lambda: self._move(0, 0.5)).grid(row=2, column=1, pady=2)
        
        ttk.Label(control_frame, text="(Можно управлять стрелками на клавиатуре)", 
                  font=("Arial", 8, "italic")).pack(pady=2)

        input_frame = ttk.Frame(control_frame)
        input_frame.pack(fill="x", pady=5, padx=5)
        
        ttk.Label(input_frame, text="Задать X (м):").grid(row=0, column=0, sticky="w")
        self.entry_x = ttk.Entry(input_frame, width=7)
        self.entry_x.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(input_frame, text="Задать Y (м):").grid(row=1, column=0, sticky="w")
        self.entry_y = ttk.Entry(input_frame, width=7)
        self.entry_y.grid(row=1, column=1, padx=5, pady=2)
        
        ttk.Button(input_frame, text="Переместить", command=self._on_teleport).grid(row=2, column=0, columnspan=2, pady=5)

        self.lbl_status = tk.Label(right_panel, textvariable=self.status_text, font=("Arial", 12, "bold"), 
                                   relief="groove", bd=2, width=57, height=2)
        self.lbl_status.pack(fill="x", pady=10)
        
        ttk.Label(right_panel, text="Журнал событий системы:").pack(anchor="w")
        self.txt_log = tk.Text(right_panel, width=35, height=12, font=("Courier", 9), state="disabled")
        self.txt_log.pack(fill="x", pady=5)

    def _move(self, dx: float, dy: float):
        try:
            old_status, _ = self.controller.check_safety()
            self.controller.move_robot(dx, dy)
            new_status, zone_name = self.controller.check_safety()
            
            if new_status != old_status and new_status != "SAFE":
                self._log_event(f"НАРУШЕНИЕ: Вход в {zone_name} [{new_status}]")
            elif new_status == "SAFE" and old_status != "SAFE":
                self._log_event("ОБЪЕКТ: Вернулся в безопасную зону")
                
            self._refresh_ui()
            
        except ValueError as err:
            messagebox.showwarning("Граница поля", str(err))

    def _on_key_press(self, event):
        if event.keysym == "Up":
            self._move(0, -0.2)
        elif event.keysym == "Down":
            self._move(0, 0.2)
        elif event.keysym == "Left":
            self._move(-0.2, 0)
        elif event.keysym == "Right":
            self._move(0.2, 0)

    def _on_teleport(self):
        try:
            x_val = float(self.entry_x.get())
            y_val = float(self.entry_y.get())
            
            self.controller.robot_x = x_val
            self.controller.robot_y = y_val
            
            self._log_event(f"ТЕЛЕПОРТ: X={x_val}, Y={y_val}")
            self._refresh_ui()
            
        except ValueError:
            messagebox.showerror("Ошибка ввода", "Введите корректные числа в пределах размеров поля (0...10)!")

    def _log_event(self, message: str):
        self.txt_log.config(state="normal")
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.txt_log.insert(tk.END, f"[{timestamp}] {message}\n")
        self.txt_log.see(tk.END)
        self.txt_log.config(state="disabled")

    def _refresh_ui(self):
        self.canvas.delete("all")
        
        for zone in self.controller.zones:
            x1, y1 = zone.x1 * self.SCALE, zone.y1 * self.SCALE
            x2, y2 = zone.x2 * self.SCALE, zone.y2 * self.SCALE
            
            status = zone.get_status()
            if status == "STOP":
                color, border = "#ffcccc", "red"
            elif status == "WARNING":
                color, border = "#fff2cc", "orange"
            else:
                color, border = "#e2efda", "green"
                
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=border, width=2)
            self.canvas.create_text(x1 + 10, y1 + 15, text=zone.name, anchor="w", font=("Arial", 9, "bold"))

        rx = self.controller.robot_x * self.SCALE
        ry = self.controller.robot_y * self.SCALE
        r_size = 8
        self.canvas.create_oval(rx - r_size, ry - r_size, rx + r_size, ry + r_size, fill="#0070c0", outline="black", width=2)
        self.canvas.create_line(rx - 12, ry, rx + 12, ry, fill="black")
        self.canvas.create_line(rx, ry - 12, rx, ry + 12, fill="black")

        self.status_text.set(str(self.controller))

        safety_status, _ = self.controller.check_safety()
        if safety_status == "STOP":
            self.lbl_status.config(bg="red", fg="white", text="АВАРИЯ: СТОП!")
        elif safety_status == "WARNING":
            self.lbl_status.config(bg="orange", fg="black", text="ПРЕДУПРЕЖДЕНИЕ!")
        else:
            self.lbl_status.config(bg="green", fg="white", text="ОБЪЕКТ В БЕЗОПАСНОСТИ")


# ==============================================================================
# 3. ТОЧКА ВХОДА В ПРОГРАММУ
# ==============================================================================
def main():
    controller = SafetyController(field_width=10.0, field_height=10.0)
    
    # Зоны безопасности по Варианту 15
    controller.add_zone(WarningZone("Зона Предупреждения А", x1=2.0, y1=2.0, x2=8.0, y2=8.0))
    controller.add_zone(StopZone("Критическая Зона Б", x1=4.0, y1=4.0, x2=6.0, y2=6.0))
    
    app = SafetyApp(controller)
    app.mainloop()


if __name__ == "__main__":
    main()

