#!/usr/bin/env python3
import os
import re

with open("input-1") as f:
    m = re.findall(r"\d+", f.read(), re.MULTILINE)
    print(len(m))

with open("input-1") as f:
    lines = [l.strip() for l in f.readlines()]
