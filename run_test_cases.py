
import json
from pathlib import Path

from pydantic import ValidationError

from extractor import extract_job_posting


# Project directories
PROJECT_DIR = Path(__file__).resolve().parent
INPUT_DIR = PROJECT_DIR / "test_cases" / "inputs"
OUTPUT_DIR = PROJECT_DIR / "test_cases" / "outputs"


def main():
    # Create the output folder if it doesn't exist.
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Find all job description text files.
    input_files = sorted(INPUT_DIR.glob("*.txt"))

    if not input_files:
        print(f"No input files found in: {INPUT_DIR}")
        return

    passed = 0
    failed = 0

    for input_file in input_files:
        print(f"\nProcessing: {input_file.name}")

        try:
            job_text = input_file.read_text(encoding="utf-8")

            # Extract and validate the job posting.
            job = extract_job_posting(job_text)

            # Convert the validated model to a JSON-compatible dictionary.
            result = job.model_dump(mode="json")

            # Save the extracted data as a JSON file.
            output_file = OUTPUT_DIR / f"{input_file.stem}.json"

            output_file.write_text(
                json.dumps(result, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )

            print(f"PASS: {input_file.name}")
            print(f"Saved: {output_file.relative_to(PROJECT_DIR)}")
            passed += 1

        except (ValidationError, ValueError) as error:
            print(f"FAIL: {input_file.name}")
            print(f"Reason: {error}")
            failed += 1

        except Exception as error:
            print(f"ERROR: {input_file.name}")
            print(f"Reason: {error}")
            failed += 1

    print("\n" + "=" * 40)
    print(f"Total: {len(input_files)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print("=" * 40)


if __name__ == "__main__":
    main()
