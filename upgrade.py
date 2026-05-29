import argparse
import subprocess
from pathlib import Path


def detect_repo_name():
    """
    Detect current git repository name.
    """

    try:
        repo_path = subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"],
            text=True
        ).strip()

        return Path(repo_path).name

    except Exception:
        return "unknown-repository"


def load_template():
    """
    Load issue template from file.
    """

    with open("issue_template.md", "r", encoding="utf-8") as file:
        return file.read()


def generate_issue(repo_name):
    """
    Generate issue title and body.
    """

    title = f"java Spring Boot Upgrade Planning - {repo_name}"

    body = load_template()

    return title, body


def print_issue(title, body):
    """
    Print generated issue.
    """

    print("\n" + "=" * 60)
    print("Generated GitHub Upgrade Planning Issue")
    print("=" * 60)

    print(f"\nTITLE:\n{title}")

    print(f"\nBODY:\n{body}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate Java Spring Boot upgrade planning issue"
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print issue instead of creating it"
    )

    args = parser.parse_args()

    repo_name = detect_repo_name()

    title, body = generate_issue(repo_name)

    print_issue(title, body)


if __name__ == "__main__":
    main()