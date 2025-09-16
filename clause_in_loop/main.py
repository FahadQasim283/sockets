# run_all_and_capture_outputs.py
# Runs all activities in sequence so you can capture outputs for your report.

from activity1_private import run as act1
from activity2_shared import run as act2
from activity3_first_private import run as act3
from activity4_lastprivate import run as act4
from activity5_reduction_dot import run as act5
from activity6_nowait import run as act6

def main():
    # Activities 1–4
    act1(n=8, max_workers=4)
    act2(n=8, max_workers=4)
    act3(vlen=20, n=4, max_workers=4)
    act4(n=8, max_workers=4)

    # Activity 5 with three schedules (like in the lab)
    act5(n=40, chunk=5, schedule="static",  max_workers=4)
    act5(n=40, chunk=5, schedule="dynamic", max_workers=4)
    act5(n=40, chunk=4, schedule="guided",  max_workers=4)

    # Activity 6
    act6(N=10, max_workers=4)

if __name__ == "__main__":
    main()
