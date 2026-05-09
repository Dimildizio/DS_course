---
name: session-handoff
description: Write a short handoff note to `docs/logs/HANDOFF.md` so the next Claude session can resume mid-task without re-reading the repo. Triggers — context window is filling up, user pauses mid-task ("let's continue tomorrow"), task is too big for one session, or right before `/compact`. Overwritten each handoff, cleared once the work resumes and lands. Distinct from STATE (stable shape, slow-moving) and DEVLOG (append-only history of completed changes).
---

# session-handoff

## What this is

A service-agnostic template for `docs/logs/HANDOFF.md` — a short, **volatile**, single-page note that captures in-flight session state so the next session resumes without re-discovery. Drop into `.claude/skills/session-handoff/SKILL.md` of any target repo.

## Why it exists

`STATE.md` describes the project's **shape** (slow-moving, only on architecture-level triggers). `DEVLOG.md` records **history** (append-only, only after a change has landed). Neither captures the third thing a fresh session needs:

- "I was 60 % through implementing X."
- "Next concrete action is Y."
- "Open question I parked: Z."
- "I noticed gotcha G but haven't decided what to do about it."

Without HANDOFF this state lives only inside the closed conversation. The next session re-derives it by reading code and DEVLOG, burning context. HANDOFF is the cheapest way to avoid that.

## When to write

Write / update HANDOFF when:

- The user signals end-of-session mid-task ("let's continue tomorrow", "park this for now").
- Context window is getting tight and you suspect a `/compact` or a fresh session is imminent.
- You're handing off to a different agent or human reviewer.
- You finished one chunk of a multi-chunk task and the next chunk is non-trivial.

## When **not** to write

- Task is **fully done** → write a DEVLOG entry instead, then either delete HANDOFF or mark it `(none — last session done, see DEVLOG)`.
- Short Q&A or read-only exploration with no meaningful work-in-flight → no handoff needed.
- The "next action" is a one-liner trivially derivable from the current state of the repo (e.g. "run the tests") → not worth a file.

## Lifecycle

HANDOFF is **overwritten**, not appended:

1. Session ends mid-task → write/overwrite HANDOFF.
2. New session starts → reads HANDOFF first, then resumes.
3. New session finishes the task → **clear HANDOFF** (or replace with the next handoff if still mid-flight) **and** write a DEVLOG entry for the completed work.

If HANDOFF is empty / a placeholder, the next session knows there is no in-flight work and only reads STATE + recent DEVLOG.

## Format

Short. One screen. Opinionated about what's missing.

```markdown
# Handoff — <project-name>

> Volatile in-flight session state. Overwritten each handoff, cleared when the task lands. Last update: YYYY-MM-DD HH:MM (timezone optional).

## Current task

One line. What is being worked on and the link / ticket / planning doc if any.

## Done in the session that just ended

- bullet, one line each: what is now on disk
- include file paths: `src/foo/bar.py:42` style if useful
- include "decisions made this session" that are too tactical for an ADR

## Next action

One or two lines. The **very next concrete step**. Not a list of everything left to do — just what the next session does first.

## Open questions

- bullet: question parked mid-flight, what would unblock it
- bullet: decision deferred, why deferred

## Gotchas discovered (not yet acted on)

- bullet: surprise found this session that the next session needs to know but isn't yet a fix / decision
- bullet: examples — flaky test, undocumented behaviour, dependency quirk

## Files in flight

- `path/to/file.py` — uncommitted, what state it's in
- `path/to/other.md` — partial draft

## Skipped sections

If a section is empty, write a single line `(none)` rather than removing the heading — keeps the shape predictable.
```

## Good example

```markdown
# Handoff — <your-service>

> Volatile in-flight session state. Last update: YYYY-MM-DD HH:MM.

## Current task

Wire the real parser into `/import` (replace `_stub_parse`). Spec: `docs/planning/import_strategy.md` §3.

## Done in the session that just ended

- `src/parsers/csv_parser.py` — schema-driven parse with type coercion; rejects malformed rows with structured error.
- 6 unit tests in `tests/parsers/test_csv_parser.py`, all green.
- Decided to reuse `pandas.read_csv` over a hand-rolled tokenizer — added to deps.

## Next action

Replace `_stub_parse` in `src/api/app.py:118` with `from src.parsers.csv_parser import parse_csv` and rerun the existing TestClient suite. Expect 1 failure on `import-empty-file` (stub returned 200; real parser returns 422 — adjust the route's mapping).

## Open questions

- Files with extra columns: strict reject or lenient drop? Parked — see `import_strategy.md` §3.2 follow-up.
- `pandas` adds ~50 MB to the image; CI base image needs a rebuild before the parser ships.

## Gotchas discovered (not yet acted on)

- Trailing newlines in some inputs produce an empty final row (sample `data/samples/orders_2024_q3.csv`). The parser handles it; the downstream validator does not — currently flags it as a malformed row.

## Files in flight

- `src/parsers/csv_parser.py` — committed.
- `tests/parsers/test_csv_parser.py` — committed.
- `src/api/app.py` — clean, untouched this session.
```

## Bad examples (don't do this)

```markdown
# Handoff
- working on stuff                            # ← no signal
- next: continue                              # ← worthless
```

```markdown
## Done

[two pages of every line of code that changed, with rationale]   # ← that's a DEVLOG entry, not a handoff
```

```markdown
## Architectural decisions

We chose LightGBM because ...                # ← that's an ADR or planning doc, not handoff
```

## Length budget

If HANDOFF grows past ~80 lines, you're putting the wrong things in it. Common offenders:

- Long rationale → move to ADR / planning.
- History of edits → DEVLOG.
- Stable shape (layout, locked decisions) → STATE.
- Full TODO list for the rest of the project → tracker.

Handoff is **only** the volatile slice the next session needs to resume.

## Procedure for the resuming session

1. Read `HANDOFF.md` first. Then `STATE.md`. Then most recent DEVLOG entries.
2. Confirm with the user that "Current task" is still the right thing to work on (priorities may have shifted).
3. Execute "Next action".
4. When the work lands → write a DEVLOG entry, then either:
   - **clear** HANDOFF (replace body with `(none — last session landed, see DEVLOG entry YYYY-MM-DD)`), or
   - **overwrite** HANDOFF with the next handoff if you're still mid-flight on a follow-up chunk.

## Related skills

- **devlog-update** — runs at the end of work, after HANDOFF is cleared. DEVLOG = what shipped; HANDOFF = what's mid-flight.
- **state-snapshot** — runs only on extra-important triggers; HANDOFF triggers every session that ends mid-task. If you're tempted to put something in STATE because it's "current", check whether it's actually volatile — if yes, it belongs in HANDOFF.
