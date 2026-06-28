# Architecture

Module ownership and dependency boundaries. Read before any architecture or module-boundary
change. The goal is that an agent can place new code correctly without re-deriving the structure.

## Module Map

<List each module / package / layer, what it owns, and what it must not depend on.>

- `<module>` — <responsibility>. Depends on: `<...>`. Must not depend on: `<...>`.
- `<module>` — <...>

## Dependency Rules

- <Allowed and forbidden dependency directions — e.g. "UI may depend on services; services must
  not depend on UI.">
- Keep data and service logic out of the presentation layer.
- One source of truth per piece of state; do not add a parallel model.

## Sources Of Truth

- <State / concept> → <where it lives and how it is read/written>.

## Extending The System

- <Where new features should go, and the seams to reuse rather than duplicate.>
- <Patterns to follow so new code matches the surrounding code.>
