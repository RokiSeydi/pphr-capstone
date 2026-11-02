"""Generate the synthetic capstone dataset.

    python scripts/make_capstone_data.py [--seed 42] [--n 2000]

Everything here is simulated from a seeded generator. No real patient data
is involved and none of these attendances describe a real person. The
generating process is deliberately visible: the outcome really is driven by
NEWS2, lactate and age, so when your logistic regression recovers those
associations you know your modelling code is right. That is the point of
practising on synthetic data - you can check your answer.

The clinical domain is deliberately different from both past papers, which
use NHS waiting lists, staffing, and diet/blood-pressure data. Here it is
suspected sepsis in the emergency department.
"""
import argparse
import random
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "capstone"

HOSPITALS = [
    ("H01", "St Alban's University Hospital", "London", 820),
    ("H02", "Riverside General Hospital", "North West", 1140),
    ("H03", "Kingsmead Hospital", "South East", 460),
    ("H04", "Fenwick Royal Infirmary", "Yorkshire", 980),
    ("H05", "Ardenmoor Community Hospital", "South West", 230),
    ("H06", "Northgate University Hospital", "North East", 710),
]

TRIAGE = ["Immediate", "Very urgent", "Urgent", "Standard", "Non-urgent"]
TRIAGE_WEIGHTS = [0.04, 0.16, 0.34, 0.34, 0.12]

# Free-text presenting complaints, for the regex week. Some record vitals or
# a symptom duration inline, some are vague, some contain negations.
COMPLAINT_TEMPLATES = [
    "Fever and rigors for {days} days, temp {temp} on arrival.",
    "Productive cough {days} days, SpO2 {spo2}% in triage.",
    "Query urosepsis. Dysuria for {days} days. BP {sys}/{dia}.",
    "Unwell for {days} days, no fever reported. HR {hr}.",
    "Confusion and reduced oral intake over {days} days.",
    "Abdominal pain {days} days with vomiting, temp {temp}.",
    "Cellulitis left leg, spreading over {days} days.",
    "Shortness of breath, worsening {days} days, SpO2 {spo2}%.",
    "Collapse at home. No preceding symptoms.",
    "Post-operative wound discharge, {days} days post procedure.",
    "Sore throat and myalgia {days} days. Denies breathlessness.",
    "Indwelling catheter, cloudy urine for {days} days, temp {temp}.",
]


def news2_resp(rate):
    if rate <= 8:
        return 3
    if rate <= 11:
        return 1
    if rate <= 20:
        return 0
    if rate <= 24:
        return 2
    return 3


def news2_spo2(spo2):
    if spo2 <= 91:
        return 3
    if spo2 <= 93:
        return 2
    if spo2 <= 95:
        return 1
    return 0


def news2_temp(temp):
    if temp <= 35.0:
        return 3
    if temp <= 36.0:
        return 1
    if temp <= 38.0:
        return 0
    if temp <= 39.0:
        return 1
    return 2


def news2_systolic(sys_bp):
    if sys_bp <= 90:
        return 3
    if sys_bp <= 100:
        return 2
    if sys_bp <= 110:
        return 1
    if sys_bp <= 219:
        return 0
    return 3


def news2_pulse(hr):
    if hr <= 40:
        return 3
    if hr <= 50:
        return 1
    if hr <= 90:
        return 0
    if hr <= 110:
        return 1
    if hr <= 130:
        return 2
    return 3


def news2_total(resp, spo2, temp, sys_bp, hr, consciousness):
    total = (
        news2_resp(resp)
        + news2_spo2(spo2)
        + news2_temp(temp)
        + news2_systolic(sys_bp)
        + news2_pulse(hr)
    )
    if consciousness != "Alert":
        total += 3
    return total


