from pathlib import Path
from dotenv import find_dotenv, load_dotenv

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

PROJECT_ROOT = Path(dotenv_path).parent if dotenv_path else Path(
    __file__).resolve().parent

DATA_DIR = PROJECT_ROOT / "data"
CHROMA_DIR = DATA_DIR / "chroma"

FILE_NAME = "progit.epub"
EPUB_PATH = DATA_DIR / "documents" / FILE_NAME

name_without_extension = EPUB_PATH.stem
