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

CODEX_PROVIDER_CONFIG = [
    "-c",
    'model_provider="iapiboxcode"',
    "-c",
    'model="gpt-5.5"',
    "-c",
    'model_reasoning_effort="high"',
    "-c",
    'network_access="enabled"',
    "-c",
    'disable_response_storage=true',
    "-c",
    'windows_wsl_setup_acknowledged=true',
    "-c",
    'model_verbosity="high"',
    "-c",
    'model_providers.iapiboxcode.name="iapiboxcode"',
    "-c",
    'model_providers.iapiboxcode.base_url="https://www.iapibox.com/t/iapiboxcode/v1"',
    "-c",
    'model_providers.iapiboxcode.wire_api="responses"',
    "-c",
    'model_providers.iapiboxcode.requires_openai_auth=true',
]


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
        *CODEX_PROVIDER_CONFIG,
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
    auth_key = env.get("IAPIBOX_API_KEY") or env.get("OPENAI_API_KEY")
    if auth_key:
        login = subprocess.run(
            ["codex", "login", "--with-api-key"],
            input=auth_key.encode("utf-8"),
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
