# Codex GitHub 热门资料自动化

这个目录用于每天自动搜集 GitHub 上与 Codex 相关的热门使用教程、方法和案例，并按日期整理成 Markdown 日报。

## 自动化内容

- **运行时间**：每天 12:00 UTC。
- **数据来源**：GitHub Search API。
- **排序方式**：按仓库星标数排序，兼顾最近更新时间。
- **输出位置**：`codex-github-digest/digests/YYYY-MM-DD.md`。
- **分组维度**：教程、方法、案例。

## 手动运行

```bash
python3 codex-github-digest/scripts/collect_codex_digest.py
```

生成指定日期日报：

```bash
python3 codex-github-digest/scripts/collect_codex_digest.py --date 2026-05-29
```

## GitHub Actions

自动化工作流位于 `.github/workflows/codex-github-digest.yml`。工作流会在生成日报后自动提交变更到当前分支。
