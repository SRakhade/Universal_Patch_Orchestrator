# Inventory and topology model

UPO must not silently guess production topology. Classification is evidence-based and can be verified by an administrator.

## Discovery precedence
1. Verified UPO assignment / CMDB
2. BigFix properties and approved computer groups
3. Cluster/provider discovery
4. Installed software and services
5. Naming conventions

Lower-confidence discovery creates a suggestion, not an authoritative role.

## Core relationships
- Application contains topology nodes.
- Server belongs to an application/environment and may have a role.
- Nodes can depend on other nodes.
- Cluster nodes have cluster identity and runtime role.
- Patch strategy consumes the topology graph.

Example:
```
Load Balancer
   |
APP-01  APP-02
   \     /
 MW-01  MW-02
      |
 SQL-AG-PROD
 DB01 <-> DB02
```

Tier and cluster execution must validate runtime health/role before disruptive operations.
