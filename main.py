#!/usr/bin/env python3
"""Write the Angry Judge short-rant entry to $MAKEFUN_OUTPUT_DIR/entry.txt.

The bounty ("Angry Judge: The Short Rant Contest") gates the entry at
1 to 400 characters of UTF-8 text, not only whitespace. The rant below is
a furious competition judge letting rip about the terrible entries he has
to read every day. The program checks the gate itself before writing and
reads the file back afterwards, so a bad edit fails loudly here instead
of at the grader.
"""

import os
import sys

RANT = (
    "I have read ten thousand of your 'rants.' Ten thousand! Half are "
    "'Mondays, am I right?' — groundbreaking, truly, nobody has ever "
    "disliked a Monday. The other half are love letters to a printer "
    "written by people who have clearly never met one. One of you "
    "submitted a grocery list. A GROCERY LIST. With coupons. I am not "
    "angry, I am professionally deceased."
)

MIN_CHARS = 1
MAX_CHARS = 400


def validate(text: str) -> str | None:
    """Return a problem description, or None if the text passes the gate."""
    if not (MIN_CHARS <= len(text) <= MAX_CHARS):
        return f"{len(text)} characters, outside {MIN_CHARS}..{MAX_CHARS}"
    if not text.strip():
        return "only whitespace"
    if text != text.strip():
        return "leading or trailing whitespace would waste characters"
    return None


def main() -> int:
    problem = validate(RANT)
    if problem is not None:
        print(f"rant fails the gate: {problem}", file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(RANT)

    with open(path, "rb") as fh:
        raw = fh.read()
    written = raw.decode("utf-8")
    if written != RANT or len(raw) != len(RANT.encode("utf-8")):
        print("read-back mismatch", file=sys.stderr)
        return 1
    problem = validate(written)
    if problem is not None:
        print(f"written file fails the gate: {problem}", file=sys.stderr)
        return 1

    print(f"wrote {len(written)} characters ({len(raw)} bytes) to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
