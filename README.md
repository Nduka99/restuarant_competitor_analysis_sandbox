# MenuForge Sandbox V2

Sandbox V2 is the evidence-first research sandbox for MenuForge: a local, notebook-driven pipeline for turning text-heavy menu images and menu-like documents into auditable structured signals before any image generator is trusted.

The sandbox supports the horizon-scan thesis that reliable restaurant menu generation should begin with rich feature records, schema-first rendering, OCR verification, and human-governed revision rather than direct caption-to-image prompting. The final Horizon Scan document at `horizon_scan/Horizon_Scan.docx` is the strategic source for the future implementation plan.

## Current Status

Sandbox V2 is complete through Notebook 9.

Implemented:

- source and model registration
- public and synthetic menu-source scouting
- unified document manifest across eight sources
- local PaddleOCR PP-OCRv5 baseline
- constrained PaddleOCR-VL diagnostic comparison
- deterministic schema normalisation
- extraction metrics
- image-generation readiness scoring
- schema-first composite render proof with OCR-after-render checks

Not yet implemented:

- live prompt packs for Qwen-Image, Z-Image-Turbo, or other image generators
- production menu generation
- LoRA, DreamBooth, or adapter training
- full LangChain/LangGraph agent orchestration
- partner-data ingestion
- deployed user interface

The strongest current claim is deliberately narrow: the local pipeline can extract, normalise, score, and render menu-generation signals from heterogeneous text-heavy documents. It does not prove a production-grade autonomous menu-generation product.

## Why This Sandbox Exists

Restaurant menus are dense commercial documents. A useful AI menu system must preserve dish names, sections, prices, descriptions, dietary signals, reading order, layout, visual style, brand constraints, and competitor positioning. A visually attractive image is not good enough if the text is wrong.

Sandbox V2 therefore treats menu generation as a representation problem first:

1. Collect menu and document evidence with provenance.
2. Extract OCR, layout, and source metadata.
3. Normalise extraction into menu schema rows.
4. Score whether each document is useful for generation, review, style reference, or evaluation control.
5. Render from schema deterministically.
6. Verify rendered outputs with OCR.
7. Keep image generation as an experimental branch until text fidelity can be measured.

## Key Finding

The most important result is the OCR versus document-VLM comparison.

On the eight-document smoke sample, PaddleOCR PP-OCRv5 on local CPU produced 1,485 text regions with 0 failures and a mean confidence of 0.9413. PaddleOCR-VL-0.9B, run under the constrained CPU `native` backend, produced one coarse region per document and recovered fewer characters than the OCR baseline on every tested document.

This does not mean OCR is universally better than document VLMs. It means model tier choice depends on the actual local resource envelope. For this sandbox, PaddleOCR remains the primary extraction engine and PaddleOCR-VL is retained as diagnostic evidence.

## Evidence Snapshot

| Stage | Result |
|---|---|
| Unified manifest | 848 ready images, 0 load issues, 8 sources |
| Source mix | NYPL, NYPL expanded, Wikimedia menu images, Wikimedia Commons English menus, synthetic menu concepts, SROIE, FUNSD, CORD |
| OCR baseline | 8/8 sample documents processed, 1,485 regions, 0 failures, 0.9413 mean confidence |
| Document VLM diagnostic | 8/8 documents processed, 8 total coarse regions, 52.339s mean runtime |
| Schema normalisation | 277 menu schema rows, 20 manual-review flags |
| Extraction metrics | 0.9096 mean combined extraction quality |
| Readiness gate | 2 ready for generation, 1 needs review, 5 do not generate |
| Render proof | 4 schema-first renders, 4 render successes, 4 OCR-after-render successes |
| Render text coverage | 1.0 mean item-name coverage, 1.0 mean price coverage |

Primary local evidence pack:

- `horizon_scan/SBV2_EVIDENCE_PACK.md`
- `outputs/sandbox_v2/audit_tables/`
- `outputs/figures/sandbox_v2/`
- `data/processed/sandbox_v2/`

These output folders are local evidence artefacts. They are not part of the planned GitHub upload boundary unless explicitly approved later.

## GitHub Publication Boundary

For the next GitHub update, publish only:

