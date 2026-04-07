# HVLCS Dynamic Programming

## Student Information
- Name: Carson T Reis
- UFID: 18459067

## Overview
This project solves the Highest-Value Longest Common Subsequence (HVLCS) problem.

Given a set of character values, a string `A`, and a string `B`, the program computes:
1. the **maximum total value** of a common subsequence of `A` and `B`
2. **one optimal subsequence** that achieves that value

---

## Repository Structure

src/
  hvlcs.py
  benchmark.py

data/
  example.in
  example.out
  benchmarks/
    benchmark_01.in
    benchmark_02.in
    ...
    benchmark_10.in

results/
  benchmark_results.csv
  runtime_plot.png

## Build / Dependencies

No compilation is needed.

Requirements:
Python 3
matplotlib for the benchmark graph

Install matplotlib if needed:

pip install matplotlib

## How to Run

Run HVLCS solver

Using an input file:
python3 src/hvlcs.py data/example.in

Or with standard input:
python3 src/hvlcs.py < data/example.in


Run the benchmark script
This generates:

10 benchmark input files
results/benchmark_results.csv
results/runtime_plot.png
python3 src/benchmark.py

## Example Input and Output

Example input
File: data/example.in

3
a 2
b 4
c 5
aacb
caab

Expected Output:

File: data/example.out
9
cb

How to reproduce the example- Run:

python3 src/hvlcs.py data/example.in

## Assumptions
Input follows the format from the assignment, character values are integers.
If more than one optimal subsequence exists, program may output any one of them.

## Questions / Written Component

Question 1:

I made 10 benchmark input files where each string length is at least 25, then ran the 
benchmark script on all of them and graphed the runtimes. The CSV is within results/benchmark_results.csv 
and the graph is results/runtime_plot.png. It shows that when the strings got longer, the program generally took 
longer too, which is what is to be expected from a dynamic programming solution.

Question 2:

Let OPT(i, j) mean best total value we can still get starting from position i in A and position j in B. If either string is already finished then OPT(i, j) is equal to 0 because there's nothing left to match. If A[i] and B[j] are different, the only real choices are to skip the current character in A or skip the current character in B, so
OPT(i, j) = max(OPT(i+1, j), OPT(i, j+1)). If A[i] and B[j] match, then we get one extra option: take that character, add its value, and move forward in both strings, so OPT(i, j) = max(OPT(i+1, j), OPT(i, j+1), value(A[i]) + OPT(i+1, j+1))

This works due to the reason that at every step, any optimal answer has to start by making one of those valid choices. So if we check all the possible good moves and take the maximum, we get the correct recurrence.

Question 3:

The pseudocode:

OPT(i, j):
    if i is past end of A or j is past end of B:
        return 0

    answer = max(OPT(i+1, j), OPT(i, j+1))

    if A[i] == B[j]:
        answer = max(answer, value(A[i]) + OPT(i+1, j+1))

    return answer

There are |A|*|B| different (i, j) states so the runtime is O(|A||B|) since they're ran once.
