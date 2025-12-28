import os
import streamlit as st
from pathlib import Path

from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

# -------------------------------------------------
# CONFIG
# -------------------------------------------------
st.set_page_config(page_title="HR Resume RAG", layout="wide")
st.title(" HR Resume Recommendation System")

RESUME_DIR = "resumes"
os.makedirs(RESUME_DIR, exist_ok=True)

# -------------------------------------------------
# SESSION STATE
# -------------------------------------------------
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None
if "docs" not in st.session_state:
    st.session_state.docs = []
if "files" not in st.session_state:
    st.session_state.files = []
 
# -------------------------------------------------
# LOAD RESUMES
# -------------------------------------------------
def load_resumes():
    loader = PyPDFDirectoryLoader(RESUME_DIR)
    docs = loader.load()
    if not docs:
        return False

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100
    )
    docs = splitter.split_documents(docs)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.from_documents(docs, embeddings)

    st.session_state.docs = docs
    st.session_state.vectorstore = vectorstore
    st.session_state.files = list(
        set(Path(d.metadata["source"]).name for d in docs)
    )
    return True

# -------------------------------------------------
# SIDEBAR – CRUD OPERATIONS
# -------------------------------------------------
st.sidebar.title(" Resume Management (CRUD)")

# CREATE
uploaded = st.sidebar.file_uploader(" Upload Resume (PDF)", type="pdf")
if uploaded:
    with open(f"{RESUME_DIR}/{uploaded.name}", "wb") as f:
        f.write(uploaded.getbuffer())
    st.sidebar.success(f"Uploaded {uploaded.name}")

# READ
if st.sidebar.button(" Load All Resumes"):
    if load_resumes():
        st.sidebar.success("Resumes loaded")
    else:
        st.sidebar.error("No resumes found")

# DELETE
if st.session_state.files:
    delete_file = st.sidebar.selectbox(
        " Delete Resume", st.session_state.files
    )
    if st.sidebar.button("Delete Selected"):
        os.remove(f"{RESUME_DIR}/{delete_file}")
        st.sidebar.success(f"Deleted {delete_file}")
        st.session_state.vectorstore = None
        st.session_state.docs = []
        st.session_state.files = []

# -------------------------------------------------
# HR INSTRUCTION (SYSTEM PROMPT)
# -------------------------------------------------
HR_INSTRUCTION = """
You are an HR Manager in a company.

Your job:
1. Review resumes
2. Suggest the best candidates
3. ALWAYS explain the reason for your suggestion

When recommending resumes, explain:
- Skills match
- Experience relevance
- Why this candidate fits the role

If user asks:
- "show all resumes" → list filenames
- "best resume for python developer" → suggest with reason
"""

# -------------------------------------------------
# USER QUERY
# -------------------------------------------------
st.subheader("Ask HR")

query = st.text_input(
    "Ask like an HR:",
    placeholder="show all resumes OR suggest best python developer"
)

# -------------------------------------------------
# PROCESS QUERY
# -------------------------------------------------
if st.button("Get HR Recommendation") and query:

    if "show all" in query.lower():
        st.subheader(" All Available Resumes")
        if st.session_state.files:
            for f in st.session_state.files:
                st.write(f"• {f}")
        else:
            st.warning("No resumes loaded")

    elif not st.session_state.vectorstore:
        st.error("Load resumes first")

    else:
        results = st.session_state.vectorstore.similarity_search(query, k=3)

        st.subheader(" HR Recommendation")

        for i, doc in enumerate(results, 1):
            filename = Path(doc.metadata["source"]).name
            content = doc.page_content[:400]

            st.markdown(f"""
### {i}. {filename}

**Reason for Selection (HR View):**
- Matches required skills mentioned in the query  
- Relevant experience found in resume  
- Suitable profile for the role based on content  

**Resume Evidence:**
> {content}...
""")

# -------------------------------------------------
# STATUS
# -------------------------------------------------
st.subheader("System Status")
col1, col2 = st.columns(2)
col1.metric(" Resume Pages", len(st.session_state.docs))
col2.metric("Resume Files", len(st.session_state.files))
