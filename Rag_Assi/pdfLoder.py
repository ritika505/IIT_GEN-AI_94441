
# Install first (if needed)
# pip install pypdf langchain-community

from langchain_community.document_loaders import PyPDFDirectoryLoader

# Point to your folder containing all PDFs
loader = PyPDFDirectoryLoader("D:/Git/test_app/IIT_GEN-AI_94441/RAG_Assi/resume")
documents = loader.load()

# Check what you got
print(f"✅ Loaded {len(documents)} pages")
print(f"📁 From {len(set(doc.metadata['source'] for doc in documents))} unique PDFs")

# See first few docs
for i, doc in enumerate(documents[:3]):
    print(f"\n📄 Page {i+1}: {doc.metadata['source']}")
    print(f"   Preview: {doc.page_content[:100]}...")