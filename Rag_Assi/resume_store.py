import os
import faiss
from sentence_transformers import SentenceTransformer
from langchain_community.document_loaders import PyPDFDirectoryLoader

VECTORSTORE = None
DOCS = []  # list of dicts: {"text": ..., "source": ...}
FILES = []

# Local embedding model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def embed_texts(texts):
    """Convert list of texts to embeddings."""
    return model.encode(texts, convert_to_numpy=True)

def load_resumes():
    """Load all PDFs in ./resumes and create FAISS index."""
    global VECTORSTORE, DOCS, FILES

    os.makedirs("resumes", exist_ok=True)
    pdfs = [f for f in os.listdir("resumes") if f.endswith(".pdf")]
    if not pdfs:
        return "No resumes found."

    loader = PyPDFDirectoryLoader("resumes")
    pages = loader.load()

    DOCS.clear()
    for page in pages:
        DOCS.append({
            "text": page.page_content,
            "source": page.metadata["source"]
        })

    FILES[:] = list(set(d["source"] for d in DOCS))

    # Embed all pages
    embeddings = embed_texts([d["text"] for d in DOCS])

    # Create FAISS index
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    VECTORSTORE = {
        "index": index,
        "docs": DOCS,
        "embeddings": embeddings
    }

    return f"Loaded {len(FILES)} resumes ({len(DOCS)} pages)"

def list_resumes():
    return [os.path.basename(f) for f in FILES]

def search_resumes(query, k=4):
    if VECTORSTORE is None:
        return []

    query_vec = embed_texts([query])[0].reshape(1, -1)
    distances, indices = VECTORSTORE["index"].search(query_vec, k)
    results = [VECTORSTORE["docs"][i] for i in indices[0]]
    return results
