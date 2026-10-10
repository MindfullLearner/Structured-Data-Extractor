
from unittest.mock import patch, Mock
from pydantic import ValidationError

from extractor import extract_job_posting


sample_job = """
We are hiring a Python Developer at TechNova.
Required skills: Python and SQL.
Work arrangement: Remote.
"""


# First response: invalid work_type.
invalid_response = Mock()
invalid_response.parsed = {
    "job_title": "Python Developer",
    "work_type": "Work from home",
}
invalid_response.text = None

# Second response: valid work_type.
valid_response = Mock()
valid_response.parsed = {
    "job_title": "Python Developer",
    "company": "TechNova",
    "required_skills": ["Python", "SQL"],
    "work_type": "Remote",
}
valid_response.text = None

with patch(
    "extractor.client.models.generate_content",
    side_effect=[invalid_response, valid_response],
) as mocked_gemini:

    result = extract_job_posting(sample_job)

    print("Extracted result:")
    print(result.model_dump_json(indent=2))

    print("\nGemini calls:", mocked_gemini.call_count)

    assert result.job_title == "Python Developer"
    assert result.work_type == "Remote"
    assert mocked_gemini.call_count == 2

    print("\nPASS: validation failed first, then retry succeeded.")
