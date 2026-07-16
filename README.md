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

## map-trainer

Reconstruct the strategy chart from memory, cell by cell. The grid redraws as you
go so you watch the picture fill in; wrong cells are flagged and re-drilled until
the whole chart is clean.

```sh
uv run blackjack-trainer map-trainer in-order     # cells top-left to bottom-right
uv run blackjack-trainer map-trainer random-row   # whole rows shuffled, cells left-to-right
uv run blackjack-trainer map-trainer random        # final boss: every cell shuffled
```

Keys: `h` Hit · `s` Stand · `d` Double · `p` Split · `q` quit

## Dev

```sh
uv run ruff check .
uv run ruff format .
```