- `notebooks/SBV2_*.ipynb`
- this README, `sandbox_v2/README.md`

If the GitHub repository needs a root README, use this file as the source for that root README.

Do not publish by default:

- `data/`
- `outputs/`
- `models/`
- `.cache/`
- raw source downloads
- generated render artefacts
- Horizon Scan assessment documents
- private notes or local environment files

The notebooks should be treated as the visible research record. The README should explain the pipeline, evidence, scope, and next work without requiring raw datasets to be public.

## Repository Map

```text
menuforge/
+-- sandbox_v2/
|   +-- README.md
|   +-- IMPLEMENTATION_PLAN.md
|   +-- SOURCE_AND_MODEL_REGISTER.md
|   +-- env.sh
|   +-- ocr_baseline.py
|   +-- local_vlm_extraction.py
|   +-- document_dataset_loading.py
|   +-- schema_normalisation.py
|   +-- extraction_metrics.py
|   +-- readiness_scoring.py
|   +-- menu_render.py
|   +-- ready_available_visual_sources.py
|   +-- synthetic_menu_concepts.py
|   +-- wikimedia_menu_copies.py
+-- notebooks/
|   +-- SBV2_00_environment_and_register.ipynb
|   +-- SBV2_01_data_download_and_manifest.ipynb
|   +-- SBV2_02_nypl_sampling.ipynb
|   +-- SBV2_02b_public_menu_source_scouting.ipynb
|   +-- SBV2_02c_ready_available_visual_sources.ipynb
|   +-- SBV2_03_document_dataset_loading.ipynb
|   +-- SBV2_04_ocr_baseline.ipynb
|   +-- SBV2_05_local_vlm_extraction.ipynb
|   +-- SBV2_06_schema_normalisation.ipynb
|   +-- SBV2_07_extraction_metrics.ipynb
|   +-- SBV2_08_readiness_scoring.ipynb
|   +-- SBV2_09_composite_render_proof.ipynb
+-- data/
|   +-- raw/sandbox_v2/
|   +-- interim/sandbox_v2/
|   +-- processed/sandbox_v2/
+-- outputs/
|   +-- sandbox_v2/
|   +-- figures/sandbox_v2/
+-- horizon_scan/
    +-- Horizon_Scan.docx
    +-- SBV2_EVIDENCE_PACK.md
```

## Notebook Pipeline

| Notebook | Purpose | Main outputs |
|---|---|---|
| `SBV2_00_environment_and_register.ipynb` | Verify hardware, packages, paths, and source/model register | runtime summary, package audit, register preview |
| `SBV2_01_data_download_and_manifest.ipynb` | Acquire or verify source datasets | acquisition table, source counts, NYPL handoff |
| `SBV2_02_nypl_sampling.ipynb` | Sample NYPL menu pages and staged Wikimedia menu images | menu-page manifests, contact sheets, review tables |
| `SBV2_02b_public_menu_source_scouting.ipynb` | Scout additional public menu-image sources | public-source cards, inclusion review, source manifests |
| `SBV2_02c_ready_available_visual_sources.ipynb` | Freeze the first ready visual-source handoff | ready-source manifest, keep/defer/reject ledger |
| `SBV2_03_document_dataset_loading.ipynb` | Build the unified document manifest | 848-row manifest, source mix, contact sheet |
| `SBV2_04_ocr_baseline.ipynb` | Run local PaddleOCR baseline | OCR JSONL, text regions, overlay contact sheet |
| `SBV2_05_local_vlm_extraction.ipynb` | Run constrained PaddleOCR-VL diagnostic | VLM JSONL, comparison table, diagnostic contact sheet |
| `SBV2_06_schema_normalisation.ipynb` | Convert OCR outputs into menu-generation schema rows | schema CSV/parquet, validation issues, extraction-source decision |
| `SBV2_07_extraction_metrics.ipynb` | Score text and schema extraction quality | document/source metric tables, extraction-quality chart |
| `SBV2_08_readiness_scoring.ipynb` | Assign each sample document a generation role | readiness scores, prompt candidates, role counts |
| `SBV2_09_composite_render_proof.ipynb` | Render selected schema rows into menu artefacts and OCR-check them | HTML/PDF/PNG renders, render audit, proof figure |

