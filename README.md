# CareerMatch 🎯

CareerMatch is a beginner-friendly resume and job-description analyzer built with Python and Streamlit. It identifies technical skills in both texts, estimates a keyword overlap score, highlights missing skills, and suggests learning next steps.

## Features
- Paste resume text or upload a text-based PDF
- Paste a target job description
- Estimated skill overlap score and summary metrics
- Matched skills, missing skills, and additional resume skills
- Skill-gap learning suggestions
- Download results as CSV
- No paid API required

## Run locally (Windows PowerShell)

1. Install Python 3.11 or 3.12 from https://www.python.org/downloads/ if you do not already have a compatible version.
2. Extract this project folder.
3. Open PowerShell in the `CareerMatch` folder.
4. Create and activate a virtual environment:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run this in the current terminal:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

5. Install packages:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

6. Start the app:

```powershell
streamlit run app.py
```

Streamlit will open CareerMatch in your browser.

## How the score works

The starter version detects skills from a built-in keyword list. The estimated match score is:

`matched detected job skills / all detected job skills * 100`

This is not an ATS score or a hiring prediction. It does not assess proficiency, years of experience, project quality, context, or soft skills. Keyword matching can miss synonyms and skills not included in the taxonomy.

## Customize the skill list

Open `app.py` and add skills to `SKILL_CATEGORIES`. Add learning suggestions in `roadmap_for()` when you want more tailored recommendations.

## Suggested next improvements
1. Add a curated skills dictionary for specific roles (Data Analyst, Data Scientist, Web Developer).
2. Add synonyms and phrase normalization.
3. Add an option to compare multiple job descriptions.
4. Add tests for the scoring logic.
5. Deploy on Streamlit Community Cloud after checking the platform's current privacy and deployment requirements.

## Privacy note

Do not upload confidential or sensitive resumes to a public demo. This starter app does not intentionally store resume content in a database, but hosting providers and deployment configurations may process logs or uploaded files. Review the deployment platform's policies before using real personal data.
