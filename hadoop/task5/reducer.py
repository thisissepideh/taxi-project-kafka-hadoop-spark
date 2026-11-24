#!/usr/bin/env python3
"""Reducer / Combiner: جمع تعداد برای هر بازه"""
import sys

current, count = None, 0
for line in sys.stdin:
    key, val = line.rstrip("\n").split("\t")
    if key != current:
        if current is not None:
            print(f"{current}\t{count}")
        current, count = key, 0
    count += int(val)
if current is not None:
    print(f"{current}\t{count}")
