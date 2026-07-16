#!/usr/bin/env python3
"""Blackjack basic-strategy COLORING trainer (Dealer Stands Soft 17).

You reconstruct the strategy chart from memory, cell by cell, by typing the
action for each cell. The grid redraws as you go so you watch the picture fill
in. Wrong answers are revealed and re-drilled until the whole chart is clean.

Keys:  h = Hit (green)   s = Stand (red)   d = Double (blue)   p = Split (orange)
       q or Ctrl-C = quit
"""

import sys
import termios
import tty

# --- Strategy table: Dealer Stands on Soft 17 -------------------------------
# Columns are dealer upcard: 2 3 4 5 6 7 8 9 10 A
COLS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "A"]

# (section, row-label, 10 actions for cols 2..A)
ROWS = [
    ("HARD", "17+", "SSSSSSSSSS"),
    ("HARD", "16", "SSSSSHHHHH"),
    ("HARD", "15", "SSSSSHHHHH"),
    ("HARD", "14", "SSSSSHHHHH"),
    ("HARD", "13", "SSSSSHHHHH"),
    ("HARD", "12", "HHSSSHHHHH"),
    ("HARD", "11", "DDDDDDDDDD"),
    ("HARD", "10", "DDDDDDDDHH"),
    ("HARD", "9", "HDDDDHHHHH"),
    ("HARD", "8", "HHHHHHHHHH"),
    ("SOFT", "A,9", "SSSSSSSSSS"),
    ("SOFT", "A,8", "SSSSDSSSSS"),
    ("SOFT", "A,7", "DDDDDSSHHH"),
    ("SOFT", "A,6", "HDDDDHHHHH"),
    ("SOFT", "A,5", "HHDDDHHHHH"),
    ("SOFT", "A,4", "HHDDDHHHHH"),
    ("SOFT", "A,3", "HHHDDHHHHH"),
    ("SOFT", "A,2", "HHHDDHHHHH"),
    ("PAIR", "AA", "PPPPPPPPPP"),
    ("PAIR", "TT", "SSSSSSSSSS"),
    ("PAIR", "99", "PPPPPSPPSS"),
    ("PAIR", "88", "PPPPPPPPPP"),
    ("PAIR", "77", "PPPPPPHHHH"),
    ("PAIR", "66", "PPPPPHHHHH"),
    ("PAIR", "55", "DDDDDDDDHH"),
    ("PAIR", "44", "HHHPPHHHHH"),
    ("PAIR", "33", "PPPPPPHHHH"),
    ("PAIR", "22", "PPPPPPHHHH"),
]

# --- Colors (truecolor, black text on chart-matching backgrounds) ------------
FG_BLACK = "38;2;0;0;0"
BG = {
    "H": "48;2;46;204;113",  # green
    "S": "48;2;231;76;60",  # red
    "D": "48;2;52;152;219",  # blue
    "P": "48;2;243;156;18",  # orange
}
RESET = "\033[0m"
DIM = "\033[2m"
BOLD = "\033[1m"


def cell(action, *, current=False, miss=False):
    """Render one 4-char-wide cell."""
    if action == " ":  # empty
        inner = " ?? " if current else " ·  "
        style = "\033[7m" if current else DIM
        return f"{style}{inner}{RESET}"
    letter = action.lower() if miss else action
    mark = "\033[4m" if miss else ""  # underline flags a corrected miss
    return f"\033[{FG_BLACK};{BG[action]}m{mark} {letter}  {RESET}"


def clear():
    sys.stdout.write("\033[2J\033[H")


def draw(answers, cur_idx, misses):
    """answers: list[str] parallel to flattened cells, ' ' if unfilled."""
    clear()
    out = []
    out.append(f"{BOLD}Blackjack Strategy — Coloring Trainer  (Dealer Stands Soft 17){RESET}")
    out.append(
        f"  {BG['H'] and ''}"
        f"\033[{FG_BLACK};{BG['H']}m h {RESET} Hit   "
        f"\033[{FG_BLACK};{BG['S']}m s {RESET} Stand   "
        f"\033[{FG_BLACK};{BG['D']}m d {RESET} Double   "
        f"\033[{FG_BLACK};{BG['P']}m p {RESET} Split      {DIM}q=quit{RESET}"
    )
    out.append("")
    # column header — align each label to the letter position inside its 4-char cell
    header = "      " + "".join(f" {c:<3}" for c in COLS)
    out.append(f"{BOLD}{header}{RESET}   {DIM}dealer{RESET}")

    prev_section = None
    for r, (section, label, _correct) in enumerate(ROWS):
        if section != prev_section and prev_section is not None:
            out.append("")  # white-gap separator between sections
        prev_section = section
        line = f"{BOLD}{label:>5}{RESET} "
        for c in range(10):
            idx = r * 10 + c
            line += cell(
                answers[idx],
                current=(idx == cur_idx),
                miss=(idx in misses and answers[idx] != " "),
            )
        # section tag on the first row of each block
        tag = ""
        if r == 0 or ROWS[r - 1][0] != section:
            tag = f"  {DIM}{section}{RESET}"
        out.append(line + tag)

    out.append("")
    sys.stdout.write("\n".join(out) + "\n")
    sys.stdout.flush()


def getch():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
    return ch


def run():
    flat_correct = [a for (_s, _l, row) in ROWS for a in row]
    total = len(flat_correct)
    answers = [" "] * total
    misses = set()  # cells answered wrong at least once
    order = list(range(total))
    status = "Fill every cell. Type h / s / d / p."

    key_to_action = {"h": "H", "s": "S", "d": "D", "p": "P"}

    def drill(indices):
        nonlocal status
        i = 0
        while i < len(indices):
            idx = indices[i]
            draw(answers, idx, misses)
            r, c = divmod(idx, 10)
            sys.stdout.write(f"  {ROWS[r][1]} vs {COLS[c]}   {status}\n")
            sys.stdout.flush()
            ch = getch().lower()
            if ch in ("q", "\x03"):
                return False
            if ch not in key_to_action:
                status = "keys: h s d p"
                continue
            guess = key_to_action[ch]
            correct = flat_correct[idx]
            answers[idx] = correct  # always show the correct color in the picture
            if guess == correct:
                status = "✓"
            else:
                misses.add(idx)
                names = {"H": "HIT", "S": "STAND", "D": "DOUBLE", "P": "SPLIT"}
                status = f"✗ you said {names[guess]} — it's {names[correct]}"
            i += 1
        return True

    # First full pass
    if not drill(order):
        clear()
        print("Bailed. Later.")
        return

    # Re-drill misses until clean
    while misses:
        redo = sorted(misses)
        # reset those cells to blank so you truly re-enter them
        for idx in redo:
            answers[idx] = " "
        misses.clear()
        status = f"Re-drill: {len(redo)} missed cell(s)."
        if not drill(redo):
            break
        # any still wrong got re-added to misses; loop again

    clear()
    draw(answers, -1, set())
    print(f"  {BOLD}Chart complete and clean.{RESET}  ({total} cells)")
    print(f"  {DIM}Run again to re-test from a blank grid.{RESET}")


def main():
    try:
        run()
    except KeyboardInterrupt:
        sys.stdout.write(RESET + "\n")


if __name__ == "__main__":
    main()
