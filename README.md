# Skill Router

**Runtime polymorphism for AI agent expertise**

Skill Router brings intelligent, embedding-based dispatch to modular AI skills. Route user queries to the right expertise module in ~10ms instead of waiting for LLM-based selection.

[![PyPI](https://img.shields.io/pypi/v/skill-router)](https://pypi.org/project/skill-router/)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue)](LICENSE)
[![Tests](https://img.shields.io/github/actions/workflow/status/01100001singh/skill-router/ci.yml)](https://github.com/01100001singh/skill-router/actions)

## Why Skill Router?

| Problem | Current State | With Skill Router |
|---------|--------------|-------------------|
| Skill selection latency | Full LLM inference pass | ~10ms embedding lookup |
| Routing determinism | Varies with temperature, prompt | Reproducible similarity scores |
| Audit trails | Implicit in LLM reasoning | Explicit, logged decisions |
| Testability | Probabilistic assertions | Deterministic unit tests |

## Quick Start

```bash
pip install skill-router
```

```python
from skill_router import SkillVTable, HybridStrategy
from skill_router.encoders import OpenAIEncoder

# Initialize router
vtable = SkillVTable(
    skills_dir="./skills",
    encoder=OpenAIEncoder(),
    strategy=HybridStrategy(confidence_threshold=0.85)
)

# Route a query
result = vtable.dispatch("Extract tables from financial_report.pdf")
print(f"Selected: {result.skill_name} (confidence: {result.confidence:.2f})")
# Selected: pdf (confidence: 0.94)

# Get the skill content for your LLM context
skill_content = result.skill_path.read_text()
```

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Request                             │
│              "Extract tables from financial_report.pdf"          │
└─────────────────────────────────┬───────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                    SKILL VTABLE LAYER                            │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                   Strategy Selection                       │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐│  │
│  │  │  Semantic   │  │ Classifier  │  │  Hybrid (default)   ││  │
│  │  │  (fast)     │  │ (accurate)  │  │  semantic + fallback││  │
│  │  └─────────────┘  └─────────────┘  └─────────────────────┘│  │
│  └───────────────────────────────────────────────────────────┘  │
│                                  │                               │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                   Skill Registry                           │  │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────────────┐  │  │
│  │  │   pdf   │ │  docx   │ │  xlsx   │ │credit-scoring   │  │  │
│  │  │ [embed] │ │ [embed] │ │ [embed] │ │    [embed]      │  │  │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────────────┘  │  │
│  │              Cosine Similarity Ranking                     │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                  │                               │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                  Dispatch Decision                         │  │
│  │  skill: "pdf"  confidence: 0.94  strategy: "semantic"      │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## Integrations

- **Claude Code**: Native skill routing for Claude Code agents
- **MCP Servers**: MCP tool integration
- **LangChain**: `SkillRouterTool` wrapper

## Industry Use Cases

| Industry | Use Cases |
|----------|-----------|
| **Financial Services** | Loan underwriting, KYC/AML compliance, invoice processing, fraud detection |
| **Healthcare** | Clinical documentation, diagnostic support, care coordination |
| **Insurance** | Claims processing, policy quoting, underwriting |
| **Legal** | Contract review, e-discovery, regulatory filing |
| **Enterprise** | HR onboarding, procurement, financial close |

## Key Differentiator

| Existing Solutions | What They Route | Skill Router |
|-------------------|-----------------|--------------|
| RouteLLM | Strong model ↔ Weak model | Skill modules within same model |
| Semantic Router | Intent → Route/Function | Intent → Domain expertise bundle |
| vLLM Semantic Router | Query → Best model in pool | Query → Best skill for task |
| MCP | Tool selection | Expertise selection (skills > tools) |

## Documentation

- [Getting Started](docs/getting-started.md)
- [Architecture](docs/architecture.md)
- [API Reference](docs/api-reference.md)
- [Skill Authoring Guide](docs/skill-authoring-guide.md)
- [Industry Guides](docs/industry-guides/)

## Contributing

We welcome contributions! See [CONTRIBUTING.md](.github/CONTRIBUTING.md).

### Adding Skills

```bash
# Scaffold a new skill
python scripts/init_skill.py my-skill --description "My custom skill"

# Validate skill format
python scripts/validate_skill.py skills/my-skill/
```

## Citation

```bibtex
@software{skill_router,
  title = {Skill Router: Runtime Polymorphism for AI Agent Expertise},
  year = {2025},
  url = {https://github.com/01100001singh/skill-router}
}
```

## License

Apache 2.0 - See [LICENSE](LICENSE)
