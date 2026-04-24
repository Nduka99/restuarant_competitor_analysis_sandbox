# MenuForge 🍽️

**Multi-agent menu design sandbox** — restaurant competitor analysis and menu generation using open-source VLMs/LLMs (Gemma & Qwen).

> _This README is a placeholder. A comprehensive write-up will follow as part of the CMP7226 horizon scan report._

## Project Structure

```
menuforge/
├── notebooks/       # Jupyter notebooks (data acquisition → EDA → vision embeddings)
├── agents/          # LangGraph agent definitions
├── configs/         # YAML settings & model registry
├── eval/            # Evaluation harness
├── utils/           # Shared utilities
├── pyproject.toml   # Project metadata & tool config
└── requirements.txt # Python dependencies
```

## Quick Start

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Tech Stack

| Layer | Tool |
|-------|------|
| Vision encoders | V-JEPA, Qwen2.5-VL |
| Language models | Gemma 3, Qwen2.5 |
| Retrieval | LightRAG / LanceDB |
| Orchestration | LangGraph |
| Hardware target | RTX 4060 Laptop (8 GB VRAM) |

---

*CMP7226 · Horizon Scan Evidence System*
