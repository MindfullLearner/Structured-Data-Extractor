# Structured Data Extractor

A Python application that extracts structured information from job postings using Google's Gemini API, native structured output, and Pydantic validation.

## Features

- Extracts job titles, companies, locations, skills, experience, work arrangements, employment types, salaries, and application deadlines.
- Uses Gemini's native structured output rather than regex-based JSON parsing.
- Validates extracted data using a Pydantic schema.
- Retries once when the returned data fails Pydantic validation.
- Represents missing optional information as `null`.
- Distinguishes single salary amounts from salary ranges and records salary periods and estimated amounts.
- Includes five varied job-posting test cases.

## Tech Stack

- Python
- Google Gemini API (`google-genai`)
- Pydantic
- python-dotenv

## Project Structure

```text
Structured-Data-Extractor/
├── schema.py
├── extractor.py
├── test_schema.py
├── test_extractor.py
├── test_retry.py
├── run_test_cases.py
├── requirements.txt
├── .gitignore
├── .env
└── test_cases/
    ├── inputs/
    │   ├── job_01_complete.txt
    │   ├── job_02_internship.txt
    │   ├── job_03_senior_remote.txt
    │   ├── job_04_incomplete.txt
    │   └── job_05_ambiguous.txt
    └── outputs/
        ├── job_01_complete.json
        ├── job_02_internship.json
        ├── job_03_senior_remote.json
        ├── job_04_incomplete.json
        └── job_05_ambiguous.json
```

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/MindfullLearner/Structured-Data-Extractor.git
cd Structured-Data-Extractor
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure the API key

Create a `.env` file in the project root:

```text
GEMINI_API_KEY=your_api_key_here
```

Replace the placeholder with your own Gemini API key. Never commit `.env` or publish your API key.

## Usage

Call the extraction function from Python:

```python
from extractor import extract_job_posting

job_text = """
We are hiring a Python Developer.
Required skills: Python, SQL, and Django.
The position is fully remote.
"""

job = extract_job_posting(job_text)
print(job.model_dump_json(indent=2))
```

## Testing

Run schema validation tests:

```powershell
python test_schema.py
```

Test the validation-retry behavior using a mocked response:

```powershell
python test_retry.py
```

Run extraction against all five sample job postings:

```powershell
python run_test_cases.py
```

The batch runner saves the extracted JSON files in `test_cases/outputs/`.

## Validation and Retry Behavior

The extractor uses Gemini's structured output capability to produce data conforming to the `JobPosting` schema. Pydantic validates the returned values, including allowed categories and salary constraints.

If a response reaches Pydantic validation and fails, the extractor adds the validation errors to the prompt and retries once. If the second validation attempt also fails, the error is raised.

The retry test mocks the model responses to verify that the retry logic works without relying on a real API failure.

## Limitations

- Extraction quality depends on the source text and model response.
- Missing information is not guaranteed to be inferred.
- Passing schema validation does not guarantee factual accuracy.
- Salary normalization can be ambiguous when the posting uses vague or incomplete wording.

## Future Improvements

- Add more job-posting samples and edge cases.
- Improve salary normalization and handling of ambiguous compensation.
- Add automated test coverage with pytest.
- Add structured logging and clearer API error handling.
