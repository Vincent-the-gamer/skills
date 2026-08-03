# discipline

A pre-flight guardrail skill. Invoke it before work where the agent should be extra careful — it makes the agent gate every tool call through an explicit rule set.

**How to use:** type `discipline` before a sensitive task. The agent reads the rules, then checks every action against them.

The rules:

- Stay within what the user authorized — no scope creep
- Read before writing or executing
- Never run something you can't explain
- Don't invent capabilities the user hasn't given you
- Ask before any destructive file operation
