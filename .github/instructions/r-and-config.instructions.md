---
applyTo: "**/*.{R,r,yml,yaml}"
description: "Use when editing R source, Quarto configuration, or GitHub workflow files in this repository."
---

# R and Config Work

- This repo is both a Quarto project and a small R package. Check
  [DESCRIPTION](../../DESCRIPTION), [_quarto.yml](../../_quarto.yml), and the
  relevant workflow file before changing package, render, or CI behavior.
- Respect [.lintr.R](../../.lintr.R). For changed `.R` files run
  `Rscript -e 'lintr::lint("path/to/file.R")'`, then confirm
  `Rscript -e 'lintr::lint_dir()'` still passes (this is what CI runs).
- If a render-affecting config change touches a page, render only that page in
  HTML (`quarto render <file>.qmd --to html`), not the full site.
- Run `Rscript -e 'spelling::spell_check_package()'` before finishing changes to
  `.R` or config files. Fix only errors you introduced, and add legitimate
  technical terms to `inst/WORDLIST` rather than disabling the check.
- This is a template: every dependency added here lands in every downstream
  book, so do not add a new R package or Quarto extension without a clear
  reason. Align workflow and render changes with the existing CI patterns
  instead of inventing parallel setup.
- Do not edit generated files (`README.md` is built from `README.Rmd`; `_site/`,
  `_freeze/`, and `.quarto/` are build outputs).

See also:

- [DESCRIPTION](../../DESCRIPTION)
- [_quarto.yml](../../_quarto.yml)
- [CLAUDE.md](../../CLAUDE.md)
- [lint-project.yaml](../workflows/lint-project.yaml)
- [preview.yml](../workflows/preview.yml)
- [copilot-instructions.md](../copilot-instructions.md)
