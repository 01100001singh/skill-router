#!/usr/bin/env python3
"""Validate a skill file."""

import argparse
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from skill_router.parsers.skill_parser import SkillParser


def main():
    parser = argparse.ArgumentParser(description="Validate a skill")
    parser.add_argument("path", help="Path to skill directory or SKILL.md")

    args = parser.parse_args()

    skill_parser = SkillParser()
    errors = skill_parser.validate(args.path)

    if errors:
        print("Validation errors:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)
    else:
        print("Skill is valid!")

        # Print parsed info
        parsed = skill_parser.parse(args.path)
        print(f"\nName: {parsed.name}")
        print(f"Description: {parsed.description}")
        print(f"Utterances: {len(parsed.utterances)}")
        print(f"Keywords: {len(parsed.keywords)}")


if __name__ == "__main__":
    main()
