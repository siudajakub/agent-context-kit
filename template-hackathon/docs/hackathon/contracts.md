# Cross-Lane Contracts

Freeze the seams that let lanes move independently. This is not a complete architecture spec.
The integration captain owns this file on `hack/integration`; a contract change names every
consumer and is broadcast before implementation.

## System Shape

```text
<client> -> <application/API> -> <meaningful technical core> -> <external systems or fixtures>
```

## Ownership Map

| Surface | Owning lane | Consumers | Stable entry point |
| --- | --- | --- | --- |
| <route/module/schema> | <lane> | <lanes> | <path/export/endpoint> |

## Interface Contracts

For each cross-lane boundary, include one successful example and one failure example.

### <Contract name>

- Owner: <lane / person>
- Consumers: <lanes / people>
- Version / status: `v1 PROPOSED | FROZEN | CHANGING`
- Transport / call: <HTTP route, function signature, event, file format>
- Success: <copy-pasteable request/input and response/output>
- Failure: <error shape and expected consumer behavior>
- Timeout / retry: <explicit behavior>
- Fixture / mock: <path and how to activate it>
- Compatibility: <what may change without coordinating>

## Shared Data And Fixtures

| Name | Source of truth | Owner | Reset / seed command |
| --- | --- | --- | --- |
| <demo dataset> | <path/service> | <lane> | `<command>` |

## Contract Change Protocol

1. Owner writes the proposed delta and names affected consumers.
2. Consumers acknowledge or request an adapter.
3. Captain marks the contract CHANGING and broadcasts it in `TEAM_BOARD.md`.
4. Owner lands compatibility or coordinates a single integration wave.
5. After integration checks pass, captain freezes the new version and removes the broadcast.