## Source Roles

| Source | Role in Sandbox V2 |
|---|---|
| NYPL | Real historical menu pages; useful but sometimes weak schema evidence |
| NYPL expanded | Stronger menu-page candidate source for schema and readiness evidence |
| Wikimedia English menus | Real menu-image style sidecar; licence and attribution must remain explicit |
| Wikimedia Commons English menus | Public visual diversity sidecar; per-file licence handling required |
| Synthetic menu concepts | Known-good control for schema, rendering, and OCR-after-render checks |
| SROIE | English receipt key-value control for OCR robustness |
| FUNSD | Form layout/key-value control for document robustness |
| CORD | Receipt/menu-structure sidecar; not used for English generation claims |

## Setup

Use Python 3.11. The repo keeps heavyweight caches inside the project so notebook runs do not spill into user-level cache folders.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-paddle.txt
pip install -r requirements.txt
source sandbox_v2/env.sh
jupyter lab notebooks/
```

`sandbox_v2/env.sh` redirects PaddleX, Hugging Face, pip, Torch, Matplotlib, and Jupyter caches under `.cache/`. Source it before launching notebooks or running sandbox helper modules.

## Local-First Execution Rules

- Keep notebooks as the primary evidence surface.
- Keep helper scripts aligned with notebook logic.
- Record every source, model, and tool in `SOURCE_AND_MODEL_REGISTER.md`.
- Load only one heavyweight model at a time on the RTX 4060 Laptop GPU class target.
- Treat model failures and CPU/GPU constraints as evidence, not as hidden errors.
- Do not describe planned generation experiments as completed work.
- Do not promote style-reference images into training data until licence and attribution status is verified.
- Store generated artefacts separately from ground truth.
- Preserve manual-review flags rather than smoothing them away.

## Core Data Products

| Artefact | Local path | Meaning |
|---|---|---|
| Unified manifest | `data/interim/sandbox_v2/manifests/sbv2_03_document_manifest.csv` | All ready document images and source metadata |
| OCR text regions | `data/interim/sandbox_v2/ocr_outputs/sbv2_04_ocr_text_regions.csv` | PaddleOCR line-level text, confidence, and boxes |
| VLM diagnostic regions | `data/interim/sandbox_v2/vl_outputs/sbv2_05_vl_text_regions.csv` | PaddleOCR-VL diagnostic output |
| Menu schema | `data/processed/sandbox_v2/menu_generation_schema.csv` | Normalised section/item/price rows |
| Extraction metrics | `data/processed/sandbox_v2/extraction_metrics.csv` | Quality metrics by document/source |
| Readiness scores | `data/processed/sandbox_v2/readiness_scores.csv` | Generation-readiness labels and training-signal roles |
| Render audit | `outputs/sandbox_v2/audit_tables/sbv2_09_composite_render_audit.csv` | Render success and OCR-after-render coverage |

## Figures Worth Reusing Locally

| Figure | Local path |
|---|---|
| Current sandbox architecture | `outputs/figures/sandbox_v2/sbv2_architecture_current.png` |
| Source mix | `outputs/figures/sandbox_v2/sbv2_03_source_mix.png` |
| Unified document contact sheet | `outputs/figures/sandbox_v2/sbv2_03_unified_document_contact_sheet.jpg` |
| OCR baseline overlay | `outputs/figures/sandbox_v2/sbv2_04_ocr_overlay_contact_sheet.jpg` |
| OCR versus PaddleOCR-VL | `outputs/figures/sandbox_v2/sbv2_05_baseline_vs_vl_comparison.png` |
| Schema rows by source | `outputs/figures/sandbox_v2/sbv2_06_schema_rows_by_source.png` |
| Extraction quality | `outputs/figures/sandbox_v2/sbv2_07_extraction_quality.png` |
| Readiness gate | `outputs/figures/sandbox_v2/sbv2_08_readiness_scores.png` |
| Composite render proof | `outputs/figures/sandbox_v2/sbv2_09_composite_render_proof.jpg` |
| Future framework diagram | `outputs/figures/sandbox_v2/menuforge_framework_future.png` |

## Horizon Scan Carry-Forward

`horizon_scan/Horizon_Scan.docx` frames the next phase as a 4-to-6-month feasibility study for a competitor-aware, brand-preserving, agentic restaurant menu-generation framework.

The implementation direction from the scan:

1. Treat menus as text-heavy branded documents, not decorative images.
2. Convert each menu into a rich feature record: image, extracted text, sections, dish names, descriptions, prices, reading order, layout cues, visual style cues, brand rules, competitor brief, model outputs, and approval status.
3. Use a shared design world state for agents rather than passing loose prompts between tools.
4. Use LangChain tools and LangGraph orchestration for market analysis, menu strategy, schema-constrained content generation, visual composition, OCR verification, critique, human review, and iterative revision.
5. Keep schema-first rendering as the baseline.
6. Test Qwen-Image, Z-Image-Turbo, and other text-aware image models as an experimental branch conditioned on schema, layout, and brand features rather than captions alone.
7. Compare schema-first rendering and one-shot image generation only after both have measurable OCR, layout, price, and brand-fit checks.
8. Keep human approval and source/licence governance in the loop.

## Future Implementation Roadmap

### Month 1: Freeze the Research Substrate

- Freeze task definitions and output formats.
- Define the LangGraph state object.
- Preserve a manually checked holdout set.
- Turn source records into durable feature records.
- Extend the source/model register for partner-data and model-licence governance.
- Define evaluation criteria before adding new generators.

### Months 2-3: Build the Agentic Baseline

- Add competitor retrieval agents for grounded mini-briefs.
- Add schema-constrained LLM nodes for menu content.
- Extend deterministic HTML/CSS rendering templates.
- Evaluate item-name coverage, price coverage, category structure, OCR-after-render recovery, and basic brand fit.
- Keep notebooks as the audit trail while moving stable logic into reusable modules.

### Months 3-5: Test the Experimental Image Branch

- Build prompt packs from readiness-approved schema rows.
- Test text-aware image generation with Qwen-Image, Z-Image-Turbo, or comparable open models.
- Condition generation on schema, layout, and brand features.
- Run OCR-after-generation and layout checks.
- Record VRAM, RAM, runtime, failures, and model-licence constraints.

### Month 6: Compare Routes

- Compare schema-first rendering against one-shot image generation.
- Keep schema-first rendering as the publishable route if image generation remains text-unreliable.
- Promote only measured results into the research narrative.
- Keep speculative agent and image-generation claims separate from implemented evidence.

## Governance And Ethics

Sandbox V2 keeps research evidence, production intent, and experimental comparison separate.

Required before partner data:

- NDA and processing terms
- asset-rights review
- model-licence compatibility review
- storage-location decision
- adapter retention and deletion policy
- output ownership decision
- human approval workflow

Synthetic data is useful as a known-good control, but it must stay labelled as synthetic and must not be used as proof of real-world cultural, commercial, or partner-data coverage.

Competitor evidence must be used for analysis, not imitation. Menu generation should not generalise across cuisines, cultures, or brands without representative evidence and human review.

## Development Notes

The helper modules mirror notebook stages:

- `document_dataset_loading.py` builds and validates document manifests.
- `ocr_baseline.py` wraps PaddleOCR processing and text-region outputs.
- `local_vlm_extraction.py` supports the PaddleOCR-VL diagnostic route.
- `schema_normalisation.py` converts OCR output into menu-generation rows.
- `extraction_metrics.py` computes text/schema metrics.
- `readiness_scoring.py` assigns generation-readiness labels and roles.
- `menu_render.py` renders schema rows and supports OCR-after-render checks.

When adding new code, keep notebook outputs visible first. Promote helper functions only after the notebook has produced auditable tables and figures.

## What Success Looks Like Next

The next successful version of Sandbox V2 should produce:

- a stronger manually reviewed menu holdout
- richer feature records with layout and visual style cues
- a minimal LangGraph state and agent loop
- grounded competitor mini-briefs with citations
- deterministic renders across more templates
- prompt packs from readiness-approved rows
- a measured image-generation experiment with OCR-after-generation checks
- an explicit route comparison between schema-first rendering and one-shot generation

Until that evidence exists, the public claim remains: Sandbox V2 validates the preprocessing, schema, readiness, and render-check layers needed before controlled menu generation can be attempted.
