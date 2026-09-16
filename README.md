# AutoTestAgent (SentinelQA) 🛡️🤖

> **Autonomous AI Agent for Semantic Quality Assurance, Self-Healing Test Generation & Comparative Robustness Analytics**

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Hackathon](https://img.shields.io/badge/Hackathon-2026-brightgreen.svg)](#)
[![Status](https://img.shields.io/badge/Status-Architecture%20%26%20Design-orange.svg)](#)

---

## 📖 1. Project Background & Motivation

In enterprise software engineering (especially within high-stakes domains like Financial Technology, Banking, and Regulatory Systems), **code quality and regression safety** are paramount. However, traditional automated testing practices face four major bottlenecks:

1. **The "JaCoCo Illusion" (Cold & Misleading Metrics)**: Traditional line/branch coverage tools (e.g., JaCoCo, Cobertura) provide sterile numbers. An 85% line coverage report often conceals the fact that tests are merely calling getters/setters or mocking out critical paths without asserting actual business rules.
2. **Business vs. Tech Disconnect**: Unit and integration tests rarely map back to real **Business Requirements** (User Stories, Acceptance Criteria in Jira/PRDs). Engineers and managers struggle to answer: *"Is our critical overdraft calculation or sanction screening rule actually tested?"*
3. **Passive Reporting without Remediation**: Traditional linters and QA tools complain about missing tests or untested branches, but they burden developers with tedious manual test scripting.
4. **Lack of Executive-Level Quality Visibility**: Reviewers, POs, and Tech Leads lack intuitive, side-by-side comparative dashboards showing how a new PR/branch actually bolsters the system's real-world robustness.

**AutoTestAgent** transforms testing from a passive check into an **autonomous, proactive engineering partner**.

---

## 🎯 2. Core Capabilities & Value Proposition

Given a **GitHub Repository URL** and an optional **Jira Issue ID / Requirement Doc**, AutoTestAgent executes an end-to-end autonomous QA workflow:

```
+---------------------------------------------------------------------------------------------------+
|                                       AutoTestAgent Flow                                          |
|                                                                                                   |
|  [User via React Web UI]                                                                          |
|          │ (Repo URL + optional Jira ID)                                                          |
|          ▼                                                                                        |
|  +--------------------+       +------------------------------------+       +-------------------+  |
|  | Context Ingestion  | ----> | Dual-Dimension Semantic Coverage   | ----> | Major Gap         |  |
|  | (Code AST + ACs)   |       | (Business Matrix + IT Edge Cases)  |       | Identification    |  |
|  +--------------------+       +------------------------------------+       +-------------------+  |
|                                                                                      |            |
|                                                                                      v            |
|  +--------------------+       +------------------------------------+       +-------------------+  |
|  | Comparative        | <---- | Execution Sandbox Validation       | <---- | Autonomous Test   |  |
|  | React Dashboard    |       | (mvn test compile & test loop)     |       | Generation (Branch|  |
|  +--------------------+       +------------------------------------+       +-------------------+  |
|          ▲                                                                                        |
|          └──────────────── SSE Streaming (Real-time Agent Progress) ─────────────────────────────┘  |
+---------------------------------------------------------------------------------------------------+
```

### 1. Dual-Dimension Semantic Coverage (IT & Business)
Instead of cold line percentages, AutoTestAgent evaluates code across two human-readable dimensions:
- **Business Dimension (Acceptance Criteria Traceability)**: Parses requirements from Jira or repository specs, extracts business assertions, and maps them to existing test scenarios item-by-item.
- **IT & Robustness Dimension**: Identifies critical boundary and resilience gaps (e.g., `Null/Empty Payloads`, `Timeout & Retry Scenarios`, `Transaction Rollback under Concurrent Failures`, `Idempotency Violations`).
- **High-Readability Output**: Renders itemized checklists with clear statuses (e.g., `[COVERED]`, `[PARTIAL]`, `[CRITICAL_BLINDSPOT]`).

### 2. Autonomous Remediation & Self-Healing Execution Loop
When critical test coverage gaps are identified:
- **Autonomous Branching**: Automatically spins up an enhancement branch (e.g., `agent/test-enhancement-<timestamp>`).
- **Targeted Test Generation**: Synthesizes idiomatic, maintainable unit/integration tests (JUnit 5 + Mockito, SpringBootTest, or PyTest) complete with realistic fixtures and edge-case mocks.
- **Verification Sandbox**: Executes the test suite in a containerized build environment (`mvn test`, `gradle test`, or `pytest`).
- **Self-Healing Reflection**: If compilation fails or assertions break, the Agent inspects the stack trace, adjusts mocking/imports, and iterates until the build is green before committing.

### 3. Dual Robustness Dashboards & Comparative Analytics
- **Single-Branch Robustness View**: Calculates an explainable **Robustness Score (0-100)** with clear criteria weightings:
  - Business AC Alignment (40%)
  - Resilience & Edge Defenses (35%)
  - Assertion Efficacy (25%)
- **Side-by-Side Comparative View**: Generates a visually striking Diff Dashboard comparing the `Original Branch` vs. the `Enhanced Branch`:
  - Score Delta (e.g., `61 -> 89 (+28)`)
  - Blindspots eliminated (visual radar chart and checklist)
  - Added test suites and verified execution logs
  - One-click GitHub Pull Request creation link

---

## 🏗️ 3. Architecture & Functional Specification

Detailed architectural specifications, data models, and prompt workflows are maintained in:
- [System Requirements Specification (SRS)](docs/REQUIREMENTS.md)

---

## 👥 4. Team & Hackathon Information

- **Team**: Hackathon 2026 Team
- **Repository**: [https://github.com/nvd11/auto-test-agent](https://github.com/nvd11/auto-test-agent)
- **Primary Focus**: Autonomous SDLC Agents, DevSecOps, Enterprise Quality Assurance

---

## 📄 License
This project is open-source under the [MIT License](LICENSE).
