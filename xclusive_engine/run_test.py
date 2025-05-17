# run_test.py

import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from mlb.engine import get_today_mlb_picks

picks = get_today_mlb_picks()

print("\n✅ PICKS GENERATED:\n")
for pick in picks:
    print(pick)
