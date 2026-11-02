"""Set up and time a mock paper.

    python scripts/mock_exam.py 1      # sit mock 1 (Jan 2026)
    python scripts/mock_exam.py 2      # sit mock 2 (Sep 2025)
    python scripts/mock_exam.py --list

Copies the blank paper into mocks/attempts/<date>/ so the original stays
clean, drops the data files it needs alongside it, and prints the clock
times you need to keep to. mocks/attempts/ is gitignored, so your answers
stay on your own machine - the study-group repo holds the papers and the
drills, not anybody's attempts.
"""
import argparse
import shutil
import sys
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MOCKS = ROOT / "mocks"
ATTEMPTS = MOCKS / "attempts"

PAPERS = {
    1: {
        "file": "mock_01_jan2026.ipynb",
        "name": "January 2026",
        "images": ["flow_diagram.png", "table_example.png"],
        "data": ["nhs_waiting_lists.csv", "nhs_staffing_info.csv"],
        "data_dir": "exam_2026",
    },
    2: {
        "file": "mock_02_sep2025.ipynb",
        "name": "2 September 2025",
        "images": ["data_to_read.png"],
        "data": ["health_info.csv", "diet_info.csv", "epd_202310_statins.zip"],
        "data_dir": "exam_2025",
    },
    3: {
        "file": "mock_03_practice.ipynb",
        "name": "Practice paper (synthetic ED data)",
        "images": [],
        "data": ["ed_attendances.csv", "observations.csv", "labs.csv",
                 "outcomes.csv", "hospitals.csv"],
        "data_dir": "capstone",
    },
}

DURATION = timedelta(hours=3)
SUBMIT_GRACE = timedelta(minutes=20)


def list_papers():
    print("\n  Available mock papers:\n")
    for number, paper in PAPERS.items():
        exists = "" if (MOCKS / paper["file"]).exists() else "   (missing)"
        print(f"    {number}  {paper['name']}{exists}")
    print()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("number", nargs="?", type=int, help="which paper to sit")
    parser.add_argument("--list", action="store_true", help="list the papers")
    args = parser.parse_args()

    if args.list or args.number is None:
        list_papers()
        return

    paper = PAPERS.get(args.number)
    if paper is None:
        print(f"No paper {args.number}. Try --list.")
        sys.exit(1)

    source = MOCKS / paper["file"]
    if not source.exists():
        print(f"{source} is missing.")
        sys.exit(1)

    stamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    target = ATTEMPTS / f"mock{args.number:02d}_{stamp}"
    (target / "data").mkdir(parents=True, exist_ok=True)

    shutil.copy2(source, target / paper["file"])
    for image in paper["images"]:
        if (MOCKS / image).exists():
            shutil.copy2(MOCKS / image, target / image)
    for name in paper["data"]:
        source_data = ROOT / "data" / paper["data_dir"] / name
        if source_data.exists():
            shutil.copy2(source_data, target / "data" / name)

    start = datetime.now()
    print(f"""
  {paper['name']} - 3 hours, 12 questions, 100 marks

  Paper      {target / paper['file']}
  Data       {target / 'data'}

  Started    {start:%H:%M}
  Half way   {start + DURATION / 2:%H:%M}    (aim to be at question 6-7)
  One hour   {start + DURATION - timedelta(hours=1):%H:%M}    (start writing up)
  Pens down  {start + DURATION:%H:%M}
  Submit by  {start + DURATION + SUBMIT_GRACE:%H:%M}    (20 minutes' grace)

  Open it with:  make lab

  Exam conditions: no AI, no notes beyond the module materials, Stack
  Overflow and the Python docs. Mark each other's papers afterwards - the
  marks are in the comments and the written interpretation as much as the
  code, and that is the part you cannot grade with pytest.
""")


if __name__ == "__main__":
    main()
