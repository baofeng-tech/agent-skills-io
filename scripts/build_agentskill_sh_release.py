#!/usr/bin/env python3
"""Build a GitHub-ready agentskill.sh release layer from targetSkills/."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import build_claude_release as base
import build_agentskills_so_release as shared
from release_zip import write_deterministic_zip


REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCE_ROOT = REPO_ROOT / "targetSkills"
OUTPUT_ROOT = REPO_ROOT / "agentskill-sh-release"
ZIP_ROOT = OUTPUT_ROOT / "zips"
PUBLIC_REPO = "https://github.com/baofeng-tech/agent-skills"
PUBLIC_BRANCH = "main"
PUBLIC_PLATFORMS = "agentskills.io,agentskill.sh,github"


def zip_skill(skill_dir: Path, zip_path: Path) -> None:
    write_deterministic_zip(skill_dir, zip_path)


def write_skill_readme(skill_dir: Path, frontmatter: dict[str, object]) -> None:
    name = str(frontmatter.get("name") or skill_dir.name)
    description = str(frontmatter.get("description") or f"{name} Agent Skill.")
    lines = [
        f"# {base.prettify_skill_name(name)}",
        "",
        "GitHub-ready release package prepared specifically for agentskill.sh import and refresh.",
        "",
        "## Notes",
        "",
        f"- {description}",
        "- This directory keeps one root-level skill per folder so agentskill.sh can scan the repository cleanly.",
        "- The same skill can also be submitted by direct `SKILL.md` URL when needed.",
    ]
    (skill_dir / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_skill(src_dir: Path) -> dict[str, object]:
    out_dir = OUTPUT_ROOT / src_dir.name
    shutil.rmtree(out_dir, ignore_errors=True)
    out_dir.mkdir(parents=True, exist_ok=True)

    base.copy_tree(src_dir, out_dir)
    frontmatter, body = base.load_frontmatter(src_dir / "SKILL.md")
    cleaned_frontmatter = shared.clean_frontmatter(
        src_dir,
        frontmatter,
        repository_url=PUBLIC_REPO,
        platforms=PUBLIC_PLATFORMS,
    )  # type: ignore[arg-type]
    cleaned_body = shared.rewrite_body(body, src_dir.name)
    (out_dir / "SKILL.md").write_text(base.dump_skill(cleaned_frontmatter, cleaned_body), encoding="utf-8")

    audit = base.SkillAudit(
        name=src_dir.name,
        source_path=str(src_dir.relative_to(REPO_ROOT)),
        output_path=str(out_dir.relative_to(REPO_ROOT)),
        description=str(cleaned_frontmatter["description"]),
    )
    base.prune_release_tree(out_dir, audit)
    shared.trim_standard_skill_surface(out_dir, audit)
    base.patch_runtime_files(out_dir, audit)
    base.rewrite_markdown_tree(out_dir, "agentskills", audit)
    write_skill_readme(out_dir, cleaned_frontmatter)
    audit.changes.append("flattened metadata for agentskill.sh-friendly GitHub import")
    audit.changes.append("preserved root-level skill folder layout for repository scanning")

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


def write_docs(skills: list[dict[str, object]]) -> None:
    readme = [
        "# agentskill.sh Release",
        "",
        "GitHub-ready release layer generated from `targetSkills/` for agentskill.sh import.",
        "",
        "## Purpose",
        "",
        "- Produce a root-level public skill repository that agentskill.sh can scan with `Analyze & Import`.",
        "- Keep the frontmatter close to the open Agent Skills spec while making the repo shape explicit for GitHub import.",
        "- Emit per-skill ZIP artifacts for direct-URL or manual update workflows.",
        "",
        "## Recommended Submit Flow",
        "",
        f"1. Push this directory to the public GitHub repository root at `{PUBLIC_REPO}`.",
        "2. Open `https://agentskill.sh/submit`.",
        "3. Paste the GitHub repo URL and run `Analyze & Import`.",
        "4. Optionally add the GitHub webhook `https://agentskill.sh/api/webhooks/github` for faster sync.",
        "5. Keep `index.json`, `index.md`, and `well-known-skills-index.json` at repo root for cleaner crawler discovery.",
        "",
        "## Generated Skills",
        "",
    ]
    for skill in skills:
        readme.append(f"- `{skill['name']}`")
    (OUTPUT_ROOT / "README.md").write_text("\n".join(readme) + "\n", encoding="utf-8")

    publishing = [
        "# Publishing agentskill.sh Release",
        "",
        "1. Run `python3.12 scripts/build_agentskill_sh_release.py`.",
        f"2. Push the generated contents to the public GitHub repository `{PUBLIC_REPO}`.",
        "3. Submit that repository at `https://agentskill.sh/submit`.",
        "4. For ongoing sync, add the webhook `https://agentskill.sh/api/webhooks/github`.",
        "5. Keep the generated catalog files at repo root for GitHub import clarity.",
        "",
        "## Notes",
        "",
        "- agentskill.sh accepts either a GitHub repo URL or a direct `SKILL.md` URL.",
        "- This release layer keeps one skill per root directory so repo scanning stays predictable.",
        "- It removes plugin wrapper files such as `package.json` and `index.ts` when they are not part of the shipped standard skill surface.",
    ]
    (OUTPUT_ROOT / "PUBLISHING.md").write_text("\n".join(publishing) + "\n", encoding="utf-8")

    payload = {
        "generated_at": "2026-04-20",
        "source": "targetSkills",
        "skills": skills,
    }
    (OUTPUT_ROOT / "index.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    audit_lines = [
        "# agentskill.sh Release Audit",
        "",
        f"- Generated skills: {len(skills)}",
        "- Frontmatter mode: Agent Skills spec-leaning with flat metadata.",
        "- Repository mode: one skill directory per repo root entry for GitHub scanning.",
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
    shared.write_index_markdown(
        skills,
        output_root=OUTPUT_ROOT,
        repository_url=PUBLIC_REPO,
        branch=PUBLIC_BRANCH,
    )
    shared.write_well_known_index(
        skills,
        output_root=OUTPUT_ROOT,
        repository_url=PUBLIC_REPO,
        branch=PUBLIC_BRANCH,
    )
    shared.copy_root_license(output_root=OUTPUT_ROOT)


def main() -> None:
    shutil.rmtree(OUTPUT_ROOT, ignore_errors=True)
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    ZIP_ROOT.mkdir(parents=True, exist_ok=True)

    skills = [build_skill(path.parent) for path in sorted(SOURCE_ROOT.glob("*/SKILL.md"))]
    write_docs(skills)
    print(f"Built {len(skills)} agentskill.sh-ready skills into {OUTPUT_ROOT.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
