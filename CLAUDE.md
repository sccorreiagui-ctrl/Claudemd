# CLAUDE.md

Guidance for AI assistants (Claude Code and others) working in this repository.

## Project overview

**Claudemd** is a repository for generating high-level projects with Claude Code
(see `README.md`). At the time of writing it is a **greenfield repository**: the
only tracked content is `README.md`. There is no application code, build system,
test suite, or dependency manifest yet.

Treat this file as the source of truth for conventions. As real code lands,
**update the relevant sections below** so this document keeps describing the
codebase as it actually is — do not let it drift into describing intentions
instead of reality.

The project's human-facing description is written in Portuguese ("Repositório
para Claude code. Geração de projetos de alto nível!"). Match the existing
language of a file when editing it: keep user-facing docs consistent with
`README.md`, and keep code identifiers/comments in English unless a file already
establishes otherwise.

## Current repository layout

```
.
├── README.md      # Short project description (Portuguese)
└── CLAUDE.md      # This file — guidance for AI assistants
```

When you add the first real subsystem, replace this tree with an accurate one
and add a short note on what each top-level directory is responsible for.

## Getting started (for a new stack)

No toolchain is committed yet, so there is nothing to install or build. When you
introduce the first piece of a stack, also commit the standard entry points for
it and document them here. For example:

- **Node/TypeScript** → `package.json` with `scripts` for `build`, `test`,
  `lint`; commit the lockfile.
- **Python** → `pyproject.toml` (and a lockfile), a `tests/` directory, and a
  documented way to run the app.
- **Go** → `go.mod`, standard `go build ./...` / `go test ./...`.

Whichever stack is chosen, wire up **format, lint, and test** commands early and
record the exact invocations in the next section.

## Development workflow

### Commands

_No build/test/lint tooling exists yet._ Once it does, list the canonical
commands here so they can be run without guessing, e.g.:

```
# examples — replace with the project's real commands
<install>     # install dependencies
<build>       # build the project
<test>        # run the full test suite
<test-one>    # run a single test / file
<lint>        # lint and format checks
```

Keep this list minimal and correct. If a command needs environment setup, note
it inline.

### Branching and commits

- **Do all work on a feature branch**, never commit directly to `main`. The
  active development branch for the current task is `claude/claude-md-docs-b071kr`;
  create it from the latest `main` if it does not exist locally.
- Write clear, imperative commit messages ("Add X", "Fix Y") describing the
  change and its intent.
- Push with `git push -u origin <branch-name>`.
- **Do not open a pull request unless explicitly asked.**
- If the PR for a branch has already been merged, start fresh from the latest
  `main` rather than stacking new commits on merged history.

## Conventions

- **Documentation-as-you-go.** Because this is a starter repository, the most
  important convention is keeping `README.md` and this `CLAUDE.md` accurate.
  Every structural change (new directory, new tooling, new entry point) should
  come with a matching docs update in the same change.
- **Small, verifiable changes.** Prefer focused commits over large drops of
  generated code. When you add code, add the means to verify it (tests or a
  documented manual check).
- **No secrets in the repo.** Keep credentials, tokens, and environment-specific
  values out of version control; use a `.env` (git-ignored) or the environment.

## Notes for AI assistants

- This repository is intentionally minimal right now. Do not assume the
  existence of frameworks, directories, or scripts that are not present — verify
  with the filesystem first.
- When a request implies a stack or structure not yet established, pick sensible
  defaults, state the choice, and record it here so future sessions stay
  consistent.
