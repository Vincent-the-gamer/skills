# jev

Skill to get a typed, calibrated decision from TypeSafe AI's Jev (System One) Model — choose one of a list, answer yes/no, or rate on a scale — through `scripts/jev.mjs`.

Ask the Agent to route a ticket, pick a tool, judge urgency, or grade risk without guessing.

Requires Node.js ≥ 20. `scripts/jev.mjs` is self-contained (axios and cac are bundled), so there is nothing to install.

## Usage

```bash
node scripts/jev.mjs <type> --state <state> --question <question> [options]
```

`<type>` is `choice`, `noul`, or `score`, and must come first. `--state` (the situation) and `--question` (one bounded question about it) are always required.

### Choose one — `choice`

Pick a single option from a list of at least 2:

```bash
node scripts/jev.mjs choice \
  --state "A customer writes: my plan was charged twice this month, can you refund one charge?" \
  --question "Which team should handle this ticket?" \
  -o Billing -o "Tech Support" -o Sales -o "Account Security"
```

### Answer yes / no — `noul`

Returns P(yes); takes no options:

```bash
node scripts/jev.mjs noul \
  --state "A user's account just signed in from another country and they ask you to freeze it now." \
  --question "Does this need an immediate reply?"
```

### Rate on a scale — `score`

Options are ordered low → high; `score` is the expected level as a 0-based index:

```bash
node scripts/jev.mjs score \
  --state "About to drop production log tables older than 30 days; the change cannot be rolled back." \
  --question "How high is the risk of this operation?" \
  --options "Very low,Low,Medium,High,Very high"
```

## Options

| Flag | Meaning |
|---|---|
| `--state <text>` | Situation to evaluate. Required. |
| `--question <text>` | One bounded question about the state. Required. |
| `-o, --option <text>` | An option; repeat once per option. `choice`/`score` need at least 2. |
| `--options <list>` | Options as a comma-separated string or JSON array, in place of `-o`. |
| `--api <url>` | Override the endpoint. Default `https://api-proxy.vince-g.xyz/jev`. |
| `--timeout <ms>` | Request timeout in milliseconds. Default `30000`. |
| `--raw` | Print the API's raw result instead of the arranged one. |
| `-h, --help` | Show usage. |
| `-v, --version` | Show version. |

Notes:

- The order you list options defines `decisionIndex`; when you mix the two forms, all `-o` values are collected before the `--options` values.
- `--options` accepts `"a,b,c"` or `'["a","b","c"]'` — use the JSON form when an option itself contains a comma.
- `noul` rejects any options; `choice` and `score` reject fewer than 2.

## Output

A single JSON object is printed to stdout; errors go to stderr and the process exits non-zero.

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

- `decision` — the most likely label (the pick for `choice`/`score`, or `是`/`否` for `noul`), with its `probability`.
- `probabilities` — the full distribution, in the order you passed the options.
- `score` — expected level for `score` questions, 0-based (add 1 for a 1–N scale). Present for `score` only.
