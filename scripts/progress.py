"""Show how far through the drills you are.

    python scripts/progress.py

Runs each week's tests and reports a line per week. A drill that still
raises NotImplementedError counts as "not started" rather than "wrong", so
the table distinguishes what you have not reached from what you got wrong.
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

TITLES = {
    1: "Lists, dicts and indexing",
    2: "Loops and simulation",
    3: "Clinical decision logic",
    4: "Strings, f-strings and dates",
    5: "Functions, docstrings and errors",
    6: "Regex on clinical free text",
    7: "Classes and inheritance",
    8: "Selecting from a DataFrame",
    9: "Reading files and sorting",
    10: "Grouping and aggregation",
    11: "Merging and cross-tabulating",
    12: "Matplotlib figures",
    13: "Features and logistic regression",
}

BAR_WIDTH = 18


def run_week(number):
    """Run one week's tests, returning (passed, failed, not_started).

    Note: pytest.ini already sets -q, so this must not pass -q again.
    Two -q flags suppress the summary line this function parses.
    """
    path = ROOT / "tests" / f"test_week{number:02d}.py"
    if not path.exists():
        return None
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", str(path), "--tb=no", "-rN",
         "-p", "no:cacheprovider"],
        cwd=ROOT, capture_output=True, text=True,
    )
    output = proc.stdout + proc.stderr

    def count(label):
        match = re.search(rf"(\d+) {label}", output)
        return int(match.group(1)) if match else 0

    passed = count("passed")
    failed = count("failed") + count("error")
    not_started = output.count("NotImplementedError")
    return passed, failed, not_started


def bar(passed, total):
    if total == 0:
        return " " * BAR_WIDTH
    filled = round(BAR_WIDTH * passed / total)
    return "#" * filled + "." * (BAR_WIDTH - filled)


def main():
    print()
    print(f"  {'Week':<5} {'Topic':<34} {'Progress':<{BAR_WIDTH + 2}} Passing")
    print("  " + "-" * 72)

    total_passed = total_tests = 0
    for number in sorted(TITLES):
        result = run_week(number)
        if result is None:
            continue
        passed, failed, _ = result
        total = passed + failed
        total_passed += passed
        total_tests += total
        state = "done" if failed == 0 and total else f"{failed} to fix"
        print(
            f"  {number:<5} {TITLES[number]:<34} [{bar(passed, total)}] "
            f"{passed:>3}/{total:<4} {state}"
        )

    print("  " + "-" * 72)
    pct = 100 * total_passed / total_tests if total_tests else 0
    print(f"  {'':<5} {'Overall':<34} [{bar(total_passed, total_tests)}] "
          f"{total_passed:>3}/{total_tests:<4} {pct:.0f}%")
    print()


if __name__ == "__main__":
    main()
