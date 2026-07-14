---
description: Render the full Quarto site and report build status
allowed-tools:
  - Bash(quarto render:*)
  - Bash(quarto render)
---

Run `quarto render` to build the full site.

Report:

- Whether the build succeeded or failed
- Any ERROR or WARNING messages, with the file and line number where each occurred
- A summary of which output formats were produced

If the build fails, diagnose the root cause and suggest a fix before asking to proceed.
Do not commit `_site/`, `_freeze/`, or `.quarto/` — those are build artifacts.
