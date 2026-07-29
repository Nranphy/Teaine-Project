import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "teaine-common"))
sys.path.insert(0, str(ROOT / "teaine-ruler"))

RULER_ROOT = ROOT / "teaine-ruler"

# 冒烟测试必须使用隔离的内存数据库，不读取 .env.test 或外部环境里的真实链接。
os.environ["TEAINE_RULER_SERVICE_NAME"] = "ruler"
os.environ["TEAINE_RULER_DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"
os.environ["TEAINE_RULER_INTERNAL_API_KEYS"] = '{"dev":"dev-secret"}'
os.environ["TEAINE_RULER_KMS_SALT"] = "test-kms-salt"
