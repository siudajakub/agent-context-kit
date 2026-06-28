# Verification

Build/test/smoke commands and the check matrix. Read before selecting checks or claiming a change
is done. Use these commands verbatim — do not invent new ones.

## Environment

<Any required toolchain, runtime version, or environment variables. Example:>

```bash
<export ANY_REQUIRED_ENV=...>
```

## Fast Checks

Run on every change:

```bash
<lint>
<unit-tests>
python3 tools/check_agent_docs.py
```

## Full Checks

Run before merge or release:

```bash
<full test suite>
<integration / e2e>
<build / package artifact>
```

## Check Matrix

| Change type | Required checks |
| --- | --- |
| Docs only | `python3 tools/check_agent_docs.py` |
| Logic change | fast checks |
| Cross-module / pre-release | full checks |

## Claiming Completion

- Report the exact commands run and their result; paste failures rather than summarizing them.
- State plainly which checks were skipped and why.
- A change is not "done" until the Definition Of Done in AGENTS.md is met.
