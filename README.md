# blackjack-trainer

Terminal trainers for memorizing blackjack basic strategy (Dealer Stands Soft 17).

## Setup

```sh
uv sync
```

## Run

```sh
uv run blackjack-trainer
```

## Coloring trainer

Reconstruct the strategy chart from memory, cell by cell. The grid redraws as you
go so you watch the picture fill in; wrong cells are revealed and re-drilled until
the whole chart is clean.

Keys: `h` Hit · `s` Stand · `d` Double · `p` Split · `q` quit

## Dev

```sh
uv run ruff check .
uv run ruff format .
```
