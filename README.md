# blackjack-trainer

Terminal trainer for memorizing blackjack basic strategy (Dealer Stands Soft 17).

You reconstruct the strategy chart from memory, cell by cell, typing the action
for each hand. The grid redraws as you go so you watch the picture fill in; wrong
cells are flagged in yellow and re-drilled until the whole chart is clean.

<p align="center">
  <img src="docs/chart.png" alt="Blackjack strategy chart" width="420">
</p>

## Setup

```sh
uv sync
```

## Run

```sh
uv run blackjack-trainer map-trainer in-order     # cells top-left to bottom-right
uv run blackjack-trainer map-trainer random-row   # whole rows shuffled, cells left-to-right
uv run blackjack-trainer map-trainer random        # final boss: every cell shuffled
```

Keys: `h` Hit · `s` Stand · `d` Double · `p` Split · `q` quit

Needs a real terminal (single-keypress input) and a truecolor-capable emulator.

## Dev

```sh
uv run ruff check .
uv run ruff format .
```
