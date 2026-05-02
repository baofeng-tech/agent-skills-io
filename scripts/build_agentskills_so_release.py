#!/usr/bin/env python3
"""Build a GitHub-ready Agent Skills / AgentSkills.so release layer from targetSkills/."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import build_claude_release as base
from release_zip import write_deterministic_zip


REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCE_ROOT = REPO_ROOT / "targetSkills"
OUTPUT_ROOT = REPO_ROOT / "agentskills-so-release"
ZIP_ROOT = OUTPUT_ROOT / "zips"
PUBLIC_REPO = "https://github.com/baofeng-tech/agent-skills-so"
PUBLIC_BRANCH = "main"
PUBLIC_PROVIDER = "AIsa"
PUBLIC_PLATFORMS = "agentskills.io,agentskills.so,github"
NON_STANDARD_PLUGIN_FILES = {
    "CHANGELOG.md",
    "index.ts",
    "openclaw.plugin.json",
    "package-lock.json",
    "package.json",
}


def infer_tags(name: str, description: str) -> list[str]:
    lower = f"{name} {description}".lower()
    tags: list[str] = []
    for token in (
        "twitter",
        "x",
        "youtube",
        "search",
        "research",
        "market",
        "stock",
        "prediction",
        "finance",
        "media",
        "video",
        "image",
        "llm",
        "router",
        "provider",
        "aisa",
    ):
        if token in lower and token not in tags:
            tags.append(token)
    if not tags:
        tags.append("automation")
    return tags[:8]


def flatten_metadata(
    frontmatter: dict[str, object],
    skill_dir: Path,
    description: str,
    *,
    repository_url: str = PUBLIC_REPO,
    platforms: str = PUBLIC_PLATFORMS,
) -> dict[str, str]:
    metadata = frontmatter.get("metadata") or {}
    aisa = metadata.get("aisa") if isinstance(metadata, dict) else {}
    primary_env = ""
    if isinstance(aisa, dict):
        primary_env = str(aisa.get("primaryEnv") or "")
    version = str(frontmatter.get("version") or "1.0.0")
    homepage = base.normalize_homepage(frontmatter.get("homepage")) or "https://aisa.one"
    repository = str(frontmatter.get("repository") or repository_url)
    flattened = {
        "author": str(frontmatter.get("author") or "AIsa"),
        "version": version,
        "homepage": homepage,
        "repository": repository,
        "tags": ",".join(infer_tags(skill_dir.name, description)),
        "platforms": platforms,
    }
    if primary_env:
        flattened["primary_env"] = primary_env
    return flattened


def clean_frontmatter(
    skill_dir: Path,
    frontmatter: dict[str, object],
    *,
    repository_url: str = PUBLIC_REPO,
    platforms: str = PUBLIC_PLATFORMS,
) -> dict[str, object]:
    name = skill_dir.name
    description = str(frontmatter.get("description") or f"{name} Agent Skill.")
    compatibility = str(frontmatter.get("compatibility") or "")
    cleaned: dict[str, object] = {
        "name": name,
        "description": description,
    }
    license_value = frontmatter.get("license")
    if license_value not in (None, "", []):
        cleaned["license"] = license_value
    if compatibility:
        cleaned["compatibility"] = compatibility

    metadata = flatten_metadata(
        frontmatter,
        skill_dir,
        description,
        repository_url=repository_url,
        platforms=platforms,
    )
    if metadata:
        cleaned["metadata"] = metadata

    allowed_tools = base.infer_allowed_tools(skill_dir, frontmatter)  # type: ignore[arg-type]
    if allowed_tools:
        cleaned["allowed-tools"] = allowed_tools
    return cleaned


def rewrite_body(body: str, skill_name: str) -> str:
    rewritten = base.rewrite_user_facing_markdown(base.rewrite_skill_body(body, skill_name), "agentskills", skill_name)
    return rewritten


def trim_standard_skill_surface(skill_dir: Path, audit: base.SkillAudit) -> None:
    removed: list[str] = []
    for name in sorted(NON_STANDARD_PLUGIN_FILES):
        path = skill_dir / name
        if path.exists():
            path.unlink()
            removed.append(name)
    if removed:
        audit.changes.append(
            "removed non-standard plugin wrapper files from the standard GitHub skill bundle: "
            + ", ".join(removed)
        )


def zip_skill(skill_dir: Path, zip_path: Path) -> None:
    write_deterministic_zip(skill_dir, zip_path)


def write_skill_readme(skill_dir: Path, frontmatter: dict[str, object]) -> None:
    name = str(frontmatter.get("name") or skill_dir.name)
    description = str(frontmatter.get("description") or f"{name} Agent Skill.")
    lines = [
        f"# {base.prettify_skill_name(name)}",
        "",
        "GitHub-ready Agent Skills release package for AgentSkills-compatible marketplaces.",
        "",
        "## Notes",
        "",
        f"- {description}",
        "- This release keeps the standard `SKILL.md` + `scripts/` + `references/` shape for GitHub indexing and ZIP export.",
        "- Publish each skill as a root-level directory in a public repository for best marketplace pickup.",
    ]
    (skill_dir / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_skill(src_dir: Path) -> dict[str, object]:
    out_dir = OUTPUT_ROOT / src_dir.name
    shutil.rmtree(out_dir, ignore_errors=True)
    out_dir.mkdir(parents=True, exist_ok=True)

    base.copy_tree(src_dir, out_dir)
    frontmatter, body = base.load_frontmatter(src_dir / "SKILL.md")
    cleaned_frontmatter = clean_frontmatter(src_dir, frontmatter)
    cleaned_body = rewrite_body(body, src_dir.name)
    (out_dir / "SKILL.md").write_text(base.dump_skill(cleaned_frontmatter, cleaned_body), encoding="utf-8")

    audit = base.SkillAudit(
        name=src_dir.name,
        source_path=str(src_dir.relative_to(REPO_ROOT)),
        output_path=str(out_dir.relative_to(REPO_ROOT)),
        description=str(cleaned_frontmatter["description"]),
    )
    base.prune_release_tree(out_dir, audit)
    trim_standard_skill_surface(out_dir, audit)
    base.patch_runtime_files(out_dir, audit)
    base.rewrite_markdown_tree(out_dir, "agentskills", audit)
    write_skill_readme(out_dir, cleaned_frontmatter)
    audit.changes.append("flattened metadata for marketplace-friendly Agent Skills frontmatter")
    audit.changes.append("preserved relative-path runtime assets for GitHub-backed discovery")

    zip_path = ZIP_ROOT / f"{src_dir.name}.zip"
    zip_skill(out_dir, zip_path)
    return {
        "name": audit.name,
        "path": audit.output_path,
        "description": audit.description,
        "zip": str(zip_path.relative_to(REPO_ROOT)),
        "changes": audit.changes,
        "residual_risks": audit.residual_risks,
    }


def skill_tree_url(skill_name: str, *, repository_url: str = PUBLIC_REPO, branch: str = PUBLIC_BRANCH) -> str:
    return f"{repository_url}/tree/{branch}/{skill_name}"


def summarize_skill_files(skill_dir: Path) -> list[str]:
    included: list[str] = []
    for candidate in (
        "scripts",
        "references",
        "assets",
        "requirements.txt",
        "SKILL.md",
        "README.md",
    ):
        path = skill_dir / candidate
        if path.is_dir():
            for child in sorted(path.rglob("*")):
                if child.is_file():
                    included.append(str(child.relative_to(skill_dir)))
                    if len(included) >= 5:
                        return included
        elif path.is_file():
            included.append(candidate)
            if len(included) >= 5:
                return included
    return included


def write_index_markdown(
    skills: list[dict[str, object]],
    *,
    output_root: Path = OUTPUT_ROOT,
    repository_url: str = PUBLIC_REPO,
    branch: str = PUBLIC_BRANCH,
) -> None:
    lines = [
        "# AIsa Agent Skills Index",
        "",
        "This index is prepared for the public Agent Skills repository used by AgentSkills.so-style crawlers.",
        "",
        f"- Repository: <{repository_url}>",
        f"- Branch: `{branch}`",
        f"- Branch URL: <{repository_url}/tree/{branch}>",
        "",
        "## Skills",
        "",
    ]
    for skill in skills:
        name = str(skill["name"])
        description = str(skill["description"])
        lines.append(f"### `{name}`")
        lines.append("")
        lines.append(f"- GitHub: <{skill_tree_url(name, repository_url=repository_url, branch=branch)}>")
        lines.append(f"- Summary: {description}")
        includes = summarize_skill_files(output_root / name)
        if includes:
            lines.append("- Includes:")
            for item in includes:
                lines.append(f"  - `{item}`")
        lines.append("")
    (output_root / "index.md").write_text("\n".join(lines), encoding="utf-8")


def write_well_known_index(
    skills: list[dict[str, object]],
    *,
    output_root: Path = OUTPUT_ROOT,
    repository_url: str = PUBLIC_REPO,
    branch: str = PUBLIC_BRANCH,
) -> None:
    payload = {
        "version": "1.0",
        "provider": {
            "name": PUBLIC_PROVIDER,
            "repository": repository_url,
            "branch": branch,
            "homepage": f"{repository_url}/tree/{branch}",
        },
        "skills": [
            {
                "name": str(skill["name"]),
                "description": str(skill["description"]),
                "location": skill_tree_url(str(skill["name"]), repository_url=repository_url, branch=branch),
            }
            for skill in skills
        ],
    }
    (output_root / "well-known-skills-index.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def copy_root_license(*, output_root: Path = OUTPUT_ROOT) -> None:
    candidates = [REPO_ROOT / "LICENSE", REPO_ROOT / "LICENSE.txt", REPO_ROOT / "LICENSE.md"]
    for candidate in candidates:
        if candidate.exists():
            shutil.copy2(candidate, output_root / "LICENSE")
            return
    for candidate in sorted(output_root.glob("*/LICENSE")):
        shutil.copy2(candidate, output_root / "LICENSE")
        return


def write_docs(skills: list[dict[str, object]]) -> None:
    readme = [
        "# AgentSkills.so Release",
        "",
        "Agent Skills open-standard release layer generated from `targetSkills/`.",
        "",
        "## Purpose",
        "",
        "- Produce a GitHub-ready root-level skill catalog for `agentskills.so` style indexing.",
        "- Keep frontmatter close to the published Agent Skills spec: `name`, `description`, `license`, `compatibility`, flat `metadata`, and optional `allowed-tools`.",
        "- Emit per-skill root-flat ZIP artifacts for manual import flows.",
        "",
        "## Layout",
        "",
        "- `<skill>/`: publishable skill directory",
        "- `zips/<skill>.zip`: root-flat archive with `SKILL.md` at archive root",
        "",
        "## Recommended Publish Flow",
        "",
        f"1. Push this directory to the public repository `{PUBLIC_REPO}`.",
        "2. Keep every skill directory at the repo root.",
        "3. Preserve `index.json`, `index.md`, and `well-known-skills-index.json` at repo root so crawlers see a stable catalog signal.",
        "4. Submit or share the repo URL with marketplaces that index Agent Skills from GitHub.",
        "5. Use the generated ZIPs for platforms that support direct skill upload/import.",
        "",
        "## Generated Skills",
        "",
    ]
    for skill in skills:
        readme.append(f"- `{skill['name']}`")
    (OUTPUT_ROOT / "README.md").write_text("\n".join(readme) + "\n", encoding="utf-8")

    publishing = [
        "# Publishing AgentSkills.so Release",
        "",
        "1. Run `python3.12 scripts/build_agentskills_so_release.py`.",
        f"2. Copy the directory contents to the public GitHub repository root at `{PUBLIC_REPO}`.",
        "3. Keep the generated catalog files at repo root: `index.json`, `index.md`, and `well-known-skills-index.json`.",
        "4. Submit or surface that GitHub repository to `agentskills.so` or other Agent Skills directories.",
        "5. Keep future updates on the same repository so marketplace crawlers can refresh from GitHub.",
        "",
        "## Notes",
        "",
        "- This release layer is standards-first, not Claude-specific.",
        "- It removes plugin-wrapper files such as `package.json` and `index.ts` when they are not part of the shipped standard skill surface.",
        "- It is tuned for `agentskills.so` indexing rather than generic multi-runtime wording.",
    ]
    (OUTPUT_ROOT / "PUBLISHING.md").write_text("\n".join(publishing) + "\n", encoding="utf-8")

    payload = {
        "generated_at": "2026-04-20",
        "source": "targetSkills",
        "skills": skills,
    }
    (OUTPUT_ROOT / "index.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    audit_lines = [
        "# AgentSkills.so Release Audit",
        "",
        f"- Generated skills: {len(skills)}",
        "- Frontmatter mode: Agent Skills spec-leaning with flat metadata.",
        "- Archive mode: root-flat ZIP per skill for manual import flows.",
        f"- Repository target: `{PUBLIC_REPO}`",
        "- Safety trim: removes plugin wrapper files from standard skill bundles.",
        "",
    ]
    for skill in skills:
        audit_lines.extend(
            [
                f"## {skill['name']}",
                "",
                f"- Path: `{skill['path']}`",
                f"- Zip: `{skill['zip']}`",
                f"- Description: {skill['description']}",
                "",
            ]
        )
    (OUTPUT_ROOT / "AUDIT.md").write_text("\n".join(audit_lines), encoding="utf-8")

    gitignore = [
        ".DS_Store",
        "__pycache__/",
        "*.pyc",
        ".pytest_cache/",
        ".claude-skill-data/",
    ]
    (OUTPUT_ROOT / ".gitignore").write_text("\n".join(gitignore) + "\n", encoding="utf-8")
    write_index_markdown(skills, output_root=OUTPUT_ROOT)
    write_well_known_index(skills, output_root=OUTPUT_ROOT)
    copy_root_license(output_root=OUTPUT_ROOT)


def main() -> None:
    shutil.rmtree(OUTPUT_ROOT, ignore_errors=True)
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    ZIP_ROOT.mkdir(parents=True, exist_ok=True)

    skills = [build_skill(path.parent) for path in sorted(SOURCE_ROOT.glob("*/SKILL.md"))]
    write_docs(skills)
    print(f"Built {len(skills)} AgentSkills-ready skills into {OUTPUT_ROOT.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
