#!/usr/bin/env python3
"""Validate the portable structure of the security-research skill package."""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_RULES = [f"{index:02d}-{name}.md" for index, name in enumerate([
    "core",
    "safety-boundary",
    "blackbox-workflow",
    "whitebox-workflow",
    "target-discovery",
    "testing-policy",
    "reporting",
    "tool-routing",
])]


def check_required_files(errors: list[str]) -> None:
    for relative in ["AGENTS.md", "REFACTOR_AUDIT.md", "skills/skill/SKILL.md", "skills/skill/ROUTER.md"]:
        if not (ROOT / relative).is_file():
            errors.append(f"缺少必需文件: {relative}")
    for name in REQUIRED_RULES:
        if not (ROOT / "rules" / name).is_file():
            errors.append(f"缺少分层规则: rules/{name}")
    for name in ["blackbox-src.md", "whitebox-audit.md", "discovery-target.md", "scoped-target.md"]:
        if not (ROOT / "skills/skill/workflows" / name).is_file():
            errors.append(f"缺少工作流入口: skills/skill/workflows/{name}")


def check_names(errors: list[str]) -> None:
    for path in ROOT.rglob("*"):
        if "#U" in path.name:
            errors.append(f"发现编码转义文件名: {path.relative_to(ROOT)}")
    runtime = sorted(path.name for path in (ROOT / "rules").glob("*.md"))
    if runtime != sorted(REQUIRED_RULES):
        errors.append(f"rules/ 应仅包含 00-07 运行时规则，实际为: {runtime}")


def check_links(errors: list[str]) -> None:
    pattern = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
    for path in ROOT.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        for raw in pattern.findall(text):
            target = raw.strip().strip("<>").split("#", 1)[0]
            if not target or target.startswith(("http://", "https://", "mailto:", "~", "/")):
                continue
            # Ignore inline-code payloads that happen to contain brackets and
            # links in extracted vendor docs whose source is not bundled.
            if not ("/" in target or target.endswith((".md", ".txt", ".toml", "LICENSE"))):
                continue
            if target == "LICENSE" and path.parts[-3:-1] == ("mcp-servers", "fofa_MCP"):
                continue
            if target.startswith("'/") or target.startswith('"/'):
                continue
            if "docs/user-guide/" in str(path) and target.startswith("../internal/"):
                continue
            candidate = (path.parent / target).resolve()
            if not candidate.is_file():
                errors.append(f"失效 Markdown 引用: {path.relative_to(ROOT)} -> {raw}")


def check_duplicates(errors: list[str]) -> None:
    hashes: dict[str, Path] = {}
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts or path.name == "uv.lock":
            continue
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        previous = hashes.get(digest)
        if previous:
            errors.append(f"发现重复文件内容: {previous.relative_to(ROOT)} == {path.relative_to(ROOT)}")
        else:
            hashes[digest] = path


def check_skill_size(errors: list[str]) -> None:
    path = ROOT / "skills/skill/SKILL.md"
    lines = path.read_text(encoding="utf-8").splitlines()
    if len(lines) > 120:
        errors.append(f"SKILL.md 仍过长: {len(lines)} 行（上限 120）")


def check_knowledge_index(errors: list[str]) -> None:
    knowledge = ROOT / "skills/skill/知识库"
    actual = {path.name for path in knowledge.glob("*.md")} - {"README.md"}
    if len(actual) != 48:
        errors.append(f"知识库文件数量变化: 期望 48，实际 {len(actual)}")
    readme = (knowledge / "README.md").read_text(encoding="utf-8")
    if "**合计：48 个知识文件**" not in readme:
        errors.append("知识库 README 未声明 48 个知识文件")


def main() -> int:
    errors: list[str] = []
    check_required_files(errors)
    check_names(errors)
    check_links(errors)
    check_duplicates(errors)
    check_skill_size(errors)
    check_knowledge_index(errors)
    if errors:
        print("结构检查失败:")
        print("\n".join(f"- {error}" for error in errors))
        return 1
    print("结构检查通过: rules、工作流、知识库、引用、重复文件和入口大小均符合要求。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
