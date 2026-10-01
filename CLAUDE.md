# Working on Rafiq

## Kanban: track everything
The owner's Kanban board is this repo's GitHub issues. Every piece of work goes on it — no exceptions:

- **Before starting** a task (a request, a bug, an idea worth keeping), make sure an issue exists; add the
  `in progress` label while working on it.
- **When done**, close it with a short note of what changed and the PR number(s).
- **Ideas, follow-ups and owner to-dos** that come up along the way get their own open issue.
- Label every issue with a priority: `priority: before launch`, `priority: next` or `priority: later`.
- Big pieces of work: a parent issue with sub-issues.

## Tests: run before pushing
- `node tests/progress-fsrs.test.js`: review scheduling (FSRS) and the boxes pages read.
- Browser smoke test (webapp-testing skill): every page loads with no JavaScript errors.
  `python3 .claude/skills/webapp-testing/scripts/with_server.py --server "python3 -m http.server 8765 >/dev/null 2>&1" --port 8765 -- python3 tests/smoke.py`
- Lesson layout (heading at the top, exercise centred, Listen cue): `... -- python3 tests/lesson_layout.py` (same server command as the smoke test).
- Start-up speed (pages show within 600 ms online and offline; background sync keeps local changes): `... -- python3 tests/startup_speed.py` (same server command as the smoke test).
- Login page (opening, Sign in / Create account switch, field messages, spinner and tick): `... -- python3 tests/login_page.py` (same server command as the smoke test).
- `python3 tests/funnel.py`: after changing the funnel in `supabase/sql/backend.sql` (runs it on a throwaway Postgres).
- `python3 tools/camel-check.py`: after changing Arabic in the word list, see `tools/camel-report.md`.

## How to code (Karpathy guidelines)
From github.com/multica-ai/andrej-karpathy-skills. The Kanban rule above still applies.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

### 1. Think Before Coding
**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

### 2. Simplicity First
**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

### 3. Surgical Changes
**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

### 4. Goal-Driven Execution
**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

Rules:
- The graph isn't committed. If graphify-out/ is missing and you need it, run `graphify update .` (about 30s, no API cost).
- For codebase questions, first run `graphify query "<question>"` when graphify-out/graph.json exists. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).
