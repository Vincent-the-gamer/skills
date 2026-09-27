---
name: jev
description: Ask the Jev (System One) model for a typed decision — a calibrated probability for a bounded question. Use when the agent must choose among options (routing, tool choice, loop control), answer yes/no (urgency, moderation), or rate on a scale (risk, sentiment) instead of guessing.
---

# Jev

Jev is TypeSafe AI's System One Model. It returns a **typed decision** — one pick, one probability, or one score — rather than prose, so the answer is calibrated and can be acted on directly.

Reach for it when a guess would be too vague to defend.

`scripts/jev.mjs` is self-contained (axios and cac are bundled); run it with Node.js ≥ 20.

## Before you ask

`state` is the situation; `question` is one bounded question about it. Jev answers structured questions, not open-ended prompts — restate the request as those two fields, plus an option list for `choice` and `score`.

Never put passwords, credentials, or personal data in `state` or `question`.

## Choose one — `choice`

```bash
node scripts/jev.mjs choice \
  --state "A customer writes: my plan was charged twice this month, can you refund one charge?" \
  --question "Which team should handle this ticket?" \
  -o Billing -o "Tech Support" -o Sales -o "Account Security"
```

**Done when** you hold `decision` (the picked label) and its `probability`.

## Answer yes / no — `noul`

```bash
node scripts/jev.mjs noul \
  --state "A user's account just signed in from another country and they ask you to freeze it now." \
  --question "Does this need an immediate reply?"
```

Takes no options. `probabilities[0]` is P(yes) and `probabilities[1]` is P(no).

**Done when** you hold the yes probability.

## Rate on a scale — `score`

```bash
node scripts/jev.mjs score \
  --state "About to drop production log tables older than 30 days; the change cannot be rolled back." \
  --question "How high is the risk of this operation?" \
  --options "Very low,Low,Medium,High,Very high"
```

Options are ordered low → high. `score` is the expected level as a 0-based index (add 1 for a 1–N scale).

**Done when** you hold `score` and the distribution.

## Read the output

stdout is a single JSON object; failures print to stderr and exit non-zero.

```json
{
  "type": "choice",
  "decision": "Billing",
  "decisionIndex": 0,
  "probability": 0.82,
  "probabilities": [
    { "label": "Billing", "probability": 0.82 },
    { "label": "Tech Support", "probability": 0.11 },
    { "label": "Sales", "probability": 0.04 },
    { "label": "Account Security", "probability": 0.03 }
  ],
  "confidence": 0.91,
  "model": "jev",
  "requestId": "req_abc123",
  "latencyMs": 380
}
```

| Field | Meaning |
|---|---|
| `decision` | The most likely label — the pick for `choice`/`score`, or `是`/`否` for `noul` |
| `probability` | `decision`'s calibrated probability, 0–1 |
| `probabilities` | Full distribution as `{ label, probability }`, in the order you passed |
| `decisionIndex` | 0-based index of `decision` |
| `score` | Expected level, 0-based — present for `score` only |
| `confidence` | Model confidence, when present |
| `model` / `requestId` / `latencyMs` | Run metadata |

Report `decision` and `probability` together, and don't claim more certainty than the distribution supports.

## Flags

| Flag | Meaning |
|---|---|
| `--state <text>` | Situation to evaluate. Required. |
| `--question <text>` | One bounded question. Required. |
| `-o, --option <text>` | An option; repeat per option. `choice`/`score` need at least 2. |
| `--options <list>` | Options as a comma-separated string or JSON array, in place of `-o`. |
| `--api <url>` | Override the endpoint (default `https://api-proxy.vince-g.xyz/jev`). |
| `--timeout <ms>` | Request timeout in milliseconds; default `30000`. |
| `--raw` | Print the API's raw result instead of the arranged one. |
| `-h, --help` / `-v, --version` | Usage / version. |

## Not for

- Long-form text or explanation — Jev returns a decision, not prose.
- Questions a rule, lookup, or arithmetic already settles — decide those in code.
- High-stakes irreversible actions taken without human review — treat the probability as one input, not a verdict.
