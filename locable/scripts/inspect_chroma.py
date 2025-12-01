import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from locable.rag.chroma_store import ChromaVectorStore

store = ChromaVectorStore(persist_dir=str(ROOT / "data" / "chroma"), collection_name="bootstrap")
print(store.query("container class css", n_results=3))
