#!/usr/bin/env python3
"""Scaffold a new skill."""

import argparse
from pathlib import Path


SKILL_TEMPLATE = '''---
name: {name}
description: {description}
utterances:
  - "example query for {name}"
  - "another way to ask for {name}"
keywords:
  - {name}
---

# {title}

{description}

## Capabilities

- Capability 1
- Capability 2

## Usage

Describe how to use this skill.

## Examples

```python
# Example code
```
'''


def main():
    parser = argparse.ArgumentParser(description="Scaffold a new skill")
    parser.add_argument("name", help="Skill name (kebab-case)")
    parser.add_argument("--description", "-d", default="A new skill", help="Skill description")
    parser.add_argument("--output", "-o", default="skills/community", help="Output directory")

    args = parser.parse_args()

    # Create skill directory
    output_dir = Path(args.output) / args.name
    output_dir.mkdir(parents=True, exist_ok=True)

    # Create SKILL.md
    skill_file = output_dir / "SKILL.md"
    title = args.name.replace("-", " ").title()

    content = SKILL_TEMPLATE.format(
        name=args.name,
        description=args.description,
        title=title
    )

    skill_file.write_text(content)
    print(f"Created skill at: {skill_file}")


if __name__ == "__main__":
    main()
