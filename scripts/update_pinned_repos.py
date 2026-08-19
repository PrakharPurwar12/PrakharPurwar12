"""
Fetches the authenticated user's top repositories (by stars, then last-updated)
and writes a markdown table into README.md between the
<!--START_SECTION:pinned-repos--> / <!--END_SECTION:pinned-repos--> markers.

Runs inside GitHub Actions where GITHUB_TOKEN and GITHUB_REPOSITORY are
already set as environment variables — no manual configuration needed.
"""

import os
import re
import sys
import urllib.request
import json

START_MARKER = "<!--START_SECTION:pinned-repos-->"
END_MARKER = "<!--END_SECTION:pinned-repos-->"
README_PATH = "README.md"
MAX_REPOS = 6


def get_username():
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    if "/" in repo:
        return repo.split("/")[0]
    print("Could not determine GitHub username from GITHUB_REPOSITORY.")
    sys.exit(1)


def fetch_repos(username, token):
    url = f"https://api.github.com/users/{username}/repos?per_page=100&sort=updated"
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", "readme-updater-script")
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())


def build_table(repos):
    # Skip forks, skip the special profile repo itself, sort by stars desc.
    filtered = [
        r for r in repos
        if not r.get("fork")
        and r.get("name", "").lower() != os.environ.get("GITHUB_REPOSITORY", "").split("/")[-1].lower()
    ]
    filtered.sort(key=lambda r: (r.get("stargazers_count", 0), r.get("updated_at", "")), reverse=True)
    top = filtered[:MAX_REPOS]

    if not top:
        return "No public repositories found yet — push some code and re-run this workflow!"

    header = "| Repository | ⭐ Stars | 🍴 Forks | Language | Last Updated |\n"
    header += "|---|---|---|---|---|\n"
    rows = []
    for r in top:
        name = r["name"]
        url = r["html_url"]
        stars = r.get("stargazers_count", 0)
        forks = r.get("forks_count", 0)
        lang = r.get("language") or "—"
        updated = r.get("updated_at", "")[:10]
        rows.append(f"| [{name}]({url}) | {stars} | {forks} | {lang} | {updated} |")

    return header + "\n".join(rows)


def update_readme(table_md):
    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    pattern = re.compile(
        re.escape(START_MARKER) + r".*?" + re.escape(END_MARKER),
        re.DOTALL,
    )
    replacement = f"{START_MARKER}\n{table_md}\n{END_MARKER}"

    if not pattern.search(content):
        print("Markers not found in README.md — nothing updated.")
        return

    new_content = pattern.sub(replacement, content)

    if new_content != content:
        with open(README_PATH, "w", encoding="utf-8") as f:
            f.write(new_content)
        print("README.md pinned-repos section updated.")
    else:
        print("No changes to pinned-repos section.")


def main():
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("GITHUB_TOKEN not set.")
        sys.exit(1)

    username = get_username()
    repos = fetch_repos(username, token)
    table_md = build_table(repos)
    update_readme(table_md)


if __name__ == "__main__":
    main()
