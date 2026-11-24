#!/usr/bin/env python3
"""Two Days of Quiet Dread — entry point.

Writes one code review comment to $MAKEFUN_OUTPUT_DIR/entry.txt
(default /output). The comment is a single line of at most 140
characters that approves a pull request while carrying quiet
existential dread. Standard library only: no network, no clock,
no randomness — two runs write byte-identical output.
"""

import os
import sys

# The entry: approval up front, then the dread, flat and understated.
# "LGTM" is the approval; the tests and the types are the review;
# "I have accepted that this is what the codebase is now" is the
# quiet existential dread — resignation, not a cry for help.
ENTRY = (
    "LGTM. The tests pass, the types check, and I have accepted "
    "that this is what the codebase is now."
)


def validate(text: str) -> None:
    """Gate the entry exactly the way the sealed scorer does, plus
    the approval the judge requires: 1-140 chars, one line, not
    only white space, and it must approve the pull request."""
    if not text or not text.strip():
        raise ValueError("entry is empty or only white space")
    if len(text) > 140:
        raise ValueError(f"entry is {len(text)} chars, over the 140 limit")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if not any(word in text for word in ("LGTM", "Approved", "Approve")):
        raise ValueError("entry does not approve the pull request")


def main() -> int:
    validate(ENTRY)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    target = os.path.join(out_dir, "entry.txt")
    os.makedirs(out_dir, exist_ok=True)
    with open(target, "w", encoding="utf-8") as fh:
        fh.write(ENTRY)
    # Verify the write: read the file back and refuse to hand the
    # grader a truncated or corrupted entry.
    with open(target, "r", encoding="utf-8") as fh:
        written = fh.read()
    if written != ENTRY:
        print("two-days-of-quiet-dread: written entry.txt does not match",
              file=sys.stderr)
        return 1
    print(f"two-days-of-quiet-dread: wrote {len(ENTRY)} chars to {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
