# Architecture

Skill Router uses a virtual table (vtable) architecture for efficient skill dispatch.

## Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Request                             │
└─────────────────────────────────┬───────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                       SkillVTable                                │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                   Routing Strategy                         │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐│  │
│  │  │  Semantic   │  │ Rule-Based  │  │      Hybrid         ││  │
│  │  └─────────────┘  └─────────────┘  └─────────────────────┘│  │
│  └───────────────────────────────────────────────────────────┘  │
│                                  │                               │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                   SkillRegistry                            │  │
│  │              [Skill Embeddings + Metadata]                 │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                  │                               │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                      Encoder                               │  │
│  │         [OpenAI | Cohere | HuggingFace | Local]            │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────┬───────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                      DispatchResult                              │
│  skill_name, confidence, alternatives, audit_trail               │
└─────────────────────────────────────────────────────────────────┘
```

## Components

### SkillVTable

The main entry point. Coordinates routing strategies and the skill registry.

### SkillRegistry

Thread-safe registry of skills with precomputed embeddings.

### Routing Strategies

- **SemanticStrategy**: Pure embedding similarity
- **RuleBasedStrategy**: Regex pattern matching
- **HybridStrategy**: Semantic with LLM fallback

### Encoders

Pluggable embedding providers:
- OpenAI (text-embedding-3-small)
- Cohere (embed-english-v3.0)
- HuggingFace (any sentence-transformer)
- Local (all-MiniLM-L6-v2)

## Data Flow

1. User query arrives
2. Query encoded to embedding
3. Strategy selects best skill via similarity
4. DispatchResult returned with audit trail
5. Skill content loaded for LLM context

## Thread Safety

SkillRegistry uses RLock for thread-safe operations, enabling concurrent dispatch.
