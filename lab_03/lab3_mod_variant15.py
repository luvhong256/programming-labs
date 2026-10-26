def extract_subsample(time_series, step=2):
    return time_series[::step]

def find_settling_time(time_series, target_val=1.0, tol=0.05):
    lower_bound = target_val * (1 - tol)
    upper_bound = target_val * (1 + tol)
    settling_idx = -1
    for i in range(len(time_series) - 1, -1, -1):
        if not (lower_bound <= time_series[i] <= upper_bound):
            settling_idx = i + 1
            break
    if settling_idx == -1:
        settling_idx = 0
    if settling_idx >= len(time_series):
        return -1
    return settling_idx

def build_summary_dict(time_list, signal_list):
    max_val = max(signal_list)
    target_val = 1.0
    overshoot = max(0.0, (max_val - target_val) / target_val * 100)
    settling_idx = find_settling_time(signal_list, target_val=target_val)
    settling_time = time_list[settling_idx] if settling_idx != -1 else "Не установлено"
    return {
        'max_value': round(max_val, 3),
        'overshoot_percent': round(overshoot, 2),
        'settling_index': settling_idx,
        'settling_time': settling_time
    }

