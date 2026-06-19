from __future__ import annotations

import datetime as dt
import os
import subprocess
import sys
from pathlib import Path
from tomllib import load as load_toml


ROOT = Path(__file__).resolve().parents[1]
AUTOMATION = ROOT / "automation.toml"
OUTPUT_DIR = ROOT / "outputs"


def read_prompt() -> str:
    with AUTOMATION.open("rb") as f:
        data = load_toml(f)
    prompt = data.get("prompt")
    if not isinstance(prompt, str) or not prompt.strip():
        raise RuntimeError("automation.toml 缺少 prompt")
    return prompt


def ensure_output_dir() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def main() -> int:
    ensure_output_dir()
    prompt = read_prompt()
    today = dt.datetime.now().strftime("%Y-%m-%d")
    last_message = OUTPUT_DIR / "latest.md"

    cmd = [
        "codex",
        "--search",
        "--sandbox",
        "workspace-write",
        "--cd",
        str(ROOT),
        "exec",
        "--output-last-message",
        str(last_message),
        prompt,
    ]

    env = os.environ.copy()
    if env.get("OPENAI_API_KEY"):
        login = subprocess.run(
            ["codex", "login", "--with-api-key"],
            input=env["OPENAI_API_KEY"].encode("utf-8"),
            cwd=str(ROOT),
            env=env,
            check=False,
        )
        if login.returncode != 0:
            raise RuntimeError("codex login --with-api-key 失败")

    proc = subprocess.run(cmd, cwd=str(ROOT), env=env, check=False)
    if proc.returncode != 0:
        return proc.returncode

    dated = OUTPUT_DIR / f"{today}.md"
    if last_message.exists():
        dated.write_text(last_message.read_text(encoding="utf-8"), encoding="utf-8")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
