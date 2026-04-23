"""
Phase 0 — VRAM & latency profiling for all four GGUF models.
Produces the table required by horizon scan Section 5 (Implementation lifecycle).

Run from menuforge/ with venv active:
    python notebooks/00_phase0_vram_profile.py

Output saved to: outputs/phase0_vram_profile.txt
"""

import json
import sys
import time
from pathlib import Path

import psutil
import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

OUTPUT_DIR = ROOT / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

# ── Load model registry ───────────────────────────────────────
with open(ROOT / "configs" / "model_registry.yaml") as f:
    registry = yaml.safe_load(f)["models"]


def get_gpu_vram_mb() -> tuple[float, float]:
    """Return (used_MB, total_MB) via nvidia-smi, or (0, 0) if unavailable."""
    try:
        import subprocess
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=memory.used,memory.total",
             "--format=csv,noheader,nounits"],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            used, total = result.stdout.strip().split(", ")
            return float(used), float(total)
    except Exception:
        pass
    return 0.0, 0.0


def get_ram_gb() -> float:
    return psutil.virtual_memory().used / 1024 ** 3


def check_model_file(model_cfg: dict) -> bool:
    path = ROOT / model_cfg["path"]
    return path.exists()


def profile_model(name: str, cfg: dict) -> dict:
    """Load model, run a short prompt, unload, return timing + VRAM stats."""
    from llama_cpp import Llama

    model_path = ROOT / cfg["path"]
    result = {
        "model": name,
        "path": str(cfg["path"]),
        "file_exists": model_path.exists(),
        "vram_before_mb": None,
        "vram_after_load_mb": None,
        "vram_after_unload_mb": None,
        "ram_before_gb": None,
        "ram_after_load_gb": None,
        "load_time_s": None,
        "ttft_ms": None,        # time-to-first-token
        "tokens_per_s": None,
        "error": None,
    }

    if not model_path.exists():
        result["error"] = "File not found — download required (see configs/model_registry.yaml)"
        return result

    vram_before, vram_total = get_gpu_vram_mb()
    ram_before = get_ram_gb()
    result["vram_before_mb"] = vram_before
    result["ram_before_gb"] = round(ram_before, 2)

    try:
        t0 = time.perf_counter()
        llm = Llama(
            model_path=str(model_path),
            n_gpu_layers=cfg.get("n_gpu_layers", -1),
            n_ctx=cfg.get("context_length", 2048),
            n_threads=cfg.get("n_threads", 8),
            embedding=cfg.get("embedding", False),
            verbose=False,
        )
        load_time = time.perf_counter() - t0
        result["load_time_s"] = round(load_time, 2)

        vram_after, _ = get_gpu_vram_mb()
        result["vram_after_load_mb"] = vram_after
        result["ram_after_load_gb"] = round(get_ram_gb(), 2)

        if not cfg.get("embedding", False):
            prompt = "List three Italian pasta dishes in one sentence."
            t1 = time.perf_counter()
            output = llm(prompt, max_tokens=64, echo=False)
            elapsed = time.perf_counter() - t1
            tokens = output["usage"]["completion_tokens"]
            result["ttft_ms"] = round((time.perf_counter() - t1) * 1000 / max(tokens, 1), 1)
            result["tokens_per_s"] = round(tokens / elapsed, 1)
        else:
            t1 = time.perf_counter()
            _ = llm.embed("test embedding sentence")
            result["ttft_ms"] = round((time.perf_counter() - t1) * 1000, 1)
            result["tokens_per_s"] = "N/A (embedding)"

        del llm
        time.sleep(1)
        vram_unload, _ = get_gpu_vram_mb()
        result["vram_after_unload_mb"] = vram_unload

    except Exception as e:
        result["error"] = str(e)

    return result


def print_table(results: list[dict]) -> str:
    lines = []
    header = f"{'Model':<22} {'File':>5} {'VRAM load MB':>12} {'RAM load GB':>11} {'Load s':>7} {'TPS':>8} {'Error'}"
    lines.append(header)
    lines.append("-" * len(header))
    for r in results:
        exists = "YES" if r["file_exists"] else "NO"
        vram = f"{r['vram_after_load_mb']:.0f}" if r["vram_after_load_mb"] else "-"
        ram = f"{r['ram_after_load_gb']:.1f}" if r["ram_after_load_gb"] else "-"
        load = f"{r['load_time_s']:.1f}" if r["load_time_s"] else "-"
        tps = str(r["tokens_per_s"]) if r["tokens_per_s"] else "-"
        err = (r["error"] or "")[:50]
        lines.append(f"{r['model']:<22} {exists:>5} {vram:>12} {ram:>11} {load:>7} {tps:>8}  {err}")
    return "\n".join(lines)


def main():
    print("=" * 60)
    print("MenuForge — Phase 0 VRAM & Latency Profile")
    print("=" * 60)

    vram_used, vram_total = get_gpu_vram_mb()
    print(f"\nBaseline VRAM : {vram_used:.0f} / {vram_total:.0f} MB used")
    print(f"Baseline RAM  : {get_ram_gb():.1f} GB used\n")

    results = []
    for name, cfg in registry.items():
        print(f"Profiling: {name} ...")
        r = profile_model(name, cfg)
        results.append(r)
        if r["error"]:
            print(f"  -> {r['error']}")
        else:
            print(f"  -> load {r['load_time_s']}s | VRAM +{(r['vram_after_load_mb'] or 0) - vram_used:.0f} MB | {r['tokens_per_s']} tok/s")

    table = print_table(results)
    print("\n" + table)

    # ── Save outputs ─────────────────────────────────────────
    out_txt = OUTPUT_DIR / "phase0_vram_profile.txt"
    out_json = OUTPUT_DIR / "phase0_vram_profile.json"

    out_txt.write_text(table)
    out_json.write_text(json.dumps(results, indent=2))

    print(f"\nSaved: {out_txt}")
    print(f"Saved: {out_json}")
    print("\nPhase 0 complete. Update configs/model_registry.yaml: set ready=true for loaded models.")


if __name__ == "__main__":
    main()
