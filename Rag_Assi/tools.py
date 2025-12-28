import os

def save_pdf(uploaded_file):
    os.makedirs("resumes", exist_ok=True)
    path = f"resumes/{uploaded_file.name}"
    with open(path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return uploaded_file.name

def delete_pdf(filename):
    path = f"resumes/{filename}"
    if os.path.exists(path):
        os.remove(path)
