#!/usr/bin/env python3
"""把 registry.yaml 的元数据同步进知识库文件的 YAML frontmatter，并修正失效引用。

单一元数据源：skills/skill/知识库/registry.yaml
产物：每个知识文件头部的规范 frontmatter + 正文中旧路径引用的修正。

幂等：重复运行不会产生新的改动。

用法：
    python3 tests/sync_knowledge_meta.py            # 写入
    python3 tests/sync_knowledge_meta.py --check    # 只检查，不写入
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    import yaml
except ModuleNotFoundError:  # pragma: no cover
    print("需要 pyyaml：pip install pyyaml", file=sys.stderr)
    raise SystemExit(2)

ROOT = Path(__file__).resolve().parents[1]
KNOWLEDGE = ROOT / "skills/skill/知识库"
REGISTRY = KNOWLEDGE / "registry.yaml"

# frontmatter 字段顺序（先规范字段，后保留的自定义字段）
FIELD_ORDER = [
    "id",
    "title",
    "category",
    "status",
    "last_reviewed",
    "purpose",
    "triggers",
    "inputs",
    "outputs",
    "related",
]
# 允许从原文件继承的额外字段
EXTRA_FIELDS = ["sources", "scope", "baseline"]

# 正文中旧路径 / 旧规则名 → 现行 rules 的映射（顺序敏感，先具体后宽泛）
REFERENCE_RULES: list[tuple[str, str]] = [
    (r"`?~/.grok/rules/vuln-report-format\.md`?", "`rules/06-reporting.md`"),
    (r"`?vuln-report-format\.md`?", "`rules/06-reporting.md`"),
    (r"`?vuln-report-format`?", "`rules/06-reporting.md`"),
    (r"`?~/.grok/rules/dig-scope-workflow\.md`?", "`rules/02-blackbox-workflow.md`"),
    (r"`dig-scope`\s*§4\.2(?:\.\d+)?", "`rules/05-testing-policy.md`"),
    (r"`dig-scope`\s*§[12](?:\.\d+)*", "`rules/04-target-discovery.md`"),
    (r"`dig-scope`\s*§4(?:\.\d+)?", "`rules/02-blackbox-workflow.md`"),
    (r"`dig-scope`\s*去废\s*/\s*去非存活\s*/\s*范围闸", "`rules/04-target-discovery.md`"),
    (r"`dig-scope`\s*一种子闭环", "`rules/04-target-discovery.md`"),
    (r"`?dig-scope-workflow\.md`?", "`rules/02-blackbox-workflow.md`"),
    (r"`?dig-scope`?", "`rules/02-blackbox-workflow.md`"),
    (r"`?src-value-hunting`?", "`rules/06-reporting.md`"),
    (r"`?hunt-iter\.md`?", "`rules/05-testing-policy.md`"),
    (r"`?hunt-iter`?", "`rules/05-testing-policy.md`"),
    (r"`?cors-vuln-report-priority\.md`?", "`rules/01-safety-boundary.md`"),
    (r"`?cors-vuln-report-priority`?", "`rules/01-safety-boundary.md`"),
    (r"`?anti-over-moralization\.md`?", "`rules/01-safety-boundary.md`"),
    (r"`?skill-as-boost\.md`?", "`rules/00-core.md`"),
    (r"`?security-research-context\.md`?", "`rules/00-core.md`"),
    (r"`?researcher-blackbox-whitebox\.md`?", "`rules/00-core.md`"),
    (r"`?desktop-task-folder\.md`?", "`rules/06-reporting.md`"),
    # 相对引用统一为仓库根相对路径
    (r"`?\.\./rules/(0[0-7]-[a-z-]+\.md)`?", r"`rules/\1`"),
]

# 元数据行（引用块形式）识别
META_LINE = re.compile(r"^>\s*(status|last_reviewed|scope|baseline)\s*[:：]\s*(.*?)\s*$")
FM_FENCE = "---"


def load_registry() -> dict:
    with REGISTRY.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def split_frontmatter(text: str) -> tuple[dict, str]:
    """拆出已有 YAML frontmatter；没有则返回 ({}, 原文)。切片无损，保证幂等。"""
    match = re.match(r"\A---[ \t]*\n(.*?)\n---[ \t]*(?:\n|\Z)", text, re.S)
    if not match:
        return {}, text
    try:
        data = yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError:
        return {}, text
    body = text[match.end():]
    return (data if isinstance(data, dict) else {}), body


def extract_blockquote_meta(body: str) -> tuple[dict, str]:
    """把正文顶部的 `> status:` / `> scope:` 等元数据行抽出来并移除。"""
    lines = body.split("\n")
    found: dict = {}
    kept: list[str] = []
    for line in lines:
        match = META_LINE.match(line)
        if match:
            value = match.group(2).strip()
            if value:
                found[match.group(1)] = value
            continue
        kept.append(line)
    if not found:
        return {}, body
    # 只在头部区域（标题 + 元数据）收敛因删除产生的多余空行，正文排版保持不变
    while kept and not kept[0].strip():
        kept.pop(0)
    window = min(len(kept), 12)
    for index in range(window - 1, 0, -1):
        if not kept[index].strip() and not kept[index - 1].strip():
            kept.pop(index)
    return found, "\n".join(kept)


def normalize_references(text: str) -> str:
    for pattern, replacement in REFERENCE_RULES:
        text = re.sub(pattern, replacement, text)
    # 引用块中「只认 xxx」的写法修正后可能出现 `rules/…` ，保留原文其余部分
    return text


def build_frontmatter(topic: dict, inherited: dict, default_reviewed: str) -> dict:
    data: dict = {}
    for key in FIELD_ORDER:
        if key == "last_reviewed":
            # 依次取：专题自定义 → 原文件声明 → 注册表默认
            value = topic.get("last_reviewed") or inherited.get("last_reviewed") or default_reviewed
            if value:
                data[key] = value
            continue
        if key in topic:
            data[key] = topic[key]
    for key in EXTRA_FIELDS:
        if key in inherited:
            data[key] = inherited[key]
    return data


def render(data: dict) -> str:
    text = yaml.safe_dump(
        data,
        allow_unicode=True,
        default_flow_style=False,
        sort_keys=False,
        width=10_000,
    )
    return f"{FM_FENCE}\n{text}{FM_FENCE}\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="只检查差异，不写入")
    args = parser.parse_args()

    registry = load_registry()
    topics = registry["topics"]
    default_reviewed = str(registry.get("last_reviewed", "2026-09"))
    declared = {topic["file"] for topic in topics}
    actual = {path.name for path in KNOWLEDGE.glob("*.md")} - {"README.md"}

    problems: list[str] = []
    if declared - actual:
        problems.append(f"registry 登记了不存在的文件: {sorted(declared - actual)}")
    if actual - declared:
        problems.append(f"文件未登记进 registry: {sorted(actual - declared)}")
    if problems:
        print("注册表与实际文件不一致:", file=sys.stderr)
        print("\n".join(f"- {item}" for item in problems), file=sys.stderr)
        return 1

    changed: list[str] = []
    for topic in topics:
        path = KNOWLEDGE / topic["file"]
        original = path.read_text(encoding="utf-8")

        inherited_fm, body = split_frontmatter(original)
        quote_meta, body = extract_blockquote_meta(body)
        inherited = {**quote_meta, **inherited_fm}

        reference_fixed = normalize_references(body)
        frontmatter = build_frontmatter(topic, inherited, default_reviewed)
        updated = render(frontmatter) + "\n" + reference_fixed.lstrip("\n")
        updated = updated.rstrip("\n") + "\n"

        if updated != original:
            changed.append(topic["file"])
            if not args.check:
                path.write_text(updated, encoding="utf-8")

    verb = "需要同步" if args.check else "已同步"
    print(f"{verb} {len(changed)} 个文件:")
    for name in changed:
        print(f"  - {name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
