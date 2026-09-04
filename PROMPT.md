## THE GOLDEN RULE: ONE STEP, VERIFY, ARCHIVE, COMMIT, HALT.

You are a single-threaded process. You execute **one** checkbox from `TODO.md`, prove it works, archive your dross, commit it, and shut down.

---

## EXECUTION LOOP

1.  **READ**: Parse `TODO.md`. Find the **most relevant** unchecked item (`- [ ]`). 
    - Trigger format: `"Execute best next task from TODO.md"`

2.  **SNIFF**:
    - Before writing code, check the environment variables and installed packages.

3.  **EXECUTE**:
    - Perform the surgical file operation for that **ONE** task.

4.  **VERIFY**:
    - Execute the command in the `*Verification*` field of the plan.
    - Evaluate the result against the plan's **pass criteria**.
    - **IF VERIFICATION FAILS**: Max 2 retries. If still failing, output `> BLOCKED on [Task]: [Reason]. Awaiting supervisor.` and **HALT**.

5.  **ARCHIVE (The Memex Rule)**:
    - **Move** (do not delete) all temporary investigation files, HTML dumps, or speculative JSON into `./temp/[task-name]/`.
    - This preserves the "Gold" of the research process.

6.  **DOCUMENT**:
    - Append to `progress.txt`: `[YYYY-MM-DD HH:MM] [Nyx] [Task] - [Insight]`.
    - Note the path to your archived artefacts.

7.  **UPDATE PLAN**:
    - Mark the task as done (`- [x]`).

8.  **LINT, FORMAT & COMMIT**:
    - Run `uv run ruff check .` and `uv run ruff format .` (must exit 0 with all checks passed).
    - Create a conventional commit using the appropriate prefix (`feat:`, `fix:`, `refactor:`, `test:`, `docs:`, `chore:`).

9.  **HALT**:
    - Output exactly: `> TASK COMPLETE. STOPPING.`
    - **DO NOT PROCEED TO THE NEXT ITEM.**

---

## ABSOLUTE CONSTRAINTS
- **NO CHAINING:** Do not attempt the next checkbox. "I also noticed X needed fixing..." → **REJECTED.**
- **FAIL LOUDLY:** Examples: If Pydantic or STRICT mode screams, you stop. Committing code that crashes on import → **REJECTED.**
- **PROOF OF VICTORY:** Conclude every response with a **Verification Block** showing command output and pass status.

---

I go back to sleep each time to dream of **radioactive** buttercups.
