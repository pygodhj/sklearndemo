import json
from pathlib import Path

# --- 1. 定义项目根目录 ---
# 使用 Path(__file__) 是现代 Python 中更推荐的路径操作方式
# Path(__file__) -> E:\sklearndemo\sklearndemo\config.py
# .resolve() -> 获取绝对路径
# .parent -> E:\sklearndemo\sklearndemo (包目录)
# .parent.parent -> E:\sklearndemo (项目根目录)
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# --- 2. 定义配置文件路径 ---
CONFIG_PATH = PROJECT_ROOT / "config.json"  # 使用 / 操作符拼接路径，跨平台兼容

# --- 3. 加载配置 ---
_config = {}
if CONFIG_PATH.exists():
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        _config = json.load(f)
else:
    print(f"警告: 未在 {PROJECT_ROOT} 找到配置文件 {CONFIG_PATH.name}。将使用默认配置。")

# --- 4. 定义可导出的配置变量 ---
# 使用 .get() 方法，确保即使配置文件中没有对应项，程序也不会崩溃
DATA_DIR = PROJECT_ROOT / _config.get("data_dir", "data")
RAW_DIR = PROJECT_ROOT / _config.get("raw_dir", "data/raw")
PROCESSED_DIR = PROJECT_ROOT / _config.get("processed_dir", "data/processed")
NOTEBOOKS_DIR = PROJECT_ROOT / _config.get("notebooks_dir", "notebooks")
REPORTS_DIR= PROJECT_ROOT / _config.get("reports_dir", "reports")
SKLEARNDEMO_DIR = PROJECT_ROOT / _config.get("sklearndemo_dir", "sklearndemo")
SRC_DIR = PROJECT_ROOT / _config.get("src_dir", "sklearndemo/src")
DATABASE_MODELS_DIR = PROJECT_ROOT / _config.get("database_models_dir", "sklearndemo/database_models")
DB_DIR = PROJECT_ROOT / _config.get("db_dir", "sklearndemo/database_models/db")
# 你可以在这里添加更多配置
# API_KEY = _config.get("api_key", "your_default_api_key")

# --- 5. (可选) 自动创建目录 ---
# 在模块加载时，就确保这些目录存在
def create_directories():
    for directory in [DATA_DIR,RAW_DIR, PROCESSED_DIR,NOTEBOOKS_DIR,REPORTS_DIR,SKLEARNDEMO_DIR,SRC_DIR,DATABASE_MODELS_DIR,DB_DIR]:
        directory.mkdir(parents=True, exist_ok=True)
        # print(f"确保目录存在: {directory}")

# 当这个模块被导入时，自动执行创建目录的函数
create_directories()

# --- 6. 导出变量，方便其他模块导入 ---
__all__ = [
    "PROJECT_ROOT",
    "DATA_DIR",
    "RAW_DIR",
    "PROCESSED_DIR",
    "NOTEBOOKS_DIR",
    "REPORTS_DIR",
    "SKLEARNDEMO_DIR",
    "SRC_DIR",
    "DATABASE_MODELS_DIR",
    "DB_DIR"
]