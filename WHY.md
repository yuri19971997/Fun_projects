# Why We Work This Way

This file explains the reasoning behind the project structure. Not rules to follow -- understanding to apply. Read it once. The principles will make sense when you hit the situations they describe.

---

## Three documents, not ten

Every project has `AGENTS.md` (rules), `HANDOFF.md` (current state), and `CHANGELOG.md` (history). That's it.

We learned this the hard way. A project accumulated `START_HERE.md`, `ROADMAP.md`, `PROGRESS.md` (86K lines), `.tasks/remaining.md`, `.tasks/scope.md`, and 7 individual task files. `START_HERE.md` existed solely to warn you which other documents were stale. When you need a document to explain which documents to trust, you have too many documents.

Three files, three roles, no overlap. If you're about to create a fourth file, put the content in one of the three.

## HANDOFF.md is edited, not appended

`HANDOFF.md` always reflects the current state. When something changes, you update it in-place. You don't add a note at the bottom saying "update: this section is now wrong."

We had a progress file that grew to 86K lines because it was append-only. Nobody read it. The useful information was copied into other files. The original became dead weight. History belongs in `CHANGELOG.md` and `git log`. Current state belongs in `HANDOFF.md`. Don't mix them.

## Tests before features

The test runner, the pre-commit hook, and the baselines file exist in this template before any feature code. That's deliberate.

Every project that adds testing after the features are built has the same experience: the test infrastructure never catches up. You're always testing yesterday's code. But if the test runner exists from day one, every feature gets a test because the infrastructure is already there and running it is one command.

## The pre-commit hook is a nudge, not a wall

The hook checks that the build compiles without warnings and that tests were run. It warns about stale test results. It doesn't block everything -- an agent can still commit documentation changes without running the full suite.

We could make it stricter. But strict hooks get bypassed (`--no-verify`). A nudge that's occasionally annoying is better than a wall that gets circumvented.

## PITFALLS.md captures experience

When you fix a bug or discover non-obvious behavior, you write a 4-line entry in `PITFALLS.md`: symptom, cause, fix, commit. The file grows naturally from the work.

This exists because agents don't persist memory between sessions. An agent that spent 4 hours debugging an init recursion deadlock will lose that knowledge when the session ends. The next agent will hit the same deadlock and spend the same 4 hours. Unless the first agent wrote it down. The pitfall entry takes 30 seconds to write and saves hours for every future session.

## Pass conditions before implementation

Every task has a concrete pass condition written before work starts. Not "make it work" but "bench.cu D2H throughput > 3 GB/s" or "test_memory subtest 12 completes without blocking."

This exists because without a pass condition, "done" is subjective. An agent can convince itself something works by running it once and eyeballing the output. A pass condition is a contract you can't negotiate with.

## Reference code by name, not line number

"After the declaration of `g_handle_map`" not "after line ~2113." Line numbers drift with every edit. An agent following a stale line number will insert code in the wrong place. Function names and variable names survive edits and are greppable.

## The completeness checker is a mirror, not a motivator

The `/motivation` skill doesn't give pep talks. It checks git status, HANDOFF.md freshness, test results, and build state, then reports what's objectively incomplete. An agent doesn't need encouragement to keep working. It needs to know what's not done yet.

## Improve the process, not just the product

When you fix a bug, also add the test that would have caught it. When you hit friction, also fix the tool or script that caused it. When you discover something, also write it in PITFALLS.md. The task is never just the task. Each session should leave the workflow better than it found it.

This is how the project gets faster over time. Not because the code is better, but because the process for making the code better is better.

---

These aren't abstract principles. They're lessons from real projects where the opposite was tried and failed. Follow them not because a document says to, but because the alternative is repeating mistakes that have already been made.
