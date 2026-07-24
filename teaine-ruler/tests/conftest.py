import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "teaine-common"))
sys.path.insert(0, str(ROOT / "teaine-ruler"))

RULER_ROOT = ROOT / "teaine-ruler"
os.environ.setdefault("TEAINE_RULER_SERVICE_NAME", "ruler")
os.environ.setdefault("TEAINE_RULER_DATA_DIR", str(RULER_ROOT / "app" / "data"))
os.environ.setdefault(
    "TEAINE_RULER_PROMPT_DATA_DIR", str(RULER_ROOT / "app" / "data" / "prompt")
)
os.environ.setdefault(
    "TEAINE_RULER_CORPUS_DATA_DIR", str(RULER_ROOT / "app" / "data" / "corpus")
)
os.environ.setdefault(
    "TEAINE_RULER_KMS_DATA_FILE", str(RULER_ROOT / "app" / "data" / "kms.json")
)
os.environ.setdefault("TEAINE_RULER_DATABASE_URL", "postgresql+asyncpg://test")
os.environ.setdefault("TEAINE_RULER_INTERNAL_API_KEYS", '{"dev":"dev-secret"}')
