
from extractor import extract_job_posting


sample_job = """
We are hiring a Junior Python Developer at TechNova.
Location: Islamabad, Pakistan.
Required skills: Python, SQL, Django, Git.
Experience: 1 year.
Work arrangement: Remote.
Employment type: Full-time.
Salary: PKR 80,000 to PKR 120,000 per month.
"""


job = extract_job_posting(sample_job)

print("\nExtracted Job Posting:")
print(job.model_dump_json(indent=2))
