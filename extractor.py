
import os

from dotenv import load_dotenv
from google import genai
from pydantic import ValidationError

from schema import JobPosting


# Load the API key from the local .env file.
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY is missing. Check your .env file."
    )

client = genai.Client(api_key=api_key)

MODEL_NAME = "gemini-3.8-flash"



def extract_job_posting(job_text: str) -> JobPosting:
    """Extract job information and retry once on validation failure."""

    if not job_text.strip():
        raise ValueError("Job description cannot be empty.")

    prompt = f"""
    Extract job posting information from the text below.

    Rules:
    - Use only information supported by the supplied text.
    - Do not invent missing details.
    - Use None for unknown optional values.
    - Use an empty list if no required skills are stated.
    - Normalize categories to the allowed values in the schema.
    - Convert salary amounts to integers when possible.
    - Convert experience requirements to years when possible.
    - If a value cannot be reliably determined, leave it unknown.

    JOB DESCRIPTION:
    {job_text}
    """

    # Initial attempt + one retry = at most two API calls.
    for attempt in range(2):
        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt,
                config={
                    "response_mime_type": "application/json",
                    "response_schema": JobPosting,
                },
            )

            if isinstance(response.parsed, JobPosting):
                return response.parsed

            if response.parsed is not None:
                return JobPosting.model_validate(response.parsed)

            if response.text:
                return JobPosting.model_validate_json(response.text)

            raise ValueError("Gemini returned no usable response.")

        except ValidationError as error:
            # If this was the retry, don't make another API call.
            if attempt == 1:
                raise

            # Give Gemini the validation feedback for its retry.
            prompt += f"""

            Your previous response failed Pydantic validation.
            Validation errors:
            {error}

            Correct the output to satisfy the supplied schema.
            Use only evidence from the original job description.
            Do not invent missing information.
            Return the corrected structured output.
            """

    raise RuntimeError("Job extraction failed unexpectedly.")
