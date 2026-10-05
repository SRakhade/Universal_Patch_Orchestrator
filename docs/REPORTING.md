# Reporting and Provider Status Architecture

## Objective
Every patch campaign must remain observable after deployment. UPO stores the provider action reference, periodically reconciles its status, normalizes endpoint results and produces campaign reports independently of the patch-management vendor.

## BigFix first
For BigFix, UPO will:
1. Submit the action through the BigFix REST API.
2. Persist the returned BigFix action ID.
3. Poll/reconcile the BigFix action status through REST.
4. Normalize per-endpoint state into UPO states.
5. Persist status history and endpoint results in PostgreSQL.
6. Continue polling until a terminal state or configured timeout.
7. Run post-patch validation/compliance checks.
8. Produce campaign, patch, endpoint and failure reports.

A successful REST request is not equivalent to successful patching.

## Normalized status
Providers map their native states into:
- pending
- running
- succeeded
- partial
- failed
- cancelled
- unknown

Endpoint results can include exit code, message/failure reason and reboot requirement.

## Reports
Planned report surfaces:
- Campaign Executive Summary
- Compliance Before vs After
- Patch Success / Failure
- Endpoint Execution Detail
- Reboot Pending
- Offline / Not Reported
- Excluded / Not Relevant
- Failure Diagnostics
- Ring / Wave / Tier performance
- Maintenance-window adherence
- Provider action history
- Audit / approval history

Filters include application, business unit, environment, provider, OS, patch, severity, campaign, ring/tier, server role, status and date range.

Exports: CSV first; PDF and scheduled delivery later.

## Failure diagnostics
BigFix diagnostics can enrich failed endpoint results. Windows patch failures may correlate patch-related Windows Event Log evidence. Linux integrations can support configured diagnostic collectors, including environment-specific files such as EDR deployment results. Diagnostic collection must be bounded, auditable and avoid unrestricted remote file retrieval.

## Multi-provider design
The orchestration engine never calls BigFix directly. Each integration implements the PatchProvider contract.

Future adapters can include MECM/SCCM, Tanium, Ansible/AWX, HPSA/BladeLogic and cloud-native patch services. A provider advertises capabilities so the UI and orchestrator only expose supported operations.

A provider configuration should contain:
- provider type
- display name
- base/API URL
- authentication/secret reference
- TLS settings
- connection timeout
- status polling interval
- enabled capabilities
- optional site/tenant/context

Secrets must not be persisted as clear text in provider configuration.

## Reconciliation
Status polling belongs to background workers, not browser requests. Reconciliation is idempotent. Application restarts resume from persisted provider action IDs and execution checkpoints.
