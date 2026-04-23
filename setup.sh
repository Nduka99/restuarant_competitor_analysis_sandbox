#!/usr/bin/env bash
# ============================================================
# MenuForge — WSL2 Ubuntu install script
# Run from the menuforge/ directory inside WSL:
#   bash setup.sh
# ============================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV="$SCRIPT_DIR/.venv"
PYTHON="$VENV/bin/python"
PIP="$VENV/bin/pip"

echo "==> menuforge setup starting..."
echo "    venv : $VENV"
echo "    python: $($PYTHON --version)"

# ── 1. Upgrade pip & wheel ───────────────────────────────────
echo ""
echo "==> Upgrading pip, wheel, setuptools..."
"$PIP" install --upgrade pip wheel setuptools

# ── 2. llama-cpp-python (CUDA wheel — skip if already installed) ──
if "$PYTHON" -c "import llama_cpp" 2>/dev/null; then
    INSTALLED=$("$PIP" show llama-cpp-python | grep ^Version | awk '{print $2}')
    echo ""
    echo "==> llama-cpp-python $INSTALLED already installed — skipping CUDA build."
    echo "    See requirements-cuda.txt if you need to reinstall."
else
    echo ""
    echo "==> Building llama-cpp-python with CUDA support..."
    CMAKE_ARGS="-DGGML_CUDA=on" FORCE_CMAKE=1 \
        "$PIP" install llama-cpp-python==0.3.20 \
        --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cu121
fi

# ── 3. Main runtime dependencies ────────────────────────────
echo ""
echo "==> Installing runtime dependencies..."
"$PIP" install -r "$SCRIPT_DIR/requirements.txt"

# ── 4. Dev dependencies (optional) ──────────────────────────
if [[ "${1:-}" == "--dev" ]]; then
    echo ""
    echo "==> Installing dev dependencies..."
    "$PIP" install -r "$SCRIPT_DIR/requirements-dev.txt"
fi

# ── 5. Verify key imports ────────────────────────────────────
echo ""
echo "==> Verifying key imports..."
"$PYTHON" - <<'EOF'
checks = {
    "llama_cpp":      "llama-cpp-python",
    "langgraph":      "langgraph",
    "langchain_core": "langchain-core",
    "chromadb":       "chromadb",
    "transformers":   "transformers",
    "gradio":         "gradio",
    "pandas":         "pandas",
    "yaml":           "pyyaml",
}
failed = []
for mod, pkg in checks.items():
    try:
        __import__(mod)
        print(f"  OK  {pkg}")
    except ImportError:
        print(f"  FAIL {pkg}")
        failed.append(pkg)
if failed:
    print(f"\nFailed imports: {failed}")
    raise SystemExit(1)
print("\nAll checks passed.")
EOF

# ── 6. Freeze lock file ──────────────────────────────────────
echo ""
echo "==> Writing requirements.lock..."
"$PIP" freeze > "$SCRIPT_DIR/requirements.lock"
echo "    Saved to requirements.lock"

echo ""
echo "==> Setup complete."
echo "    Activate venv: source .venv/bin/activate"
echo "    Run Phase 0 profiling: python notebooks/00_phase0_vram_profile.py"
