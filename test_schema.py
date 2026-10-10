
from pydantic import ValidationError

from schema import JobPosting


# Test 1: Valid data
job = JobPosting(
    job_title="Python Developer",
    location="Islamabad, Pakistan",
    required_skills=["Python", "Django", "SQL"],
    salary_min=80000,
    salary_max=120000,
    salary_currency="PKR",
    work_type="Remote",
)

print("Valid job:")
print(job.model_dump(mode="json", exclude_none=False))


# Test 2: Invalid salary range
try:
    JobPosting(
        job_title="Python Developer",
        salary_min=120000,
        salary_max=80000,
    )
except ValidationError as error:
    print("\nSalary validation worked:")
    print(error)


# Test 3: Invalid work category
try:
    JobPosting(
        job_title="Python Developer",
        work_type="Work from home",
    )
except ValidationError as error:
    print("\nCategory validation worked:")
    print(error)

def test_estimated_single_salary():
    job = JobPosting(
        job_title="Data Analyst",
        salary_amount=150000,
        salary_period="Monthly",
        salary_is_estimated=True,
        salary_currency="PKR",
    )

    assert job.salary_amount == 150000
    assert job.salary_period == "Monthly"
    assert job.salary_is_estimated is True
    assert job.salary_min is None
    assert job.salary_max is None

    print("Estimated single salary validation worked.")
if __name__ == "__main__":
    test_estimated_single_salary()