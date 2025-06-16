from pathlib import Path
import json

# Load stock list from JSON files on startup
DOMESTIC_JSON_PATH = Path(__file__).parent / "symbols" / "domestic.txt"
FOREIGN_JSON_PATH = Path(__file__).parent / "symbols" / "foreign.txt"


def load_domestic_stocks():
    try:
        with open(DOMESTIC_JSON_PATH, encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"❗ 국내 종목 로딩 실패: {str(e)}")
        return []


def load_foreign_stocks():
    try:
        with open(FOREIGN_JSON_PATH, encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"❗ 해외 종목 로딩 실패: {str(e)}")
        return []
