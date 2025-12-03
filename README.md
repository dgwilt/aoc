# Advent of Code

Collection of my Advent of Code solutions spanning 2016–2025.
Each year lives in its own directory and contains the Python scripts I wrote
while solving that event’s daily puzzles. Where helpful, solutions share a
lightweight `AocDay` framework that keeps input parsing and mode selection
consistent across the repository.

## Repository layout
- `<year>/day_XX.py`: the solver for day XX. Most files bundle the puzzle input,
  optional example tests (`silver_tests`, `gold_tests`), and a small driver
  invoking `AocDay`.
- `<year>/aoc.py`: shared helpers for that year’s solutions, including the
  `AocDay` base class with utilities for grids, neighbors, parsing, etc.
- Gifts like `starter.py` or `day_xx.py` inside a year are personal experiments,
  helpers, or early drafts from that year’s solving process.

## Running a solution
1. Make sure you have Python 3.8+ available (`/usr/bin/env python3` is used in
   most shebangs).
2. Run a day script with an optional mode argument:
   ```bash
   python3 2024/day_01.py   # runs the default “st” mode (silver tests)
   python3 2024/day_01.py s # runs the silver solution on the embedded puzzle data
   python3 2024/day_01.py g # runs the gold solution on the embedded puzzle data
   ```
   The supported modes (`AocDay.MODES`) are `st`, `s`, `gt`, `g`, and `gst`.
   `st`/`gt` print the corresponding tests, `s`/`g` run the real inputs, and
   `gst` reruns the gold logic against the silver tests.
3. Any additional example inputs or helper scripts needed by a day are defined
   at the bottom of the module; edit the block guarded by `if __name__ == "__main__"`
   if you want to swap in different data.

## Adding a new solution
1. Create a new `day_XX.py` file inside the appropriate year directory.
2. Implement `run_silver`/`run_gold` on a subclass of `AocDay`.
3. Populate `silver_tests`, `gold_tests`, and `data` as shown in the existing
   days, then print the instance to exercise the chosen mode.
4. Follow the existing pattern of keeping parsing helpers on the shared `aoc.py`
   rather than recreating them per day.

## Notes
- This repo keeps the finished puzzle inputs inside each sitter; there’s no
  centralized `input/` directory.
- Every year directory may contain unused helper scripts, so lean on the
  directories themselves to discover how the solutions evolved over time.
