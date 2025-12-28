import re


# ------------------ HELPER FUNCTIONS ------------------

def extract_name(text: str) -> str:
    """
    Extract candidate name from resume text.
    Strategy:
    1. First non-empty line (most resumes have name at top)
    2. Fallback: Capitalized Firstname Lastname pattern
    """
    lines = [l.strip() for l in text.split("\n") if l.strip()]

    if lines:
        first_line = lines[0]
        if len(first_line.split()) <= 4:
            return first_line

    match = re.search(r"\b[A-Z][a-z]+ [A-Z][a-z]+\b", text)
    if match:
        return match.group(0)

    return "Candidate"


def extract_skills(text: str, required_skills: list) -> list:
    """
    Match required skills from query against resume text
    """
    text_lower = text.lower()
    matched = []

    for skill in required_skills:
        if skill.lower() in text_lower:
            matched.append(skill)

    return list(set(matched))


# ------------------ MAIN HR FUNCTION ------------------

def hr_shortlist(query, docs):

    stopwords = {"find", "developer", "developers", "backend", "engineer", "for"}
    required_skills = [
        w for w in query.lower().split()
        if w not in stopwords and len(w) > 2
    ]

    result = "## Shortlisted Candidates\n\n"
    shown = 0

    for i, text in enumerate(docs, 1):
        if shown >= 4:
            break

        name = extract_name(text)
        skills = extract_skills(text, required_skills)

        if skills:
            skills_text = ", ".join(skills)
            reason = f"{name} demonstrates relevant expertise in {skills_text}."
        else:
            skills_text = "General profile match"
            reason = f"{name} has relevant experience suitable for the role."

        result += f"""
### {shown + 1}. Candidate Name: {name}

**Skills Matched:** {skills_text}

**HR Reason:**  
{reason}

---
"""
        shown += 1

    if shown == 0:
        result += "_No suitable resumes found based on the current query._"

    return result
