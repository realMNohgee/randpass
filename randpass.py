#!/usr/bin/env python3
"""randpass — Password/passphrase generator. Zero dependencies, pure Python stdlib."""

from __future__ import annotations

import argparse
import json
import math
import secrets
import string
import sys
from typing import List

# ~200 common words for passphrase generation
WORDLIST: List[str] = [
    "alpha", "bravo", "charlie", "delta", "echo", "foxtrot", "golf", "hotel",
    "india", "juliet", "kilo", "lima", "mike", "november", "oscar", "papa",
    "quebec", "romeo", "sierra", "tango", "uniform", "victor", "whiskey", "xray",
    "yankee", "zulu", "apple", "banana", "cherry", "date", "elderberry", "fig",
    "grape", "honeydew", "kiwi", "lemon", "mango", "nectarine", "orange", "peach",
    "plum", "quince", "raspberry", "strawberry", "tangerine", "watermelon",
    "ant", "bee", "cat", "dog", "elephant", "fox", "giraffe", "horse",
    "iguana", "jaguar", "koala", "lion", "monkey", "newt", "owl", "penguin",
    "quail", "rabbit", "snake", "turtle", "urchin", "vulture", "whale", "yak",
    "zebra", "anchor", "boat", "canyon", "desert", "eagle", "forest", "glacier",
    "harbor", "island", "jungle", "kelp", "lagoon", "mountain", "north", "ocean",
    "plain", "quarry", "river", "storm", "thunder", "valley", "wind", "crystal",
    "amber", "bronze", "copper", "diamond", "emerald", "flint", "gold", "iron",
    "jade", "marble", "nickel", "onyx", "pearl", "quartz", "ruby", "silver",
    "steel", "topaz", "titanium", "uranium", "granite", "cedar", "maple", "oak",
    "pine", "birch", "willow", "spruce", "bamboo", "walnut", "cherry", "elm",
    "raven", "falcon", "hawk", "robin", "sparrow", "dove", "crow", "swan",
    "badger", "beaver", "ferret", "otter", "raccoon", "weasel", "coyote", "bison",
    "dagger", "sword", "shield", "helmet", "castle", "tower", "bridge", "gate",
    "lantern", "candle", "torch", "bonfire", "embers", "spark", "flame", "ash",
    "sage", "thyme", "basil", "clove", "ginger", "nutmeg", "pepper", "saffron",
    "ocean", "coral", "reef", "atoll", "tide", "cove", "beach", "wave",
]


PASSWORD_CHARS = string.ascii_letters + string.digits + "!@#$%^&*()-_=+[]{};:,.<>?"


def generate_password(length: int) -> str:
    """Generate a cryptographically secure password."""
    # Ensure at least one of each character class
    classes = [
        string.ascii_lowercase,
        string.ascii_uppercase,
        string.digits,
        "!@#$%^&*()-_=+[]{};:,.<>?",
    ]
    chars: List[str] = []
    for c in classes:
        chars.append(secrets.choice(c))
    remaining = max(0, length - len(chars))
    chars.extend(secrets.choice(PASSWORD_CHARS) for _ in range(remaining))
    secrets.SystemRandom().shuffle(chars)
    return "".join(chars)


def cmd_password(args: argparse.Namespace) -> int:
    passwords = [generate_password(args.length) for _ in range(args.count)]
    if args.format == "json":
        json.dump({"passwords": passwords}, sys.stdout, indent=2)
        sys.stdout.write("\n")
    else:
        for pw in passwords:
            print(pw)
    return 0


def cmd_passphrase(args: argparse.Namespace) -> int:
    separator = args.separator
    phrases: List[str] = []
    for _ in range(args.count):
        words = [secrets.choice(WORDLIST) for _ in range(args.words)]
        phrases.append(separator.join(words))
    if args.format == "json":
        json.dump({"passphrases": phrases}, sys.stdout, indent=2)
        sys.stdout.write("\n")
    else:
        for p in phrases:
            print(p)
    return 0


def estimate_entropy(password: str) -> float:
    """Estimate entropy in bits based on character class diversity."""
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in "!@#$%^&*()-_=+[]{};:,.<>?/|\\`~\"'" for c in password)

    pool_size = 0
    if has_lower:
        pool_size += 26
    if has_upper:
        pool_size += 26
    if has_digit:
        pool_size += 10
    if has_special:
        pool_size += 32

    if pool_size == 0:
        return 0.0

    return len(password) * math.log2(pool_size)


def cmd_entropy(args: argparse.Namespace) -> int:
    pw = args.password
    ent = estimate_entropy(pw)

    breakdown = {
        "lowercase": any(c.islower() for c in pw),
        "uppercase": any(c.isupper() for c in pw),
        "digits": any(c.isdigit() for c in pw),
        "special": any(c in "!@#$%^&*()-_=+[]{};:,.<>?/|\\`~\"'" for c in pw),
    }

    if args.format == "json":
        result = {
            "password": pw,
            "length": len(pw),
            "entropy_bits": round(ent, 1),
            "character_classes": breakdown,
        }
        json.dump(result, sys.stdout, indent=2)
        sys.stdout.write("\n")
    else:
        print(f"Password: {pw}")
        print(f"Length: {len(pw)}")
        print(f"Estimated entropy: {ent:.1f} bits")
        print(f"Character classes: {', '.join(k for k, v in breakdown.items() if v)}")

    return 0


def main() -> int:
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--format", choices=["text", "json"], default="text")

    p = argparse.ArgumentParser(description="randpass — Secure password/passphrase generator")
    sub = p.add_subparsers(dest="cmd", required=True)

    pw_parser = sub.add_parser("password", parents=[common], help="Generate random passwords")
    pw_parser.add_argument("--length", type=int, default=16, help="Password length (default: 16)")
    pw_parser.add_argument("--count", type=int, default=1, help="Number of passwords (default: 1)")
    pw_parser.set_defaults(func=cmd_password)

    pp_parser = sub.add_parser("passphrase", parents=[common], help="Generate xkcd-style passphrases")
    pp_parser.add_argument("--words", type=int, default=4, help="Number of words (default: 4)")
    pp_parser.add_argument("--count", type=int, default=1, help="Number of passphrases (default: 1)")
    pp_parser.add_argument("--separator", default="-", help="Word separator (default: '-')")
    pp_parser.set_defaults(func=cmd_passphrase)

    ent_parser = sub.add_parser("entropy", parents=[common], help="Estimate password entropy")
    ent_parser.add_argument("password", help="Password to analyze")
    ent_parser.set_defaults(func=cmd_entropy)

    args = p.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
