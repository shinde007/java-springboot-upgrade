import argparse
import subprocess
from pathlib import Path


DEFAULT_TITLE_PREFIX = "Java Spring Boot Upgrade Planning"


def detect_local_repo():
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
    Load issue template content.
    """

    with open("issue_template.md", "r", encoding="utf-8") as file:
        return file.read()


def generate_issue(repo_name):
    """
    Generate issue title and body.
    """

    title = f"{DEFAULT_TITLE_PREFIX} - {repo_name}"

    body = load_template()

    return title, body


def print_summary(repo_name):
    """
    Print execution summary.
    """

    print("\n" + "=" * 60)
    print("Java Spring Boot Upgrade Planning Generator")
    print("=" * 60)

    print(f"\nTarget Repository : {repo_name}")


def print_issue(title, body):
    """
    Print generated issue.
    """

    print(f"\nIssue Title:\n{title}")

    print("\nIssue Body:\n")
    print(body)

    print("\n" + "=" * 60)
    print("Dry run completed successfully")
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="Generate Java Spring Boot upgrade planning issues"
    )

    parser.add_argument(
        "--repo",
        type=str,
        help="Target GitHub repository (owner/repo)"
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print generated issue without creating it"
    )

    args = parser.parse_args()

    if args.repo:
        repo_name = args.repo
    else:
        repo_name = detect_local_repo()

    print_summary(repo_name)

    title, body = generate_issue(repo_name)

    print_issue(title, body)


if __name__ == "__main__":
    main()