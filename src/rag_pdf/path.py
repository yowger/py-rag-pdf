from pathlib import Path
from dotenv import find_dotenv, load_dotenv

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
FILE_NAME = "progit.epub"
DATA_DIR = PROJECT_ROOT / "data"
DOCUMENTS_DIR = DATA_DIR / "documents"
CHROMA_DIR = DATA_DIR / "chroma"
EPUB_PATH = DOCUMENTS_DIR / FILE_NAME

name_without_extension = EPUB_PATH.stem


def ensure_data_dirs() -> None:
    """Create the data directories if they don't exist."""
    DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
