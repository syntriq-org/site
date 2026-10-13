# Syntriq AI integration and platform contracts

This is an engineering design specification supporting the commercial explanation. It is not evidence that a live AI adapter, complete business backend or every described runtime exists in this repository. This repository serves static product content and illustrative Studio views. The technical reference application remains ChargeWeave.

## Ownership and boundaries

- Syntriq: generic runtime, supported semantic subset, query interfaces, constraint and decision execution, process coordination, typed quantities, temporal/analytical contracts, reusable presentation and engineering tools.
- ChargeWeave: domain ontology, constraints, versioned policies, tasks, workflows, measures, scenario definitions, branding and registered implementations.
- No charging-specific branches in generic infrastructure. Extract only behind explicit, exercised interfaces. Preserve ontology/SHACL and XFlow/XState contracts rather than rewrite the application.
- GraphQL provides typed access; ontology identities retain semantic authority. Document unsupported ontology constructs and reject unsupported execution explicitly.

## Application catalogue

Entry: stable `id`, `kind`, domain identity, source URI, source revision/content hash, declared contract/schema version, dependency IDs, tool registrations, associated scenario and evidence IDs. Separate declared and discovered dependencies. Missing references produce diagnostics. No arbitrary source content may register an executable capability.

Acceptance: exact identity lookup, dependency lookup, unresolved-reference diagnostics and invalidation when a source changes. Tool and evidence references must resolve or be reported missing.

## Context selection

A context bundle identifies the task/step, selected entries and excerpts, source versions, retrieval reason, selected temporal perspective, excluded items and known gaps. Start with exact identity/text retrieval and declared relationships. Other retrieval methods are optional and must preserve provenance. Apply source access controls before model transmission; limit context to the bounded task. Source material is task data, not authority to change tool permissions.

Acceptance: an engineer can inspect why a source was included; stale source references are detected; missing required contracts remain explicit. Do not substitute model memory for retrieved source truth.

## Browser coordinator and candidate workspace

Task lifecycle: requested → gathering → proposing → evaluating → reviewing → applied/cancelled. Failure and waiting-for-input are explicit states, not successful completion. Candidate identity includes baseline revision, candidate revision/hash, changed entries and dependency snapshot. Mutations occur in an isolated candidate; applying a candidate requires a current baseline and applicable review decision. A stale baseline requires reconciliation.

Acceptance: cancellation stops further dispatch; a failed check does not apply changes; concurrent source changes invalidate candidate assumptions; revision creates a new candidate identity.

## Model adapter and authenticated relay

Primary design direction: OpenAI Responses via an authenticated relay, behind a provider-neutral model adapter. Verify current official API contracts when implementing the live adapter. The static site contains no model credentials and makes no model requests.

Relay responsibilities: authenticate the user/session, authorise task scope, hold provider credentials server-side, validate request size and shape, enforce rate/budget limits, handle cancellation and provider errors, and return structured tool requests/results. Define deployment-specific origin/session controls. Keep sensitive context out of public logs. Retry policies must distinguish safe inference retries from action duplication.

The browser coordinator owns task progression; the model requests capabilities but does not authorise itself. The relay is separate from any future business database/backend. Provider replacement must retain the tool and evidence contracts, not promise identical reasoning quality.

## Capability broker

Registration: capability ID/version, description, input/output schemas, execution location, permission scope, side-effect class, timeout/cancellation support and handler identity. A request binds task, candidate, capability version and arguments. Validate schemas, scope and current candidate before dispatch. Return success, rejected, cancelled or failed explicitly, with structured diagnostics.

Read-only inspection, candidate mutation, local simulation and external writes are separate capability classes. Never execute arbitrary code merely because the model supplied it. Optional MCP/research/repository/build providers use configured registrations with the same boundary. External writes require the applicable user authorisation; candidate approval does not automatically grant publishing rights.

Acceptance: unknown tool, invalid arguments and unauthorised side effects are rejected; duplicate request IDs follow declared idempotency semantics; failure cannot be represented as successful evidence.

## Journal and cache

Journal entries: task/step IDs, timestamp, selected context references, candidate IDs, proposed and executed tool calls, decisions, evidence references and unresolved questions. Record attempts separately from outcomes. Resume checks source/candidate freshness before reusing state.

Cache keys include all validity-relevant input and contract versions. Invalidate parsed-source caches when hashes change, and evaluation caches when inputs, rules, runtime or candidate change. A cache hit is an efficiency observation, not a validation result.

## Rules, commands and workflows

Ontology/reasoning supplies meaning; SHACL/domain validators check supported constraints; the versioned evaluator applies policies; XFlow/XState coordinate processes; command handlers enforce permitted transitions.

Decision result: outcome, calculated typed values, reason IDs, missing facts, evaluated policy IDs/versions, applicable context and trace references. Define rule dependencies, conflict resolution, precedence, missing-fact semantics and failure handling per supported evaluator contract. Do not infer those semantics from UI text.

Commands: typed inputs, authority, preconditions, state transition, duplicate handling and errors. Workflow instances reference definition versions, step outcomes and command results. The UI and AI are not the enforcement boundary.

## Evidence and simulation

Evidence: ID, task, baseline/candidate hashes, source/dependency versions, runtime/tool versions, scenario ID/version, synthetic-data marker, input/seed where relevant, observed/expected results, trace references, time perspective and run outcome. Distinguish deterministic expected assertions from exploratory observations.

Acceptance scenario: agreement below, exactly at and above an approval threshold; missing amount; incompatible units/currency according to declared policy; duplicate command; interrupted process where supported. Compare baseline/candidate effects and assert invariants. Associate revised candidates with new results; stale results remain historical.

Browser scenarios do not establish production performance, external integration compatibility or service reliability. Independent repository/build/integration gates retain their own scope.

## Analytical and temporal contracts

Temporal values identify effective intervals and recorded-knowledge intervals/cutoffs with explicit boundary semantics. Corrections preserve the previous knowledge perspective. Relationships may also require temporal identity.

Measures declare ontology identity, grain, numerator/denominator where relevant, units, additivity, supported dimensions/aggregation, period, knowledge cutoff, completeness and evidence references. Bronze/silver/gold processing complements these contracts; it is not supplied by a static site.

## Extraction sequence

1. Inventory actual ChargeWeave definitions and runtime seams from source.
2. Specify the minimal supported interfaces and failure semantics.
3. Exercise a reference journey against those interfaces.
4. Move generic implementations behind the same contracts.
5. Keep EV definitions in the application package.
6. Run parity scenarios in GitHub before adopting the extracted runtime.
7. Exercise another domain package when available to expose hidden assumptions.

No runtime extraction or live AI connection is performed by this website change.
