#!/usr/bin/env python3
"""
Selectively clear Quarto's freezer for pages whose source file or included
subfiles changed in this PR.

Why this exists
---------------
The project renders with `freeze: auto`, and CI restores the `_freeze`
directory from a cache so unchanged pages reuse their previously executed
output instead of re-running R. Quarto decides whether a frozen result is
stale by hashing the page's *own* source file only. That misses the case
where a page pulls in another file via a `{{< include ... >}}` shortcode:
when the *included* subfile changes but the parent `.qmd` does not, the
parent's hash is unchanged, so Quarto serves the stale frozen output and the
include's new content never appears in the preview.

This script closes that gap. It diffs the PR against its base branch, maps
each page to the set of files it depends on (itself plus its includes,
resolved recursively), and removes the `_freeze` directory only for pages
whose file or subfiles actually changed. Everything else keeps its cached
freeze, so this stays cheap — it only forces re-execution of the pages that
genuinely need it. The full-rebuild escape hatch (the `clear-freezer` PR
label, which skips the cache restore entirely) is unchanged; this step is
skipped when that label is present.

Environment variables
----------------------
FREEZE_DIR : freezer directory to prune (default: ``_freeze``).
BASE_SHA   : base branch commit to diff against (the PR base SHA). When
             unset or unresolvable, the script makes no changes and lets
             Quarto's own `freeze: auto` handling stand.
"""

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

# {{< include path >}} / {{< include "path" >}} / {{< include 'path' >}}
# Three capture groups: double-quoted, single-quoted, unquoted.
INCLUDE_RE = re.compile(r"""\{\{<\s*include\s+(?:"([^"]+)"|'([^']+)'|([^"'>\s]+))\s*>}}""")


def run_git(args):
    """Run a git command, returning stdout (stripped) or None on failure."""
    result = subprocess.run(
        ["git", *args], capture_output=True, text=True, check=False
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def changed_files(base_sha):
    """Return the set of repo-relative paths changed between base and HEAD.

    Uses the merge-base (``base...HEAD``) so files changed only on the base
    branch since the PR forked don't count as the PR's changes.
    """
    merge_base = run_git(["merge-base", base_sha, "HEAD"]) or base_sha
    diff = run_git(["diff", "--name-only", f"{merge_base}...HEAD"])
    if diff is None:
        return None
    return {line for line in diff.splitlines() if line}


def resolve_includes(qmd_path, _seen=None):
    """Recursively collect the files a `.qmd` page depends on.

    Returns absolute, resolved ``Path`` objects: the page itself plus every
    file it pulls in through `{{< include ... >}}`, resolved relative to the
    including file's directory. Cycles and missing targets are tolerated;
    missing/deleted targets are still recorded (so deleting an included
    subfile clears the parent's freezer) but not recursed into.
    """
    if _seen is None:
        _seen = set()
    qmd_path = qmd_path.resolve()
    if qmd_path in _seen:
        return _seen
    _seen.add(qmd_path)
    if not qmd_path.is_file():
        return _seen

    try:
        text = qmd_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return _seen

    for match in INCLUDE_RE.finditer(text):
        rel_path = match.group(1) or match.group(2) or match.group(3)
        included = (qmd_path.parent / rel_path).resolve()
        resolve_includes(included, _seen)
    return _seen


def freeze_dir_for(rel_qmd, freeze_root):
    """Map a repo-relative `.qmd` path to its `_freeze` directory.

    Quarto mirrors the source path under the freezer without the extension,
    e.g. ``chapters/chapter1.qmd`` -> ``_freeze/chapters/chapter1``.
    """
    return freeze_root / rel_qmd.with_suffix("")


def main():
    repo_root = Path.cwd()
    freeze_root = Path(os.getenv("FREEZE_DIR", "_freeze"))

    if not freeze_root.is_dir():
        print(f"No freezer at {freeze_root}; nothing to clear.")
        return

    base_sha = os.getenv("BASE_SHA", "").strip()
    if not base_sha:
        print("BASE_SHA is unset; leaving the freezer to Quarto's freeze: auto.")
        return

    changed = changed_files(base_sha)
    if changed is None:
        print(
            f"Could not diff against {base_sha}; leaving the freezer to "
            "Quarto's freeze: auto."
        )
        return

    if not changed:
        print("No changed files relative to the base branch; freezer untouched.")
        return

    changed_abs = {(repo_root / f).resolve() for f in changed}

    cleared = []
    for qmd in sorted(repo_root.rglob("*.qmd")):
        # Skip pages living inside build-artifact trees.
        rel = qmd.relative_to(repo_root)
        if rel.parts and rel.parts[0] in {"_site", "_freeze", ".quarto"}:
            continue

        deps = resolve_includes(qmd)
        if not (deps & changed_abs):
            continue

        target = freeze_dir_for(rel, freeze_root)
        if not target.is_dir():
            continue

        changed_deps = sorted(
            str(d.relative_to(repo_root)) for d in (deps & changed_abs)
        )
        print(f"Clearing freezer for {rel} (changed: {', '.join(changed_deps)})")
        # Remove the page's freezer tree so Quarto re-executes it.
        shutil.rmtree(target)
        cleared.append(str(rel))

    if cleared:
        print(f"\nCleared freezer for {len(cleared)} page(s): {', '.join(cleared)}")
    else:
        print("No page's file or subfiles changed; freezer untouched.")


if __name__ == "__main__":
    sys.exit(main())
