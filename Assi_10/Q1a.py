from sentence_transformers import SentenceTransformer
import numpy as np
from langchain_text_splitters import CharacterTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_text_splitters import TokenTextSplitter
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_text_splitters import SentenceTransformersTokenTextSplitter

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

embed_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

sentences = [
    "I love football.",
    "Soccer is my favorite sport.",
    "Messi talks Spanish.",
    "Naive (Bad): Split every N characters. Break sentences randomly Semantic"
    "(Better): Split by: paragraphs, headings, sentences."
]

embeddings = embed_model.encode(sentences)

print("Similarity 1 & 2:", cosine_similarity(embeddings[0], embeddings[1]))
print("Similarity 1 & 3:", cosine_similarity(embeddings[0], embeddings[2]))
print("Similarity 1 & 4:", cosine_similarity(embeddings[0], embeddings[3]))
# print("Similarity 1 & 5:", cosine_similarity(embeddings[0], embeddings[4]))

raw_text = " ".join(sentences)
code_text = code_text = """
def add(a, b):
    return a + b

def multiply(a, b):
    return a * b
"""
# -------------------------------
# Basic Fixed-Size chunking 
char_splitter = CharacterTextSplitter(chunk_size=100 ,chunk_overlap=10)
docs = char_splitter.create_documents([raw_text])

# -------------------------------
# 2. Recursive Chunking
recursive_splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=10,
    separators=["\n\n", "\n", " ",""]
)
recursive_docs = recursive_splitter.create_documents([raw_text])


# -------------------------------
# 3. Token Chunking
token_splitter = TokenTextSplitter(chunk_size=30, chunk_overlap=7)
token_docs = token_splitter.create_documents([raw_text])


# -------------------------------
# 4. Markdown Chunking
markdown_text = """
# Sports
## Football
Football is popular worldwide.
## Soccer
Soccer is loved by many.
## Naive Chunking
Information of chunk.
"""

md_splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=[("#", "H1"), ("##", "H2") ,("###", "H3")]
)
md_docs = md_splitter.split_text(markdown_text)

# -------------------------------
# 5. Code-Aware Chunking
code_splitter =RecursiveCharacterTextSplitter.from_language(
    language="python",
    chunk_size =100,
    chunk_overlap = 10
)
code_docs = code_splitter.create_documents([code_text])


# -------------------------------
# 6. Sentence-Based Chunking
sentence_splitter = SentenceTransformersTokenTextSplitter(
    chunk_size=10,
    chunk_overlap=2
)
sentence_docs = sentence_splitter.create_documents([raw_text])

print("Chunking completed successfully.")