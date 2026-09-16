# System Requirements Specification (SRS) - AutoTestAgent

**Document Version:** 1.0.0  
**Project Name:** AutoTestAgent (SentinelQA)  
**Target Event:** Hackathon 2026  
**Status:** Approved / Draft Architecture  

---

## 1. Executive Summary & Vision

Traditional software QA relies heavily on superficial metrics like line coverage (e.g., JaCoCo reports). In enterprise environments, teams can easily achieve 80%+ line coverage without actually validating core business invariants, handling concurrent edge cases, or ensuring transactional rollbacks.

**AutoTestAgent** is an intelligent, autonomous testing agent that:
1. Translates natural language requirements (Jira tickets, PRDs, specs) and codebase AST into a **Dual-Dimension Semantic Coverage Matrix** (Business ACs + IT Robustness).
2. Identifies severe blindspots and automatically writes, executes, and self-heals high-value automated test suites on a dedicated branch.
3. Quantifies software robustness with an objective scoring model and delivers dual/comparative executive dashboards illustrating measurable improvements.

---

## 2. User Personas & Target Audience

| Persona | Key Pain Point | AutoTestAgent Solution |
| :--- | :--- | :--- |
| **Product Owner / Business Analyst** | "I don't understand JaCoCo numbers. Are our business acceptance criteria actually verified?" | Generates a plain-English checklist of covered vs. uncovered business ACs directly linked to Jira issues. |
| **Tech Lead / Engineering Lead** | "Junior devs mock out everything just to pass CI gates. High coverage, but production bugs persist." | Flags shallow assertions, missing rollback tests, unhandled NPEs, and concurrency blindspots. |
| **Software Engineer** | "Writing comprehensive integration and edge-case mocks takes 40% of my sprint time." | Auto-generates compilable, passing unit/integration tests on a new branch with ready-to-merge PRs. |
| **Hackathon Judges / Leadership** | "We need demonstrable, explainable AI impact in the DevSecOps lifecycle." | Provides interactive, aesthetically pleasing dual dashboards and clear robustness score deltas. |

---

## 3. Functional Requirements (FR)

### FR-1: Repository & Requirement Ingestion
- **FR-1.1**: The Agent MUST accept a public/private GitHub repository URL and target branch.
- **FR-1.2**: The Agent MUST accept an optional Jira Issue ID (or Jira API endpoint/token) or fallback to local repository documentation (`README.md`, `docs/`, `spec.md`, OpenAPI/Swagger definitions).
- **FR-1.3**: The Agent MUST parse repository structure, identifying primary programming language (Java / Spring Boot or Python / FastAPI), build tool (`pom.xml`, `build.gradle`, `pyproject.toml`), and existing test suites (`src/test/...`, `tests/...`).

### FR-2: Dual-Dimension Semantic Coverage Analysis
- **FR-2.1 Business Requirement Traceability**:
  - Extract Acceptance Criteria (ACs) and business domain rules from requirements.
  - Correlate each AC with existing test cases using semantic vector/LLM reasoning.
  - Produce a structured, itemized checklist: `[AC_ID] - Description - Status (COVERED / PARTIAL / MISSING) - Linked Test Method`.
- **FR-2.2 Technical & Edge-Case Robustness**:
  - Scan business logic classes (e.g., Services, Controllers, Adapters) for unhandled fault paths:
    - Null / Empty / Boundary input conditions.
    - Upstream service failure / Timeout / Circuit breaking.
    - Transactional rollback on exception (e.g., `@Transactional` failure paths).
    - Idempotency & concurrent modification.
  - Flag critical gaps: `[CRITICAL_BLINDSPOT] TransferService: Concurrent debit without row-level lock check`.

### FR-3: Autonomous Test Generation & Verification Sandbox
- **FR-3.1 Branch Management**:
  - Create a new Git branch named `agent/test-enhancement-<timestamp>`.
- **FR-3.2 Test Synthesis**:
  - Generate idiomatic test code matching the repository's native framework (e.g., JUnit 5 + Mockito / AssertJ or PyTest).
  - Include realistic mocking, test fixtures, and strict assertions on both output state and exceptions.
- **FR-3.3 Self-Healing Execution Loop**:
  - Run the generated tests in a sandboxed CLI environment (`mvn test -Dtest=...` or `pytest ...`).
  - If tests fail (compile error, wrong mock, failed assertion):
    - Capture compiler diagnostics or failure stack trace.
    - Provide the error context back to the LLM for self-correction.
    - Retry execution (capped at 3 iterations) until the build passes (Green).
- **FR-3.4 Automated Pull Request**:
  - Commit verified green test suites to the enhancement branch and push to the remote repository.

