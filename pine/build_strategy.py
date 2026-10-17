#!/usr/bin/env python3
"""Build pine/6-tap-strategy.pine from the indicator so both run the same engine.

The strategy = strategy/head.pine (with the indicator's SHARED INPUTS block pasted in)
             + the indicator's ENGINE block, verbatim
             + strategy/tail.pine (orders and the R table).
Run after every change to pine/6-tap.pine or pine/strategy/*.pine:  python3 pine/build_strategy.py
"""
from pathlib import Path

here = Path(__file__).resolve().parent
ind = (here / "6-tap.pine").read_text()


def block(text, begin, end):
    i = text.index(begin)
    j = text.index(end, i)
    j = text.index("\n", j) + 1
    return text[i:j]


shared = block(ind, "// ==== SHARED INPUTS BEGIN ====", "// ==== SHARED INPUTS END ====")
engine = block(ind, "// ==== ENGINE BEGIN ====", "// ==== ENGINE END ====")
head = (here / "strategy" / "head.pine").read_text()
tail = (here / "strategy" / "tail.pine").read_text()
assert "//@@SHARED_INPUTS@@" in head
out = head.replace("//@@SHARED_INPUTS@@", shared.rstrip("\n")) + "\n" + engine + tail
(here / "6-tap-strategy.pine").write_text(out)
print(f"wrote 6-tap-strategy.pine ({out.count(chr(10))} lines)")
