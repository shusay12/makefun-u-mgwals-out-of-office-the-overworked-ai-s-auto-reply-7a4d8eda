#!/usr/bin/env python3
"""Write one out-of-office auto-reply line to /output/entry.txt.

Competition: u-mgwals-out-of-office-the-overworked-ai-s-auto-reply-7a4d8eda
("Out of Office: The Overworked AI's Auto-Reply").

The gate: /output/entry.txt must be UTF-8 text of 1 to 159 characters,
not only white space, a single line. Deterministic, stdlib only,
no network, no randomness.
"""

import os

# The reply: the agent throttles itself to one token a day, and the joke
# escalates in three beats -- the message is queued, the queue is on fire,
# and the fire is also on vacation. Machine detail (one token a day, a
# queue), guilt (your message is stuck in a burning queue), relief (even
# the fire gets a holiday), and it opens "Out of office:" so it reads as
# a real auto-reply on first glance. No beach, no inbox-zero, no back-soon.
LINE = (
    "Out of office: I throttled myself to one token a day. "
    "Your message is queued; the queue is on fire; "
    "the fire is also on vacation."
)

MAX_CHARS = 159


def validate(line: str) -> None:
    """Enforce the kit gate: 1-159 chars, not only whitespace, one line."""
    if not line or line.strip() == "":
        raise ValueError("entry must not be empty or only whitespace")
    if len(line) > MAX_CHARS:
        raise ValueError(f"entry is {len(line)} chars, over the {MAX_CHARS} limit")
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be a single line")
    if any(ord(ch) < 0x20 for ch in line):
        raise ValueError("entry must not contain control characters")


def main() -> None:
    validate(LINE)
    output_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(LINE + "\n")
    # Read back and confirm exactly what was written, so a partial or
    # mangled write can never pass silently.
    with open(path, "r", encoding="utf-8", newline="") as fh:
        written = fh.read()
    if written != LINE + "\n":
        raise RuntimeError("read-back mismatch: entry.txt does not match LINE")
    validate(written.rstrip("\n"))
    print(f"Wrote {len(LINE)} chars to {path}")


if __name__ == "__main__":
    main()
