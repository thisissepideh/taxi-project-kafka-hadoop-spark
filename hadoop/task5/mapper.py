#!/usr/bin/env python3
"""Mapper: بازه ۵ دقیقه‌ای مدت سفر → (bucket \t 1)"""
import sys

for line in sys.stdin:
    f = line.strip().split(",")
    if len(f) < 10 or f[0] == "pickup_datetime":
        continue
    try:
        dur = float(f[8])
    except ValueError:
        continue
    lo = int(dur // 5) * 5
    print(f"{lo:03d}-{lo + 5:03d}\t1")
