from __future__ import annotations

import json
import os
import sys
import urllib.request
from pathlib import Path


def main() -> int:
    issue_number = os.getenv("REPORT_ISSUE_NUMBER", "").strip()
    token = os.getenv("GITHUB_TOKEN", "").strip()
    repo = os.getenv("GITHUB_REPOSITORY", "").strip()

    if not issue_number:
        return 0
    if not token or not repo:
        raise RuntimeError("缺少 GITHUB_TOKEN 或 GITHUB_REPOSITORY")

    body_path = Path("outputs/latest.md")
    if not body_path.exists():
        raise RuntimeError("找不到 outputs/latest.md")

    body = body_path.read_text(encoding="utf-8")
    payload = json.dumps({"body": body[:60000]}).encode("utf-8")
    url = f"https://api.github.com/repos/{repo}/issues/{issue_number}/comments"
    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        if resp.status >= 300:
            raise RuntimeError(f"GitHub API 返回状态码 {resp.status}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

