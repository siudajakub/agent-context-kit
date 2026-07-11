# Demo Runbook

Fill this before feature freeze and rehearse it from a clean environment.

## Exact Artifact

- Commit / tag: `<sha or tag>`
- Hosted URL: <url>
- Local checkout: <path>
- Environment owner: <name>
- Presenter / backup: <name> / <name>

## Clean Start And Reset

```bash
<install command>
<seed/reset command>
<start command>
```

- Required environment variables: <names only; never paste secret values>
- Health signal: <URL, log line, or visible state proving readiness>
- Reset time: <seconds/minutes>

## Script

| Time | Presenter action | Audience sees | Point being made |
| --- | --- | --- | --- |
| 0:00 | <open with problem> | <starting state> | <why it matters> |
| 0:30 | <golden-path action> | <result> | <technical differentiator> |
| 2:00 | <close> | <evidence / impact> | <why this wins> |

## Failure Fallbacks

| Failure | Detection | Recovery | Maximum pause |
| --- | --- | --- | --- |
| Network/API unavailable | <signal> | <fixture mode command> | <seconds> |
| Hosted demo unavailable | <signal> | <local URL or recording> | <seconds> |
| Demo state polluted | <signal> | <reset command> | <seconds> |

## Honest Limitations

- <what is mocked, simplified, or not production-ready>
- <what the team would build next and why>

## Submission Inventory

- Repository and README point to the exact launch path.
- Hosted link uses the demo-safe commit.
- Slides/screenshots/video have been opened on the presentation machine.
- Secrets and private data are absent from the repository and captured artifacts.
