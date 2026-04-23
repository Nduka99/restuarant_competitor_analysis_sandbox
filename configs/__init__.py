"""Config loading helpers."""

from pathlib import Path
import yaml

_CONFIGS_DIR = Path(__file__).parent


def load(name: str) -> dict:
    """Load a YAML config file by stem name, e.g. load('settings')."""
    path = _CONFIGS_DIR / f"{name}.yaml"
    with path.open() as f:
        return yaml.safe_load(f)
