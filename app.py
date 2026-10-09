import re
import io
from collections import Counter
import streamlit as st
import pandas as pd
import pdfplumber

st.set_page_config(page_title="CareerMatch | Resume Analyzer", page_icon="🎯", layout="wide")

# Simple keyword taxonomy; extend this list as you learn more skills.
SKILL_CATEGORIES = {
    "Programming": ["python", "sql", "r", "java", "c++", "javascript", "typescript"],
    "Data Analysis": ["excel", "pandas", "numpy", "data cleaning", "data analysis", "statistics", "power bi", "tableau", "looker", "matplotlib", "seaborn"],
    "Machine Learning": ["machine learning", "scikit-learn", "sklearn", "regression", "classification", "random forest", "nlp", "natural language processing", "deep learning"],
    "Databases & Tools": ["mysql", "postgresql", "mongodb", "git", "github", "jupyter", "streamlit", "power query", "etl"],
    "Web & Cloud": ["html", "css", "react", "node.js", "flask", "fastapi", "aws", "azure", "google cloud"],
    "AI": ["generative ai", "genai", "llm", "langchain", "langgraph", "rag", "prompt engineering", "agentic ai"]
}
ALL_SKILLS = sorted({s for values in SKILL_CATEGORIES.values() for s in values}, key=len, reverse=True)

def extract_pdf(uploaded_file):
    text_parts = []
    with pdfplumber.open(io.BytesIO(uploaded_file.getvalue())) as pdf:
        for page in pdf.pages:
            text_parts.append(page.extract_text() or "")
    return "\n".join(text_parts).strip()

def normalize(text):
    return re.sub(r"\s+", " ", text.lower())

def find_skills(text):
    normalized = normalize(text)
    found = set()
    for skill in ALL_SKILLS:
        # Phrase-aware matching; boundaries avoid matching "r" inside other words.
        pattern = r"(?<![a-z0-9+#.])" + re.escape(skill) + r"(?![a-z0-9+#.])"
        if re.search(pattern, normalized):
            found.add(skill)
    return found

def category_for(skill):
    for category, skills in SKILL_CATEGORIES.items():
        if skill in skills:
            return category
    return "Other"

def roadmap_for(missing):
    suggestions = {
        "python": "Practice Python fundamentals, functions, files, and small automation tasks.",
        "sql": "Learn SELECT, JOIN, GROUP BY, subqueries, and window functions.",
        "excel": "Practice PivotTables, lookup formulas, charts, and cleaning messy data.",
        "pandas": "Work with DataFrames, missing values, groupby, merges, and date columns.",
        "power bi": "Build a report with a clean data model, DAX measures, and interactive filters.",
        "tableau": "Create a dashboard with calculated fields, filters, and clear visual storytelling.",
        "statistics": "Revise distributions, sampling, confidence intervals, correlation, and hypothesis testing.",
        "machine learning": "Learn train/test splits, baselines, evaluation metrics, and overfitting.",
        "scikit-learn": "Build a pipeline using preprocessing, model training, and cross-validation.",
        "javascript": "Practice variables, functions, arrays, DOM basics, and async fetch.",
        "react": "Learn components, props, state, hooks, and API integration.",
        "git": "Practice commits, branches, pull requests, and resolving simple merge conflicts.",
        "generative ai": "Understand LLM basics, prompt design, evaluation, and responsible use.",
        "rag": "Learn chunking, embeddings, retrieval, and citation-grounded answers.",
        "power query": "Practice importing, transforming, merging, and refreshing data."
    }
    return [suggestions.get(s, f"Learn the fundamentals of {s.title()} and build a small project that demonstrates it.") for s in missing]

# Styling
st.markdown("""
<style>
.block-container {padding-top: 2rem; padding-bottom: 3rem; max-width: 1180px;}
.hero {padding: 1.5rem 1.7rem; border: 1px solid #e5e7eb; border-radius: 18px; background: linear-gradient(120deg,#f8fbff,#ffffff);}
.eyebrow {color:#2563eb; font-size:.82rem; font-weight:700; letter-spacing:.12em; text-transform:uppercase;}
.hero h1 {margin:.25rem 0 .45rem 0; font-size:2.55rem; color:#111827;}
.hero p {color:#4b5563; font-size:1.05rem; margin-bottom:0;}
.small-note {color:#6b7280; font-size:.88rem;}
.skill-chip {display:inline-block; padding:5px 10px; margin:3px; border-radius:999px; font-size:.86rem; background:#eff6ff; color:#1d4ed8; border:1px solid #dbeafe;}
.missing-chip {display:inline-block; padding:5px 10px; margin:3px; border-radius:999px; font-size:.86rem; background:#fff7ed; color:#9a3412; border:1px solid #fed7aa;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <div class="eyebrow">Career clarity starts here</div>
  <h1>CareerMatch 🎯</h1>
  <p>Compare your resume with a job description, uncover skill gaps, and plan your next learning steps.</p>
</div>
""", unsafe_allow_html=True)
st.write("")

with st.sidebar:
    st.header("How it works")
    st.markdown("1. Add your resume text or upload a PDF.\n2. Paste the job description.\n3. Review matched skills and gaps.")
    st.divider()
    st.caption("Privacy first: this starter app processes your text in the current app session and does not intentionally save resumes to a database.")
    st.caption("Note: the score is a keyword-based estimate, not a hiring prediction.")

