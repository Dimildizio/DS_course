---
name: state-snapshot
description: Update `docs/logs/STATE.md` — the single-page briefing for a fresh session (what & why, current stage, layout, locked-in decisions, how to fetch data, where to read more). Triggers **only on extra-important changes** — architecture pivot, new/removed top-level layer, new data channel, ML/tech stack swap, change to the public input/output contract. Routine work does not go here — that belongs in DEVLOG.
---

# state-snapshot

## What this is

A service-agnostic template for the `docs/logs/STATE.md` convention. Drop the file into `.claude/skills/state-snapshot/SKILL.md` of any target repo. Extend triggers / sections with project-specific bits.

## Why it exists

`STATE.md` is a **snapshot** that a fresh session (agent or human) reads first to understand the **shape** of the project in 60 seconds: what exists, what's planned, which decisions are locked in. Not a chronicle (that's DEVLOG), not a plan (that's `docs/planning/`), not a public README — an internal briefing.

## When to update (triggers)

Update **only when the shape of the project changes, not its content**:

- **Architecture pivot** — e.g. classical-ML ↔ LLM, monolith ↔ microservices, single-model ↔ ensemble.
- **New / removed top-level layer** — a `serving/` directory appeared, `research/` got killed, a separate service was carved out.
- **New data channel or major change to an existing one** — different supplier, different format, different delivery mechanism.
- **ML / tech stack swap** — dropped XGBoost, added deep learning; migrated Postgres → ClickHouse.
- **Public contract change** — input/output API changed, event schema changed, bus payload changed.

## When **not** to update

- A new module / extractor / endpoint **inside an existing layer**.
- Refactor inside `src/common/` or its equivalent.
- Bugfix, new test, dependency bump.
- Doc cosmetics.

All of the above — **DEVLOG only**, leave STATE alone.

## File structure

Recommended sections (order matters — top to bottom):

```markdown
# State — <project-name>

> Briefing for a fresh session (agent / human). This file is a **snapshot**: what exists, what's planned, what is locked in. Rationale — in `docs/planning/*` (or your equivalent). Chronology — in `DEVLOG.md`. **Update only on extra-important changes** (see triggers). Last update: YYYY-MM-DD (short note on why).

## What & why

One or two sentences: what this service is, what problem it solves, what's at the input/output, who its neighbors / counterparties are.

## Stage

One sentence: planning / scaffolding / MVP / production / sunset. What is locked in, what is not yet written.

## Layout

Top-level directory tree with short comments. Mark ✅ for what already exists and ❌ for what is planned.

## What actually works right now (≠ just planned)

A table: layer → where it lives → state in one line. Helps separate "code is there, you can call it" from "only a design doc exists".

## Architectural decisions

Bullets of locked-in decisions (what was picked, what was rejected). No long rationale — link to `docs/planning/<file>.md` or an ADR instead.

## How to fetch data / run things (if applicable)

Bootstrapping commands: install, run, run tests, fetch data. The first thing a human will ask for.

## Neighbor projects (if any)

Relevant repos / services with one-line note about their role for us (feature donor / data source / consumer / shared stack).

## Where to look next

Quick links: CLAUDE.md, docs/planning/, DEVLOG, README, dashboards.
```

## What does **not** belong in STATE

- **Long rationale** — that goes in `docs/planning/<topic>.md` or an ADR. STATE only links.
- **Chronology** — that's DEVLOG. STATE has no "what we did yesterday".
- **TODO list** — that's a tracker / separate file. STATE describes "what is", not "what we plan".
- **Live metrics / prod snapshots** — that's observability, not STATE.
- **Duplicating the public README** — README is for outside consumers; STATE is for the inside session.

## Update procedure

1. Something changed → check the triggers. Most edits don't qualify — close out via DEVLOG only.
2. Trigger fired → update **only the relevant sections** of STATE. If a layer changed — update `Layout` and `What actually works right now`. If a pivot — update `Stage` + `Architectural decisions`. Don't rewrite the whole file.
3. Bump the `Last update: YYYY-MM-DD (short reason)` line at the top.
4. In parallel, add a DEVLOG entry (via **devlog-update**) — chronology lives there, shape lives here.

## Good update example

Before:

```markdown
> ... Last update: 2026-05-05 (initial scaffold).
```

After (persistence layer landed):

```markdown
> ... Last update: 2026-05-07 (DB layer + MLflow up; v1 contract frozen).
```

And inside `Layout`, under `src/db/` — instead of `❌ stub` it now reads `✅ SQLAlchemy ORM, Alembic migrations applied`.

## Bad updates (don't do this)

- Rewriting the whole file because one new module landed inside an existing layer → **that's a DEVLOG entry**, leave STATE alone.
- Adding "yesterday we did X, today we're doing Y" → STATE is not a chronicle.
- Long paragraph "why we picked LightGBM" → that's `docs/planning/<...>.md`; STATE only links.

## Related skills

- **devlog-update** — the DEVLOG entry is written **alongside** a STATE update (not instead of). DEVLOG = what changed when; STATE = how it looks now.
