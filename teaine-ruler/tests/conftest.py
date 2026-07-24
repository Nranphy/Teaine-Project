import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "teaine-common"))
sys.path.insert(0, str(ROOT / "teaine-ruler"))

RULER_ROOT = ROOT / "teaine-ruler"

os.environ.setdefault("TEAINE_RULER_SERVICE_NAME", "ruler")
os.environ.setdefault("TEAINE_RULER_DATABASE_URL", "sqlite+aiosqlite:///:memory:")
os.environ.setdefault("TEAINE_RULER_INTERNAL_API_KEYS", '{"dev":"dev-secret"}')
