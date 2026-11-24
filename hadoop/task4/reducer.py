#!/usr/bin/env python3
"""Reducer: ورودی بر اساس کلید مرتب است. خروجی (date \t count \t avg_distance)"""
import sys

current, count, total = None, 0, 0.0

def emit():
    print(f"{current}\t{count}\t{total / count:.3f}")

for line in sys.stdin:
    key, val = line.rstrip("\n").split("\t", 1)
    dist, c = val.split(",")
    if key != current:
        if current is not None:
            emit()
        current, count, total = key, 0, 0.0
    count += int(c)
    total += float(dist)

if current is not None:
    emit()