def main(seed, n):
    rng = random.Random(seed)
    OUT.mkdir(parents=True, exist_ok=True)

    start = datetime(2026, 1, 1, 0, 0)

    attendances, observations, labs, outcomes = [], [], [], []

    for i in range(1, n + 1):
        att_id = f"A{i:05d}"
        pat_id = f"P{rng.randint(1, int(n * 0.92)):05d}"  # some reattenders
        hosp = rng.choice(HOSPITALS)[0]
        arrival = start + timedelta(
            minutes=rng.randint(0, 365 * 24 * 60), seconds=rng.randint(0, 59)
        )
        age = min(101, max(16, int(rng.gauss(64, 19))))
        sex = rng.choice(["Female", "Male"])
        triage = rng.choices(TRIAGE, weights=TRIAGE_WEIGHTS, k=1)[0]

        # Sicker patients get triaged higher, so vitals depend on triage.
        severity = {
            "Immediate": 3.0, "Very urgent": 2.1, "Urgent": 1.2,
            "Standard": 0.5, "Non-urgent": 0.1,
        }[triage] + rng.gauss(0, 0.6)

        resp = max(6, min(44, int(rng.gauss(17 + 3.1 * severity, 3))))
        spo2 = max(78, min(100, int(rng.gauss(97 - 2.3 * severity, 2))))
        temp = round(max(34.0, min(41.5, rng.gauss(37.1 + 0.55 * severity, 0.8))), 1)
        sys_bp = max(62, min(210, int(rng.gauss(132 - 9.5 * severity, 17))))
        dia_bp = max(35, min(120, int(sys_bp * rng.uniform(0.55, 0.70))))
        hr = max(38, min(180, int(rng.gauss(84 + 9.0 * severity, 14))))
        consciousness = "Alert" if rng.random() > 0.035 + 0.05 * max(severity, 0) else \
            rng.choice(["Confusion", "Voice", "Pain"])

        news2 = news2_total(resp, spo2, temp, sys_bp, hr, consciousness)

        lactate = round(max(0.4, rng.gauss(1.4 + 0.30 * severity, 1.0)), 1)
        wcc = round(max(0.6, rng.gauss(10.5 + 1.9 * severity, 4.2)), 1)
        crp = max(1, int(rng.gauss(55 + 32 * severity, 45)))
        creatinine = max(30, int(rng.gauss(88 + 14 * severity, 34)))

        # Missingness is not random: labs are skipped more often for the
        # patients triaged as least unwell. Worth noticing in the analysis.
        if rng.random() < 0.16 - 0.03 * severity:
            lactate = ""
        if rng.random() < 0.06:
            crp = ""

        # --- the true data-generating process for the outcome ---------------
        logit = (
            -4.0
            + 0.185 * news2
            + 0.44 * (lactate if lactate != "" else 1.5)
            + 0.021 * (age - 64)
            + (0.30 if consciousness != "Alert" else 0.0)
        )
        p_icu = 1 / (1 + pow(2.718281828459045, -logit))
        icu = 1 if rng.random() < p_icu else 0

        mins_to_abx = int(max(8, rng.gauss(74 - 13 * severity, 38)))
        got_abx = rng.random() < 0.52 + 0.14 * severity
        abx_time = (arrival + timedelta(minutes=mins_to_abx)) if got_abx else None

        los = round(max(0.1, rng.gauss(4.2 + 2.6 * severity + 5.0 * icu, 3.1)), 1)
        died = 1 if rng.random() < (0.012 + 0.009 * news2 + 0.10 * icu) else 0

        tmpl = rng.choice(COMPLAINT_TEMPLATES)
        complaint = tmpl.format(
            days=rng.randint(1, 12), temp=temp, spo2=spo2,
            sys=sys_bp, dia=dia_bp, hr=hr,
        )

        attendances.append([
            att_id, pat_id, hosp, arrival.strftime("%Y-%m-%d %H:%M:%S"),
            age, sex, triage, complaint,
        ])
        observations.append([
            att_id, resp, spo2, temp, sys_bp, dia_bp, hr, consciousness,
        ])
        labs.append([att_id, lactate, wcc, crp, creatinine])
        outcomes.append([
            att_id,
            abx_time.strftime("%Y-%m-%d %H:%M:%S") if abx_time else "",
            icu, los, died,
        ])

    def write(path, header, rows):
        import csv
        with open(path, "w", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(header)
            w.writerows(rows)
        print(f"  {path.name}: {len(rows)} rows")

    print(f"Writing synthetic capstone data (seed={seed}, n={n}) to {OUT}")
    write(OUT / "hospitals.csv",
          ["hospital_id", "hospital_name", "region", "beds"], HOSPITALS)
    write(OUT / "ed_attendances.csv",
          ["attendance_id", "patient_id", "hospital_id", "arrival_datetime",
           "age", "sex", "triage_category", "presenting_complaint"], attendances)
    write(OUT / "observations.csv",
          ["attendance_id", "respiratory_rate", "spo2", "temperature",
           "systolic_bp", "diastolic_bp", "heart_rate", "consciousness"],
          observations)
    write(OUT / "labs.csv",
          ["attendance_id", "lactate", "white_cell_count", "crp", "creatinine"],
          labs)
    write(OUT / "outcomes.csv",
          ["attendance_id", "antibiotics_datetime", "icu_admission",
           "length_of_stay_days", "died_in_hospital"], outcomes)
    print("Done. These files are synthetic teaching data, not real records.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--n", type=int, default=2000)
    a = ap.parse_args()
    main(a.seed, a.n)
