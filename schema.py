from pydantic import BaseModel, Field, field_validator, model_validator
from datetime import date
from typing import Literal

from pydantic import BaseModel, Field, model_validator


class JobPosting(BaseModel):
    # Job title is required and cannot be blank.
    job_title: str = Field(min_length=1)
    
    # Optional information
    company: str | None = None
    location: str | None = None

    # Skills can contain zero or more items.
    required_skills: list[str] = Field(default_factory=list)

    # Standardized categories
    experience_level: Literal[
        "Internship",
        "Entry-level",
        "Junior",
        "Mid-level",
        "Senior",
        "Lead",
    ] | None = None

    min_experience_years: float | None = Field(default=None, ge=0)

    work_type: Literal["Remote", "On-site", "Hybrid"] | None = None

    employment_type: Literal[
        "Full-time",
        "Part-time",
        "Contract",
        "Internship",
        "Temporary",
    ] | None = None
    
    salary_amount: int | None = Field(default=None, ge=0)

    salary_period: Literal[
        "Hourly",
        "Monthly",
        "Annual",
    ] | None = None

    salary_is_estimated: bool | None = None

    # Salary fields
    salary_min: int | None = Field(default=None, ge=0)
    salary_max: int | None = Field(default=None, ge=0)
    salary_currency: str | None = Field(
        default=None,
        pattern=r"^[A-Z]{3}$",
    )

    # Optional application deadline
    application_deadline: date | None = None

    @model_validator(mode="after")
    def validate_salary_range(self):
        if (
            self.salary_min is not None
            and self.salary_max is not None
            and self.salary_max < self.salary_min
        ):
            raise ValueError(
                "salary_max cannot be less than salary_min"
            )

        return self
    @field_validator("job_title")
    @classmethod
    def validate_job_title(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("job_title cannot be blank")

        return value