### FR-4: Dual Branch Robustness Dashboards & Comparative Analytics
- **FR-4.1 Robustness Scoring Model (RSM)**:
  - Aggregate coverage into an objective score from 0 to 100:
    - **Business AC Coverage (Weight: 40%)**: Ratio of verified ACs to total extracted ACs.
    - **Edge & Resilience Defense (Weight: 35%)**: Proportion of boundary/exception handling paths tested.
    - **Assertion Quality & Mutation Depth (Weight: 25%)**: Ratio of meaningful assertions vs. trivial status checks.
- **FR-4.2 Single-Branch Dashboard**:
  - Display Overall Robustness Score, category radar chart, and itemized AC/IT audit table.
- **FR-4.3 Comparative Diff Dashboard**:
  - Side-by-side view: **Original Branch (Before) vs. Agent Branch (After)**.
  - Metric deltas: Score increase, newly secured business rules, eliminated risk vectors.
  - Interactive test suite viewer showing generated test methods and verification logs.

---

## 4. Non-Functional Requirements (NFR)

- **NFR-1 (Aesthetic & Polish)**: Dashboards must use a modern dark/light executive UI (Tailwind CSS, Glassmorphism, smooth radar/bar animations) suitable for live hackathon presentations.
- **NFR-2 (Determinism & Safety)**: The Agent will NEVER alter production business code; all changes are strictly isolated to `src/test/` on a new feature branch.
- **NFR-3 (Execution Speed)**: Analysis and test generation for a medium-sized service (5-10 service classes) must complete within 3-5 minutes.
- **NFR-4 (Extensibility)**: Modular architecture allowing additional LLM backends (OpenAI, Gemini, Anthropic) and build systems.

---

## 5. System Architecture & Component Design

```
+----------------------------------------------------------------------------------------------------+
|                                      System Architecture                                           |
|                                                                                                    |
|  [React Web UI (Browser)]                                                                          |
|         │ (POST /api/v1/scan)                                                                      |
|         ▼                                                                                          |
|  ┌──────────────────────────────────────────────────────────────────────────────────────────────┐  |
|  │                        FastAPI Backend & Orchestration Engine                                │  |
|  │                                                                                              │  |
|  │  ┌───────────────────────┐   ┌───────────────────────────────┐   ┌────────────────────────┐  │  |
|  │  │  1. Repo & Doc Parser │   │ 2. Dual-Dimension Evaluator   │   │ 3. Self-Healing Engine  │  │  |
|  │  │  - Git Ingest         │   │ - Business AC Extraction      │   │ - Branch checkout      │  │  |
|  │  │  - AST / File Mapper  │   │ - Semantic Coverage Mapper    │   │ - Test code synthesizer│  │  |
|  │  │  - Jira Connector     │   │ - Robustness Scorer (0-100)   │   │ - Maven Sandbox Runner │  │  |
|  │  └───────────────────────┘   └───────────────────────────────┘   │ - Reflection loop      │  │  |
|  │                                                                  └────────────────────────┘  │  |
|  └──────────────────────────────────────────────────────────────────────────────────────────────┘  |
|         │                                                                                          |
|         ▼ (SSE Real-time Stream & JSON Report API)                                                 |
|  ┌──────────────────────────────────────────────────────────────────────────────────────────────┐  |
|  │                               React Executive Dashboard UI                                   │  |
|  │  - Base Branch Health & Radar Analysis                                                       │  |
|  │  - Enhanced Branch Score Delta (+X Points)                                                   │  |
|  │  - Interactive Side-by-Side Comparison (Blindspots Eliminated, Generated Tests, PR Link)     │  |
|  └──────────────────────────────────────────────────────────────────────────────────────────────┘  |
+----------------------------------------------------------------------------------------------------+
```

---

## 6. Deliverables & Hackathon Roadmap

1. **Sprint 1: Core Repo & Documentation Setup** (Current)
   - Public repository initialized: `nvd11/auto-test-agent`.
   - Complete SRS and Architecture specification committed.
2. **Sprint 2: Evaluator & Scoring Engine (MVP Core)**
   - AST parser for test & business code.
   - LLM-powered AC extraction & dual-matrix generator.
3. **Sprint 3: Sandbox Runner & Self-Healing Loop**
   - Headless test execution (`mvn test` / `pytest`).
   - Error log parser & 1-shot repair mechanism.
4. **Sprint 4: Executive Comparative Dashboard**
   - Modern, interactive HTML/React dashboard with before/after radar charts and diff analytics.
5. **Sprint 5: End-to-End Showcase Demo**
   - Live demo repo featuring intentional business blindspots, showcasing automated detection, self-healing test PR, and the dashboard.
