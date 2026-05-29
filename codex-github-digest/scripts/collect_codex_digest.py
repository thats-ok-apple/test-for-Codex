#!/usr/bin/env python3
"""Collect popular GitHub Codex tutorials, methods, and examples into a daily digest."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
DIGEST_DIR = ROOT / "codex-github-digest" / "digests"
INDEX_FILE = DIGEST_DIR / "README.md"

CATEGORIES: dict[str, list[str]] = {
    "教程": [
        "openai codex tutorial in:name,description,readme archived:false",
        "codex cli tutorial in:name,description,readme archived:false",
        "codex guide in:name,description,readme archived:false",
    ],
    "方法": [
        "openai codex best practices in:name,description,readme archived:false",
        "codex prompt engineering in:name,description,readme archived:false",
        "codex workflow in:name,description,readme archived:false",
    ],
    "案例": [
        "openai codex examples in:name,description,readme archived:false",
        "codex demo in:name,description,readme archived:false",
        "codex agent example in:name,description,readme archived:false",
    ],
}


def github_get(path: str, token: str | None) -> dict[str, Any]:
    url = "https://api.github.com" + path
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "codex-github-digest-bot",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    request = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"GitHub API request failed: {exc.code} {url}\n{body}") from exc


def search_repositories(query: str, token: str | None, per_page: int) -> list[dict[str, Any]]:
    params = urllib.parse.urlencode(
        {
            "q": query,
            "sort": "stars",
            "order": "desc",
            "per_page": per_page,
        }
    )
    data = github_get(f"/search/repositories?{params}", token)
    return data.get("items", [])


def collect(token: str | None, per_query: int, category_limit: int, sleep_seconds: float) -> dict[str, list[dict[str, Any]]]:
    results: dict[str, list[dict[str, Any]]] = {}
    for category, queries in CATEGORIES.items():
        seen: set[int] = set()
        repos: list[dict[str, Any]] = []
        for query in queries:
            for repo in search_repositories(query, token, per_query):
                repo_id = repo["id"]
                if repo_id in seen:
                    continue
                seen.add(repo_id)
                repos.append(repo)
            if sleep_seconds:
                time.sleep(sleep_seconds)
        repos.sort(key=lambda item: (item.get("stargazers_count", 0), item.get("updated_at", "")), reverse=True)
        results[category] = repos[:category_limit]
    return results


def repo_line(repo: dict[str, Any]) -> str:
    description = (repo.get("description") or "暂无描述").replace("\n", " ").strip()
    language = repo.get("language") or "未知语言"
    stars = repo.get("stargazers_count", 0)
    forks = repo.get("forks_count", 0)
    updated = repo.get("updated_at", "")[:10] or "未知"
    return (
        f"- [{repo['full_name']}]({repo['html_url']}) — {description}"
        f"\n  - ⭐ {stars} · Forks {forks} · {language} · 最近更新 {updated}"
    )


def render_digest(results: dict[str, list[dict[str, Any]]], run_date: dt.date) -> str:
    generated_at = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    lines = [
        f"# Codex GitHub 热门资料日报 - {run_date.isoformat()}",
        "",
        f"> 自动生成时间：{generated_at}。排序依据为 GitHub 仓库星标数，并按教程、方法、案例分组。",
        "",
        "## 摘要",
        "",
    ]
    for category, repos in results.items():
        lines.append(f"- {category}：{len(repos)} 个仓库")
    lines.append("")

    for category, repos in results.items():
        lines.extend([f"## {category}", ""])
        if repos:
            lines.extend(repo_line(repo) for repo in repos)
        else:
            lines.append("- 今日未检索到匹配仓库。")
        lines.append("")

    lines.extend(
        [
            "## 复现方式",
            "",
            "```bash",
            "python3 codex-github-digest/scripts/collect_codex_digest.py",
            "```",
            "",
            "可通过 `--date YYYY-MM-DD` 生成指定日期文件。",
        ]
    )
    return "\n".join(lines) + "\n"


def update_index(run_date: dt.date) -> None:
    entries = sorted(DIGEST_DIR.glob("*.md"), reverse=True)
    entries = [path for path in entries if path.name != "README.md"]
    lines = [
        "# Codex GitHub 热门资料日报索引",
        "",
        "这里保存自动化任务每天 12:00 UTC 从 GitHub 搜集的 Codex 热门教程、方法和案例。",
        "",
    ]
    if entries:
        lines.append("## 日报")
        lines.append("")
        for path in entries:
            lines.append(f"- [{path.stem}]({path.name})")
    else:
        lines.append("暂无日报。")
    lines.append("")
    INDEX_FILE.write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", default=dt.datetime.now(dt.timezone.utc).date().isoformat(), help="Digest date in YYYY-MM-DD format.")
    parser.add_argument("--per-query", type=int, default=10, help="Number of repositories to request for each GitHub search query.")
    parser.add_argument("--category-limit", type=int, default=10, help="Maximum repositories kept in each category.")
    parser.add_argument("--sleep", type=float, default=1.0, help="Seconds to sleep between GitHub Search API calls.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        run_date = dt.date.fromisoformat(args.date)
    except ValueError:
        print("--date must use YYYY-MM-DD", file=sys.stderr)
        return 2

    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    DIGEST_DIR.mkdir(parents=True, exist_ok=True)
    results = collect(token, args.per_query, args.category_limit, args.sleep)
    digest_path = DIGEST_DIR / f"{run_date.isoformat()}.md"
    digest_path.write_text(render_digest(results, run_date), encoding="utf-8")
    update_index(run_date)
    print(f"Wrote {digest_path.relative_to(ROOT)}")
    print(f"Updated {INDEX_FILE.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
