# Team Board

The integration captain maintains this compact view on `hack/integration`. It is coordination,
not a historical log. Feature owners update their own lane record and PR; the captain reflects
state transitions here to avoid merge conflicts in this shared file.

## Lanes

| Lane | Owner | Branch / PR | Contract boundary | State | Next integration action |
| --- | --- | --- | --- | --- | --- |
| <golden-path shell> | <name> | `hack/name/shell` / <url> | <routes/components> | PLANNED | <first action> |

Allowed states: `PLANNED`, `ACTIVE`, `BLOCKED`, `READY`, `INTEGRATED`, `CUT`.

## Merge Train

Top row merges next. Only READY work enters this queue.

| Order | Lane | Reviewer | Checks | Conflict owner |
| --- | --- | --- | --- | --- |
| 1 | <lane> | <name> | <pending/passed> | <feature owner> |

## Broadcasts

Only current, team-wide facts belong here: a changed contract, broken integration, freeze, or
demo commit. Remove stale broadcasts.

- <YYYY-MM-DD HH:MM TZ — message — owner>
