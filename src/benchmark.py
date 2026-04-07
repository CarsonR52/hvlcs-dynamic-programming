#!/usr/bin/env python3
from __future__ import annotations

import csv
import random
import statistics
import time
from pathlib import Path

import matplotlib.pyplot as plt

from hvlcs import go, parse

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "benchmarks"
RESULTS_DIR = ROOT / "results"

VALS = {
    "a": 2,
    "b": 4,
    "c": 5,
    "d": 3,
    "e": 7,
    "f": 1,
    "g": 6,
    "h": 2,
}

NS = [25, 50, 75, 100, 125, 150, 175, 200, 225, 250]
REPS = 20
SEED = 4533


def mk_raw(n: int, vals: dict[str, int], abc: list[str], rng: random.Random) -> str:
    a = "".join(rng.choices(abc, k=n))
    b = "".join(rng.choices(abc, k=n))

    lines = [str(len(vals))]

    for ch in sorted(vals):
        lines.append(f"{ch} {vals[ch]}")

    lines.append(a)
    lines.append(b)

    return "\n".join(lines) + "\n"


def dump(path: Path, raw: str) -> None:
    path.write_text(raw, encoding="utf-8")


def bench(raw: str, reps: int) -> tuple[float, float, float]:
    vals, a, b = parse(raw)
    hits: list[int] = []

    for _ in range(reps):
        t1 = time.perf_counter_ns()
        go(vals, a, b)
        t2 = time.perf_counter_ns()
        hits.append(t2 - t1)

    avg_ms = statistics.fmean(hits) / 1_000_000.0
    min_ms = min(hits) / 1_000_000.0
    max_ms = max(hits) / 1_000_000.0

    return avg_ms, min_ms, max_ms


def save_csv(rows: list[tuple[str, int, int, float, float, float]]) -> None:
    path = RESULTS_DIR / "benchmark_results.csv"

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "file",
                "len_A",
                "len_B",
                "avg_runtime_ms",
                "min_runtime_ms",
                "max_runtime_ms",
            ]
        )

        for row in rows:
            writer.writerow(row)


def draw(rows: list[tuple[str, int, int, float, float, float]]) -> None:
    xs: list[int] = []
    ys: list[float] = []

    for _, n_a, _, avg_ms, _, _ in rows:
        xs.append(n_a)
        ys.append(avg_ms)

    plt.figure(figsize=(8, 5))
    plt.plot(xs, ys, marker="o")
    plt.xlabel("String length (|A| = |B|)")
    plt.ylabel("Average runtime (ms)")
    plt.title("HVLCS runtime across 10 nontrivial inputs")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(RESULTS_DIR / "runtime_plot.png", dpi=200)
    plt.close()


def run() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    rng = random.Random(SEED)
    abc = sorted(VALS)
    rows: list[tuple[str, int, int, float, float, float]] = []

    for idx, n in enumerate(NS, start=1):
        raw = mk_raw(n, VALS, abc, rng)

        name = f"benchmark_{idx:02d}.in"
        dump(DATA_DIR / name, raw)

        avg_ms, min_ms, max_ms = bench(raw, REPS)
        rows.append((name, n, n, avg_ms, min_ms, max_ms))

    save_csv(rows)
    draw(rows)


def main() -> None:
    run()


if __name__ == "__main__":
    main()
