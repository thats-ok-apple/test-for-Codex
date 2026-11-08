#!/usr/bin/env python3
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RESEARCH_DIR = ROOT / "codex-research"
DAILY = RESEARCH_DIR / "daily-log.md"
WEEKLY = RESEARCH_DIR / "weekly-digest.md"


def main() -> None:
    if not DAILY.exists():
        raise SystemExit(f"Missing file: {DAILY}")

    content = DAILY.read_text(encoding="utf-8").strip()
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    report = f"""# Weekly Digest\n\n生成时间（UTC）：{today}\n\n## 本周新增原始记录\n\n{content}\n\n## 本周可执行方法（手动补充）\n\n- [ ] 方法 1\n- [ ] 方法 2\n- [ ] 方法 3\n\n## 下周行动清单\n\n- [ ] 持续跟踪 3 位高质量创作者\n- [ ] 提炼 2 个可落地工作流\n- [ ] 新增 1 个端到端案例复盘\n"""

    WEEKLY.write_text(report, encoding="utf-8")
    print(f"Generated: {WEEKLY}")


if __name__ == "__main__":
    main()