left, right = st.columns([1, 1], gap="large")
with left:
    st.subheader("1. Your resume")
    uploaded = st.file_uploader("Upload resume (PDF)", type=["pdf"])
    resume_text = st.text_area("Or paste resume text", height=260, placeholder="Paste your resume content here...")
    if uploaded:
        try:
            extracted = extract_pdf(uploaded)
            if extracted:
                st.success("PDF text extracted. You can review or edit it in the text box below.")
                resume_text = st.text_area("Extracted resume text (editable)", value=extracted, height=220, key="pdf_resume_text")
            else:
                st.warning("No selectable text was found in this PDF. Try copying the resume text into the box.")
        except Exception as exc:
            st.error(f"Could not read this PDF: {exc}. You can paste the resume text instead.")

with right:
    st.subheader("2. Target job")
    job_title = st.text_input("Job title (optional)", placeholder="e.g., Data Analyst Intern")
    job_text = st.text_area("Paste job description", height=330, placeholder="Paste the responsibilities, requirements, and skills from the job posting...")

analyze = st.button("Analyze my match", type="primary", use_container_width=True)

if analyze:
    if not resume_text.strip() or not job_text.strip():
        st.error("Please add both resume content and a job description before analyzing.")
    else:
        resume_skills = find_skills(resume_text)
        job_skills = find_skills(job_text)
        matched = sorted(resume_skills & job_skills)
        missing = sorted(job_skills - resume_skills)
        extra = sorted(resume_skills - job_skills)
        score = round(100 * len(matched) / len(job_skills)) if job_skills else 0

        st.divider()
        st.subheader("Your results" + (f" — {job_title}" if job_title else ""))
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Estimated match", f"{score}%")
        c2.metric("Matched skills", len(matched))
        c3.metric("Skills to build", len(missing))
        c4.metric("Resume skills found", len(resume_skills))
        st.progress(score / 100 if job_skills else 0)
        st.caption("Match score = matched detected job skills ÷ all detected job skills. It does not measure experience depth, achievements, communication, or overall candidate quality.")

        tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Matched skills", "Skill gaps", "Resume insights"])
        with tab1:
            if not job_skills:
                st.info("No skills from the built-in skill list were detected in the job description. Try including the job's technical requirements or expand the skill list in app.py.")
            else:
                st.markdown("**What this means**")
                if score >= 75:
                    st.write("Many of the detected skills overlap. Tailor your resume to clearly demonstrate them with projects and measurable outcomes.")
                elif score >= 45:
                    st.write("You have some relevant detected skills. Focus your learning plan on the missing requirements most important to this role.")
                else:
                    st.write("There are several detected skill gaps. Choose a few high-priority requirements and build a small project to demonstrate them.")
                st.markdown("**Detected job skills by category**")
                category_counts = Counter(category_for(s) for s in job_skills)
                if category_counts:
                    df = pd.DataFrame([{"Category": k, "Skills detected": v} for k, v in category_counts.items()])
                    st.bar_chart(df.set_index("Category"))
        with tab2:
            if matched:
                st.markdown("".join(f'<span class="skill-chip">{s.title()}</span>' for s in matched), unsafe_allow_html=True)
            else:
                st.info("No matching skills detected yet. Check whether your resume uses different wording.")
        with tab3:
            if missing:
                st.markdown("".join(f'<span class="missing-chip">{s.title()}</span>' for s in missing), unsafe_allow_html=True)
                st.markdown("**Suggested learning roadmap**")
                for i, (skill, suggestion) in enumerate(zip(missing, roadmap_for(missing)), start=1):
                    st.markdown(f"**{i}. {skill.title()}** — {suggestion}")
            else:
                st.success("All detected job-description skills also appear in your resume. Check that your resume proves them with examples.")
        with tab4:
            st.markdown(f"- **Detected skills in resume:** {len(resume_skills)}")
            st.markdown(f"- **Detected skills in job description:** {len(job_skills)}")
            st.markdown(f"- **Additional resume skills:** {len(extra)}")
            if extra:
                st.write(", ".join(s.title() for s in extra))
            st.markdown("**Improvement checklist**")
            checklist = [
                "Use the same truthful terminology as the job description when it accurately describes your skills.",
                "Add project bullets that explain what you built, which tools you used, and the result.",
                "Prioritize the missing skills that appear repeatedly or are listed as required.",
                "Never add a skill to your resume unless you can explain or demonstrate it."
            ]
            for item in checklist:
                st.checkbox(item, key="check_" + str(checklist.index(item)))

        export = pd.DataFrame({
            "Skill": sorted(job_skills),
            "Status": ["Matched" if s in resume_skills else "Gap to build" for s in sorted(job_skills)],
            "Category": [category_for(s) for s in sorted(job_skills)]
        })
        st.download_button("Download skill analysis (CSV)", data=export.to_csv(index=False).encode("utf-8"), file_name="careermatch_skill_analysis.csv", mime="text/csv")

st.divider()
st.markdown('<p class="small-note">CareerMatch is a learning and resume-tailoring aid. It does not guarantee interview calls or hiring outcomes. Always review the results and keep your resume accurate.</p>', unsafe_allow_html=True)
