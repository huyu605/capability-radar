# Candidate type checks

## Agents

- Identify the model, tools, memory, data flow, execution boundary, and operator.
- Separate a reusable configuration or prompt from an agent that can perform real actions.
- Check exportability, reproducibility, marketplace lock-in, and hidden paid dependencies.

## Agent skills

- Read the full `SKILL.md` and any scripts it can invoke.
- Inspect provenance, update mechanism, tool dependencies, permissions, and prompt-injection risk.
- Confirm compatibility with the target agent and distinguish instructions from executable capability.

## MCP servers

- Enumerate exposed tools/resources, transports, authentication, and requested scopes.
- Check whether operations are read-only or mutating and whether a sandbox is possible.
- Verify schema quality, error behavior, maintenance, deployment model, and secret handling.

## Tools, APIs, and CLIs

- Verify supported inputs/outputs, automation interface, rate limits, offline behavior, and stability.
- Identify external services, API keys, telemetry, destructive commands, and data retention.
- Prefer documented, versioned interfaces and reproducible installation.

## Software libraries

- Check API stability, releases, CI/tests, maintainers, dependents, dependency risk, and advisories.
- Confirm runtime/platform compatibility and estimate adoption and migration cost.
- Read the actual license and note copyleft, source-available, trademark, or commercial restrictions.

## Deployable products

- Verify deployment completeness, databases/services, upgrades, backups, observability, and resource needs.
- Check authentication, multi-user support, data ownership, export, privacy, and operational burden.
- Distinguish open source from source available and hosted-only features.
