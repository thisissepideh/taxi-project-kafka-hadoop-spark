#!/usr/bin/env python3
"""Mapper: خروجی (pickup_date \t trip_distance,1)"""
import sys

for line in sys.stdin:
    f = line.strip().split(",")
    if len(f) < 10 or f[0] == "pickup_datetime":     # رد کردن هدر و خطوط ناقص
        continue
    try:
        dist = float(f[3])
    except ValueError:
        continue
    print(f"{f[9]}\t{dist},1")
