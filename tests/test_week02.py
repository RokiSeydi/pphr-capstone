"""Week 2 - loops and simulation."""
import random

import pytest

from tests._target import mod

w = mod("week02_loops")


def test_monitor_oxygen_starts_at_start():
    assert w.monitor_oxygen(random.Random(0))[0] == 98


def test_monitor_oxygen_ends_below_floor():
    readings = w.monitor_oxygen(random.Random(1), start=98, floor=90)
    assert readings[-1] < 90
    assert all(reading >= 90 for reading in readings[:-1])


def test_monitor_oxygen_is_reproducible():
    assert w.monitor_oxygen(random.Random(7)) == w.monitor_oxygen(random.Random(7))


def test_monitor_oxygen_differs_across_seeds():
    runs = {tuple(w.monitor_oxygen(random.Random(s))) for s in range(12)}
    assert len(runs) > 1, "the simulation should depend on the rng"


def test_monitor_oxygen_respects_custom_bounds():
    readings = w.monitor_oxygen(random.Random(3), start=100, floor=95)
    assert readings[0] == 100
    assert readings[-1] < 95


def test_monitor_oxygen_steps_are_from_choices():
    readings = w.monitor_oxygen(random.Random(5))
    steps = {b - a for a, b in zip(readings, readings[1:])}
    assert steps <= {-2, -1, 0, 1}


def test_steps_until_desaturation_matches_readings():
    seed = 11
    expected = len(w.monitor_oxygen(random.Random(seed))) - 1
    assert w.steps_until_desaturation(random.Random(seed)) == expected


def test_running_fluid_balance():
    assert w.running_fluid_balance([100, 120], [80, 150]) == [20, -10]


def test_running_fluid_balance_accumulates():
    assert w.running_fluid_balance([50, 50, 50], [0, 0, 0]) == [50, 100, 150]


def test_running_fluid_balance_length_mismatch():
    with pytest.raises(ValueError):
        w.running_fluid_balance([1, 2, 3], [1, 2])


def test_first_abnormal_hour():
    assert w.first_abnormal_hour([98, 97, 88, 99], 90, 100) == 2
    assert w.first_abnormal_hour([120, 98], 90, 100) == 0


def test_first_abnormal_hour_all_normal():
    assert w.first_abnormal_hour([95, 96, 97], 90, 100) is None
