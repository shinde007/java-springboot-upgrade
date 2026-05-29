import argparse
import os
import subprocess
from pathlib import Path

from github import Github


DEFAULT_TITLE_PREFIX = "Spring Boot Upgrade Planning"


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
    print("Spring Boot Upgrade Planning Generator")
    print("=" * 60)

    print(f"\nTarget Repository : {repo_name}")


def create_github_issue(repo_name, title, body):
    """
    Create GitHub issue.
    """

    token = os.getenv("GITHUB_TOKEN")

    if not token:
        raise Exception(
            "GITHUB_TOKEN environment variable not found"
        )

    github_client = Github(token)

    repository = github_client.get_repo(repo_name)

    issue = repository.create_issue(
        title=title,
        body=body
    )

    return issue.html_url


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
        description="Generate Spring Boot upgrade planning issues"
    )

    parser.add_argument(
        "--repo",
        type=str,
        required=True,
        help="Target GitHub repository (owner/repo)"
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print generated issue without creating it"
    )

    args = parser.parse_args()

    repo_name = args.repo

    print_summary(repo_name)

    title, body = generate_issue(repo_name)

    if args.dry_run:
        print_issue(title, body)

    else:
        issue_url = create_github_issue(
            repo_name,
            title,
            body
        )

        print("\nIssue created successfully")
        print(issue_url)


if __name__ == "__main__":
    main()