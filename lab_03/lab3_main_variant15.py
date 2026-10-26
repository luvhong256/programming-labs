import sys
from lab3_mod_variant15 import extract_subsample, find_settling_time, build_summary_dict

def main():
    signal = [0.0, 0.4, 0.9, 1.25, 1.1, 0.98, 1.02, 1.0, 1.01]
    time_mesh = list(range(len(signal)))
    step = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    
    sub_signal = extract_subsample(signal, step=step)
    metrics = build_summary_dict(time_mesh, signal)
    
    print("=== АНАЛИЗ ПЕРЕХОДНОГО ПРОЦЕССА САУ ===")
    print(f"Заданный шаг прореживания (sys.argv): {step}")
    print(f"Исходный ряд сигналов: {signal}")
    print(f"Прореженный ряд (срез [::{step}]): {sub_signal}")
    print("\nПоказатели качества управления (Словарь):")
    print(f" - Максимальное значение: {metrics['max_value']}")
    print(f" - Максимальное перерегулирование: {metrics['overshoot_percent']} %")
    print(f" - Индекс времени установления: {metrics['settling_index']}")
    print(f" - Время установления: {metrics['settling_time']}")

if __name__ == '__main__':
    main()
