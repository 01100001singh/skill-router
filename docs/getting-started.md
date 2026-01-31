# Getting Started

This guide will help you get started with Skill Router.

## Installation

```bash
pip install skill-router
```

### With specific encoder support

```bash
# OpenAI embeddings
pip install skill-router[openai]

# Local embeddings (sentence-transformers)
pip install skill-router[local]

# All encoders
pip install skill-router[all]
```

## Quick Start

```python
from skill_router import SkillVTable
from skill_router.encoders import LocalEncoder

# Initialize router with local encoder
vtable = SkillVTable(
    skills_dir="./skills",
    encoder=LocalEncoder()
)

# Route a query
result = vtable.dispatch("Extract tables from report.pdf")
print(f"Selected: {result.skill_name} ({result.confidence:.0%})")
```

## Creating Skills

Skills are markdown files with YAML frontmatter:

```markdown
---
name: my-skill
description: What this skill does
utterances:
  - "example query"
  - "another query"
---

# My Skill

Skill content and instructions here.
```

## Directory Structure

```
your-project/
├── skills/
│   ├── pdf/
│   │   └── SKILL.md
│   ├── docx/
│   │   └── SKILL.md
│   └── custom-skill/
│       └── SKILL.md
└── main.py
```

## Next Steps

- Read the [Architecture](architecture.md) guide
- Learn about [Skill Authoring](skill-authoring-guide.md)
- Explore [Industry Guides](industry-guides/)
