# Universal Patch Orchestrator

Vendor-neutral enterprise patch orchestration platform.

## Goals
- Standard, rolling/batch, canary/ring, tier-based, cluster/database and hybrid patching.
- BigFix as the first execution provider without coupling orchestration logic to BigFix.
- Secure, resumable, auditable and API-first execution.
- Dynamic campaign views driven by the selected orchestration strategy.

## Architecture
```
Web UI / External API
        |
     API Layer
        |
Orchestration Engine
  |       |       |
State   Policy   Audit
        |
Provider Interface
  |             |
BigFix       Future providers
```

## Repository layout
- `apps/api` - FastAPI control-plane API
- `apps/web` - web UI (next milestone)
- `packages/orchestrator` - vendor-neutral domain and workflow engine
- `packages/providers` - execution-provider adapters
- `docs` - architecture and security decisions

## Current milestone
Foundation: campaign domain model, strategy-aware workflow planning, provider contract, BigFix adapter skeleton and API endpoints.

> Do not store BigFix credentials or other secrets in source control.
