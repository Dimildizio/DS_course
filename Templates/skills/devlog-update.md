---
name: devlog-update
description: Append a compact entry to `docs/logs/DEVLOG.md` after a significant change — new module, new feature, architectural decision, removal of something material. Triggers — "update the devlog", "log this", "note in DEVLOG", or right after the agent itself wraps a meaningful piece of work. Trivial edits do not go here.
---

# devlog-update

## What this is

A service-agnostic template for the `docs/logs/DEVLOG.md` convention. Drop the file into `.claude/skills/devlog-update/SKILL.md` of any target repo — format and triggers are ready. Extend the body with project-specific exceptions if the project has any.

## Why it exists

A single shared change-log that the next session (agent or human) reads to immediately understand "what changed, in what order". Without it the agent burns context doing archaeology over `git log` and old PRs.

## When to write an entry

Write one if **something material** happened in the current session:

- a top-level module or directory appeared / was removed;
- an architectural decision was locked in (even if no code was written yet);
- a new external service / dependency / store was wired in;
- a public contract changed (API / DB schema / config format);
- a formal spec or contract document was **produced, frozen, revised, or superseded** — e.g. a `FINAL_CONTRACT.md`, ADR, RFC, or any deliverable from a structured contract / planning pipeline. Log the freeze event and any subsequent revision rounds, not the intermediate drafts;
- a feature block or large piece of logic was added or killed;
- a refactor changed the calling convention of a module (names, signatures, import paths).

## When **not** to write

- Typos, formatting, renaming a local variable.
- Point bugfix that does not change externally observable behavior.
- Intermediate commits inside a single task — fold them into one entry once done.
- An experiment rolled back in the same session (unless "we tried this and rejected it" is itself useful — then one line).

## Format

**Compact.** 1–3 bullets, one line each. Don't write "why" if obvious. Don't write "consequences" if trivial. New entry goes **on top**.

```markdown
## YYYY-MM-DD — short headline (what was done)
- what / where: one line with the path to file/module
- (optional) why: one line, only if not obvious from the headline
- (optional) deferred / not done: one line
```

Date is **today's calendar date**, `YYYY-MM-DD`. If several related edits happened in one session on the same day — **one entry, multiple bullets**, do not repeat the headline.

## Good example

```markdown
## 2026-05-07 — DB scaffold + MLflow helpers (+ deps)
- `src/db/{base,models}.py` — SQLAlchemy 2.x ORM per design doc: 3 tables, engine/sessionmaker singleton.
- `alembic upgrade head` runs clean on a fresh SQLite; migration `9d4c8189adc3` — 3 tables + 7 indexes.
- `pyproject.toml` deps += sqlalchemy/alembic/mlflow; `.env.example` += `DATABASE_URL`.
```

## Bad examples (don't do this)

```markdown
## 2026-05-07 — small fixes
- fixed a few things in models                # ← uninformative
- why: to make it better                      # ← zero signal
- consequences: now it works                  # ← trivial
```

```markdown
## 2026-05-07 — refactor
[three paragraphs about how we renamed a field]   # ← that's an RFC, not a devlog
```

## Grouping by session

If one session closes several related tasks — **one entry with an umbrella headline** and one bullet per task. Don't split into 5 entries with the same date.

If the tasks are **unrelated** (e.g. CI in the morning, a feature in the evening) — **two entries**, both dated today, different headlines.

## Where to put it

The file lives at `docs/logs/DEVLOG.md`. If it doesn't exist yet, create it with the header:

```markdown
# Devlog — <project-name>

Chronology of meaningful changes. New entries **on top**. Trivial edits do not belong here.

**Format — compact, 1–3 bullets, one line each. Don't write "why" if obvious. Don't write "consequences" if trivial.**

---
```

Then append new entries directly after `---`, **above** existing ones.

## Related skills

- **state-snapshot** — maintains `docs/logs/STATE.md`. Triggers only on "extra-important" changes (architecture pivot, new layer, contract change). When you write a DEVLOG entry, ask yourself: does this also trigger STATE? Most of the time — no.
