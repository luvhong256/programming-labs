def stepper_positioning(target_steps, start_speed=100.0):

    # текущая позиция сколько шагов  пройдено
    current_step = 0
    # текущая скорость шагов/сек
    current_speed = start_speed
    # суммарное время
    summ_time = 0.0

    # моделируем движение, пока не дойдем до цели
    while current_step < target_steps:
        # вычисляем остаток пути
        ostatok = target_steps - current_step

        # если остаток меньше 10 шагов — уменьшаем скорость в 2 раза 
        if ostatok < 10:
            current_speed = start_speed / 2.0

        # делаем один шаг за интервал времени dt = 1 / speed
        dt = 1.0 / current_speed
        summ_time += dt

        # увеличиваем пройденное количество шагов
        current_step += 1

    return summ_time, current_step

#тестовые запуски 
test_cases = [
    (5, 100.0),  # замедляет сразу со старта
    (9, 100.0),  # граница почти сразу
    (10, 100.0), # ровно граница
    (25, 100.0), # обычная ситуация когда цель далеко
]

for target, speed in test_cases:
    t, steps = stepper_positioning(target, speed)
    print(f"\nЦель: {target} шагов, начальная скорость: {speed} шаг/с")
    print(f"  - Пройдено шагов : {steps}")
    print(f"  - Суммарное время: {t:.4f} с")
    print(f"  - Средняя скорость: {steps / t:.2f} шаг/с")
