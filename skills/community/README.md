# Community Skills

This directory contains community-contributed skills.

## Contributing a Skill

1. Fork the repository
2. Create a new directory: `skills/community/your-skill-name/`
3. Add a `SKILL.md` file with proper frontmatter
4. Submit a PR

## Skill Requirements

Your `SKILL.md` must include:

```yaml
---
name: your-skill-name
description: Brief description of what the skill does
utterances:
  - "example query 1"
  - "example query 2"
keywords:
  - keyword1
  - keyword2
---
```

## Validation

Run the validation script before submitting:

```bash
python scripts/validate_skill.py skills/community/your-skill-name/
```

## Guidelines

- Skills should be focused and specific
- Include clear usage examples
- Document any dependencies
- Follow the existing skill format
