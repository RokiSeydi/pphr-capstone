"""Week 2 reference solutions - loops and simulation."""


def monitor_oxygen(rng, start=98, floor=90, step_choices=(-2, -1, 0, 1)):
    oxygen_level = start
    readings = []
    while True:
        readings.append(oxygen_level)
        if oxygen_level < floor:
            break
        oxygen_level += rng.choice(list(step_choices))
    return readings


def steps_until_desaturation(rng, start=98, floor=90):
    # One reading is recorded before any update, so updates = readings - 1.
    return len(monitor_oxygen(rng, start=start, floor=floor)) - 1


def running_fluid_balance(hourly_intake, hourly_output):
    if len(hourly_intake) != len(hourly_output):
        raise ValueError(
            f"intake has {len(hourly_intake)} hours but output has "
            f"{len(hourly_output)}"
        )
    balance = 0
    cumulative = []
    for intake, output in zip(hourly_intake, hourly_output):
        balance += intake - output
        cumulative.append(balance)
    return cumulative


def first_abnormal_hour(readings, low, high):
    for index, reading in enumerate(readings):
        if reading < low or reading > high:
            return index
    return None
