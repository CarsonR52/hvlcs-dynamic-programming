#!/usr/bin/env python3
"""Compute highest-value common subsequence (HVLCS)"""

from __future__ import annotations

import sys
from pathlib import Path


def parse(raw: str) -> tuple[dict[str, int], str, str]:
    # REMEMBER: ignore blank lines so pasted test cases still work
    bits = []

    for line in raw.splitlines():
        line = line.strip()
        if line:
            bits.append(line)

    if len(bits) < 4:
        raise ValueError("input is too short")

    try:
        k = int(bits[0])
    except ValueError as exc:
        raise ValueError("first line must be an integer K") from exc

    if len(bits) < k + 3:
        raise ValueError("missing value lines or strings A and B")

    vals: dict[str, int] = {}

    for i in range(1, k + 1):
        row = bits[i].split()

        if len(row) != 2:
            raise ValueError(f"bad value line at line {i + 1}")

        ch = row[0]
        num = row[1]

        if len(ch) != 1:
            raise ValueError(f"symbol '{ch}' must be one character")

        try:
            vals[ch] = int(num)
        except ValueError as exc:
            raise ValueError(f"bad value for symbol '{ch}'") from exc

    a = bits[k + 1]
    b = bits[k + 2]

    return vals, a, b


def go(vals: dict[str, int], a: str, b: str) -> tuple[int, str, dict[tuple[int, int], int]]:
    n = len(a)
    m = len(b)
    # memoized recursion for best score from (i, j)
    mem: dict[tuple[int, int], int] = {}

    sys.setrecursionlimit(max(1000, n + m + 50))

    def best(i: int, j: int) -> int:
        key = (i, j)

        if key in mem:
            return mem[key]

        if i == n or j == m:
            mem[key] = 0
            return 0

        ans1 = best(i + 1, j)

        ans2 = best(i, j + 1)

        ans = ans1
        if ans2 > ans:
            ans = ans2

        # try taking both if match
        if a[i] == b[j]:
            take = vals.get(a[i], 0) + best(i + 1, j + 1)
            if take > ans:
                ans = take

        mem[key] = ans
        return ans

    def build(i: int, j: int) -> str:

        out: list[str] = []

        # should prefer taking matching character whenever it keeps
        # optimal score. otherwise, break ties by advancing in "a" first
        while i < n and j < m:
            now = best(i, j)

            if a[i] == b[j]:
                take = vals.get(a[i], 0) + best(i + 1, j + 1)

                if take == now:
                    out.append(a[i])
                    i += 1
                    j += 1
                    continue

            down = best(i + 1, j)
            right = best(i, j + 1)

            if down == now:
                i += 1
            else:
                j += 1

        return "".join(out)

    score = best(0, 0)
    out = build(0, 0)

    return score, out, mem


def solve(raw: str) -> str:
    vals, a, b = parse(raw)
    score, out, _ = go(vals, a, b)
    return f"{score}\n{out}\n"


def main() -> None:
    if len(sys.argv) > 2:
        print("Usage: python3 src/hvlcs.py [input_file]", file=sys.stderr)
        sys.exit(1)

    if len(sys.argv) == 2:
        raw = Path(sys.argv[1]).read_text(encoding="utf-8")
    else:
        raw = sys.stdin.read()

    try:
        sys.stdout.write(solve(raw))
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
