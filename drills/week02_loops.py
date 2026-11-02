"""Week 2 - while loops, for loops and simulation.

Exam archetype: Q2 (5 marks) - simulate ICU oxygen saturation with a while
loop that stops when the reading crosses a threshold.

Every function takes an `rng` (a random.Random instance) instead of calling
`random` directly. That keeps results reproducible, which is what makes the
behaviour testable - a good habit the markers reward.
"""


def monitor_oxygen(rng, start=98, floor=90, step_choices=(-2, -1, 0, 1)):
    """Simulate oxygen saturation until it drops below `floor`.

    Algorithm:
        1. Begin at `start`.
        2. Record the current level.
        3. Change the level by one value drawn from `step_choices`
           (use rng.choice).
        4. Stop as soon as the level is below `floor`, recording that
           final level too.

    :param rng: random.Random instance, for reproducibility
    :param start: starting oxygen level
    :param floor: stop once the level falls below this
    :param step_choices: possible per-step changes
    :return: list of every level recorded, first to last. The last element
             is the first value below `floor`; all earlier ones are >= floor.
    """
    raise NotImplementedError


def steps_until_desaturation(rng, start=98, floor=90):
    """Return how many updates it took to fall below `floor`.

    Reuse monitor_oxygen rather than rewriting the loop.

    :param rng: random.Random instance
    :param start: starting oxygen level
    :param floor: threshold
    :return: int number of updates applied
    """
    raise NotImplementedError


def running_fluid_balance(hourly_intake, hourly_output):
    """Return the cumulative fluid balance after each hour.

    Balance for an hour is intake minus output; the result accumulates.

    Example:
        running_fluid_balance([100, 120], [80, 150]) -> [20, -10]

    :param hourly_intake: list of millilitres in
    :param hourly_output: list of millilitres out (same length)
    :return: list of cumulative balances, one per hour
    :raises ValueError: if the two lists are different lengths
    """
    raise NotImplementedError


def first_abnormal_hour(readings, low, high):
    """Return the index of the first reading outside [low, high].

    Use a loop with an early exit rather than scanning the whole list.

    :param readings: list of numeric observations
    :param low: lower bound of the normal range (inclusive)
    :param high: upper bound of the normal range (inclusive)
    :return: index of the first out-of-range reading, or None if all normal
    """
    raise NotImplementedError
