# Hackathon Control Sheet

The stable, one-page brief for the event. The integration captain owns edits to this file on
`hack/integration`; feature lanes consume it but do not maintain divergent copies.

## Mission

- Event / deadline: <event and absolute deadline with timezone>
- Problem: <one sentence describing the painful problem>
- User: <the person experiencing it>
- Promise: <the outcome the demo proves>
- Judging bias: <the criterion that wins ties between two good ideas>

## Golden Path

In at most five observable steps:

1. <starting state>
2. <user action>
3. <system response>
4. <differentiating moment>
5. <clear result>

## Acceptance Bar

- Must work: <the minimum end-to-end behavior>
- May be mocked: <external systems or data allowed to be deterministic>
- Must be real: <the technically meaningful core>
- Explicitly cut: <features the team will not build during this event>

## Branches And Roles

- Demo-safe branch: `main`
- Integration branch: `hack/integration`
- Integration captain: <name>
- Product / demo owner: <name>
- Design owner: <name>
- Backup presenter: <name>

## Clock

Use absolute local timestamps so nobody has to translate relative time.

| Milestone | Time | Exit condition |
| --- | --- | --- |
| Contracts freeze | <YYYY-MM-DD HH:MM TZ> | Cross-lane interfaces and fixtures agreed |
| First integration | <YYYY-MM-DD HH:MM TZ> | One thin golden path runs on integration |
| Feature freeze | <YYYY-MM-DD HH:MM TZ> | Only fixes, demo copy, and observability remain |
| Demo freeze | <YYYY-MM-DD HH:MM TZ> | Exact demo commit tagged; fallback captured |
| Submission | <YYYY-MM-DD HH:MM TZ> | Links, deck, and repository submitted |

## Failure Budget And Cuts

| Risk | Signal | Fallback / cut owner |
| --- | --- | --- |
| <external API is slow> | <timeout or quota signal> | <fixture mode, owner> |
| <lane misses freeze> | <not READY by time> | <remove flag/route, owner> |

## Links

- Team channel: <url>
- Board / tracker: <url or TEAM_BOARD.md>
- Hosted demo: <url>
- Submission: <url>
