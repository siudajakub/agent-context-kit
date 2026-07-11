# Team Board

The integration captain maintains this view on `hack/integration`. Before contributors join, the
captain defines small, non-overlapping choices under **Available Work**. Contributors run
`python3 tools/hack_join.py`; the tool reads this file and creates their selected lane.

## Available Work

Each row must contain a unique lowercase kebab-case slug. Write an observable outcome and a
concrete, non-overlapping file/module claim. `hack_join.py` offers rows whose state is `AVAILABLE`
and whose slug has no active `hack/*/<slug>` branch.

| Slug | Outcome / acceptance | Claim | Contract / dependency | Priority | State |
| --- | --- | --- | --- | --- | --- |
| `golden-path-shell` | <observable result that proves this lane is done> | `src/app/**` | <contract name or `none`> | P0 | AVAILABLE |

Allowed planning states: `AVAILABLE`, `PAUSED`, `CUT`.

## Active Lanes

Feature owners update their branch-local record and PR. The captain reflects state transitions
here; contributors do not edit this table from feature branches.

| Lane | Owner | Branch / PR | Contract boundary | State | Next integration action |
| --- | --- | --- | --- | --- | --- |
| <golden-path shell> | <name> | `hack/name/shell` / <url> | <routes/components> | ACTIVE | <first action> |

Allowed delivery states: `ACTIVE`, `BLOCKED`, `READY`, `INTEGRATED`, `CUT`.

## Merge Train

Top row merges next. Only READY work enters this queue.

| Order | Lane | Reviewer | Checks | Conflict owner |
| --- | --- | --- | --- | --- |
| 1 | <lane> | <name> | <pending/passed> | <feature owner> |

## Broadcasts

Only current, team-wide facts belong here: a changed contract, broken integration, freeze, or
demo commit. Remove stale broadcasts.

- <YYYY-MM-DD HH:MM TZ — message — owner>
