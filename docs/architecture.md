# Architecture

## Core principle
The orchestration domain is provider-neutral. BigFix is an adapter, not the workflow engine.

## Control plane
The control plane owns campaign definitions, approvals, policies, topology, durable execution state, audit events and provider execution references.

## Strategy-aware campaigns
Campaign types are first-class strategies:
- standard
- rolling/batch
- canary/ring
- tiered application/middleware/database
- cluster/database
- hybrid/custom

Each strategy can expose different execution visualizations while using the same campaign and execution APIs.

## Reliability requirements
Execution will use durable state, idempotency keys, endpoint/stage checkpoints, bounded retries, timeouts and distributed locks. Restarting the control plane must never restart already-successful patch work.

## Provider boundary
Provider adapters translate generic execution requests into vendor APIs. Provider-specific IDs and raw responses are retained for diagnostics and audit, but do not leak into orchestration rules.

## Next
PostgreSQL persistence, execution state machine, audit events, topology model, authentication/RBAC and React UI.
