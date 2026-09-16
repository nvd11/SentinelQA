# System Architecture & Technical Implementation Document
**Project Name:** AutoTestAgent (SentinelQA)  
**Target Event:** Hackathon 2026  
**Architecture Style:** Decoupled Client-Server (React Frontend + FastAPI Backend)  
Implementation Language: Python 3.12 (FastAPI & LangChain Agent Core, pip-managed) + TypeScript / React (Web Dashboard)
**Target Testbeds:** Java 17/21 + Spring Boot (Maven / JUnit 5)  
**Document Version:** 1.1.0  
**Status:** Approved / In-Development  

---

## 1. Architectural Overview & Design Philosophy

AutoTestAgent adopts a **Decoupled Full-Stack Web Architecture** (`React Frontend + FastAPI Backend`). This design replaces traditional cold CLI commands with an intuitive, executive-friendly, and interactive Web application designed specifically for high-impact live demos and enterprise usability.

### Core Tenets:
1. **Decoupled Client-Server Model**:
   - **Frontend (React + Tailwind CSS + Lucide Icons + Recharts)**: Handles user input (Target GitHub Repo URL, optional Jira ID, and optional Coding Standard Repo URL), renders real-time streaming agent thoughts/progress, and presents side-by-side comparative dashboards.
   - Backend (FastAPI + Async Python 3.12, pip, LangChain Agent): Orchestrates Git operations for both target codebase and coding standards, AST parsing, LLM prompt pipelines, Maven CLI sandbox execution, and SSE (Server-Sent Events) streaming.
- Configuration Management: Standardized via `.env-template` supporting multi-environment setup (local, dev, prod).
2. **Zero Production Mutation**: The agent strictly operates within `src/test/java/...` on an isolated Git branch (`agent/test-enhancement-*`).
3. **Deterministic Execution Sandbox**: All generated JUnit tests must achieve `BUILD SUCCESS` under `mvn test` before committing.
4. **Multi-Lens Quality Metrics**: Evaluates Business Acceptance Criteria (AC traceability), Technical Robustness (concurrency, null-checks, rollbacks), and Department Coding Standard Compliance.

---

## 2. End-to-End System Architecture (Mermaid)

```mermaid
flowchart TB
    subgraph Frontend["1. Frontend Layer (React + Vite + Tailwind)"]
        UI_Input["Repo & Context Input Console\n(Target Repo URL, Branch, Jira ID, Coding Standard Repo)"]
        UI_Stream["Real-time Agent Thought Stream\n(SSE / WebSocket Listener)"]
        UI_Dashboard["Multi-Branch Comparative Dashboard\n(Radar Chart, Diff View, Score Deltas)"]
    end

    subgraph APILayer["2. API & Orchestration Layer (FastAPI Backend)"]
        API_Endpoints["REST Endpoints (/api/v1/scan, /api/v1/report)"]
        SSE_Broadcaster["Event Stream Broadcaster (SSE)"]
        Task_Orchestrator["Agent Workflow Orchestrator"]
    end

    subgraph AgentCore["3. Agent Core Modules (Python)"]
        Git_Mgr["Git Manager\n(Clone, Branch, Commit, PR)"]
        Doc_Parser["Jira / Spec Ingestor\n(AC & Rule Extraction)"]
        Std_Parser["Coding Standard Ingestor\n(Rulebook & Convention Parser)"]
        AST_Parser["Java AST Parser\n(tree-sitter-java)"]
        Evaluator["Multi-Dimension Evaluator\n(Business AC, IT Edge-Cases, Coding Standards)"]
        Healer["Self-Healing Test Synthesizer\n(JUnit 5 + Mockito, Standards-Compliant)"]
    end

    subgraph Sandbox["4. Execution Sandbox (Local JVM / Docker)"]
        Maven_Runner["Maven CLI Runner\n(mvn test -Dtest=...)"]
        Log_Inspector["Error Trace & Compiler Diagnostics"]
    end

    %% Interactions
    UI_Input -->|POST /api/v1/scan| API_Endpoints
    API_Endpoints --> Task_Orchestrator
    Task_Orchestrator -->|Progress Events| SSE_Broadcaster
    SSE_Broadcaster -->|Live Stream| UI_Stream

    Task_Orchestrator --> Git_Mgr & Doc_Parser & Std_Parser & AST_Parser
    Doc_Parser & Std_Parser & AST_Parser --> Evaluator
    Evaluator -->|Baseline Score| Task_Orchestrator
    
    Task_Orchestrator --> Healer
    Healer -->|Write Test File| Maven_Runner
    Maven_Runner -->|BUILD FAILURE Log| Log_Inspector
    Log_Inspector -->|Reflection Loop| Healer
    Maven_Runner -->|BUILD SUCCESS| Git_Mgr
    
    Git_Mgr -->|Push & Diff| Task_Orchestrator
    Task_Orchestrator -->|Enhanced Score & Comparison JSON| API_Endpoints
    API_Endpoints -->|Render Metrics| UI_Dashboard

    classDef fe fill:#e0f7fa,stroke:#00838f,stroke-width:2px;
    classDef api fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px;
    classDef core fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px;
    classDef sb fill:#fff3e0,stroke:#e65100,stroke-width:2px;

    class Frontend fe;
    class APILayer api;
    class AgentCore core;
    class Sandbox sb;
```

---

## 3. Real-Time Interaction & Self-Healing Sequence (Mermaid)

```mermaid
sequenceDiagram
    autonumber
    actor User as Judge / Developer
    participant UI as React Frontend
    participant API as FastAPI Backend
    participant Agent as Agent Orchestrator
    participant MVN as Maven Sandbox
    participant GH as Remote GitHub Repo

    User->>UI: Enter Repo URL, Jira ID & Coding Standard Repo -> Click "Start Analysis"
    UI->>API: POST /api/v1/scan
    API-->>UI: Subscribe to SSE stream (/api/v1/stream/{job_id})
    
    Agent->>GH: Clone Target Repo & Optional Coding Standard Repo
    Agent->>UI: SSE: "Extracting Java AST, Jira Acceptance Criteria & Department Coding Standards..."
    
    Agent->>Agent: Run Multi-Dimension Evaluation (Baseline Score: 58)
    Agent->>UI: SSE: "Baseline evaluated. Score: 58/100. 3 Critical Blindspots & 2 Standard Violations detected."

    Agent->>GH: Checkout new branch `agent/test-enhancement-*`
    Agent->>UI: SSE: "Synthesizing JUnit 5 tests for AccountTransferService..."
    
    Agent->>MVN: Execute `mvn test -Dtest=AccountTransferServiceTest`
    MVN-->>Agent: BUILD FAILURE (Missing Mock for CurrencyRateService)
    Agent->>UI: SSE: "Compilation failure detected. Self-healing iteration 1/3..."
    
    Agent->>Agent: Reflection & Patch Mocking Setup
    Agent->>MVN: Re-execute `mvn test -Dtest=AccountTransferServiceTest`
    MVN-->>Agent: BUILD SUCCESS (All tests passed)
    Agent->>UI: SSE: "Tests verified green! Committing and pushing to remote branch..."
    
    Agent->>GH: Git Commit & Git Push
    Agent->>Agent: Re-evaluate Enhanced Branch (Score: 89)
    Agent->>UI: SSE: "Task completed! Comparative report ready."
    API-->>UI: Return Full Comparative JSON Payload
    UI->>User: Display Interactive Before vs After Dashboard + PR Link
```

---

## 4. Subsystem Detailed Specifications

### 4.1 Frontend Architecture (`web/`)
- **Technology Stack**: React 18, Vite, TypeScript, Tailwind CSS, Recharts (for radar and score trend charts), Lucide-React icons.
- **Views**:
  1. **Workbench / Launcher**: Clean, dark-themed hero console with Target GitHub URL, branch selection, optional Jira ticket input, and optional Department Coding Standard GitHub URL.
  2. **Agent Live Console**: Terminal-style animated thought stream showing live tool invocations, standard rulebook ingestion, and self-healing iterations.
  3. **Comparative Dashboard**:
     - Score Delta banner (e.g., `58 -> 89 (+31)`).
     - 5-Axis Radar Chart (Business ACs, Concurrency/Locking, Boundary/Null, Coding Standard Compliance, Assertion Depth).
     - Itemized Acceptance Criteria Traceability Checklist & Coding Standard Audit.
     - Side-by-side Test Coverage Diff and Verified Execution Log.

### 4.2 Backend API Architecture (`server/` & `sentinel_qa/`)
- **Technology Stack**: FastAPI, Uvicorn, Pydantic v2, LiteLLM / Google GenAI SDK, LangChain.
- **Key Endpoints**:
  - `POST /api/v1/scan`: Accepts `{ repo_url: str, branch: str, jira_id: Optional[str], standard_repo_url: Optional[str] }`, initializes asynchronous background task, returns `job_id`.
  - `GET /api/v1/stream/{job_id}`: Server-Sent Events (SSE) streaming progress milestones, standard ingestion, and agent logs.
  - `GET /api/v1/report/{job_id}`: Returns complete comparative report JSON for dashboard rendering.

### 4.3 Agent Core & Self-Healing Engine
- **AST Parsing (`core/java_ast.py`)**: Uses `tree-sitter-java` to extract classes, methods, annotations (`@Transactional`, `@Valid`), and existing test methods.
- **Coding Standard Ingestor (`engine/coding_standard_client.py`)**: Clones and indexes department-level coding guidelines (e.g., test naming patterns, required assertion libraries like AssertJ, structure guidelines, exception handling patterns).
- **Evaluation Engine (`core/evaluator.py`)**: Implements the 4-pillar scoring model:
  $$\text{Score} = (0.35 \times S_{\text{Business}}) + (0.35 \times S_{\text{Resilience}}) + (0.15 \times S_{\text{Standards}}) + (0.15 \times S_{\text{Assertion}})$$
- **Self-Healing Loop (`core/self_healer.py`)**: Subprocess runner executing `mvn test`. Captures stack traces, triggers LLM reflection (max 3 tries), and ensures 100% green builds adhering to department guidelines before commit.

---

## 5. Repository Directory Layout

```
auto-test-agent/
├── README.md                           # Project homepage & mission
├── docs/
│   ├── REQUIREMENTS.md                 # System Requirements Specification (SRS)
│   └── ARCHITECTURE.md                 # Full-Stack System Architecture Document
├── web/                                # React Frontend Web App (Vite + TypeScript)
│   ├── package.json
│   ├── vite.config.ts
│   └── src/
│       ├── components/                 # Radar chart, diff table, stream console
│       ├── pages/                      # Launcher page, Dashboard page
│       └── App.tsx
├── backend/                            # FastAPI Backend (Following python-template-v2)
│   ├── requirements.txt                # Standard pip dependencies (Python 3.12 + pip)
│   ├── Dockerfile
│   ├── src/
│   │   ├── __init__.py
│   │   ├── main.py                     # Entry point for local/dev runner
│   │   ├── server.py                   # FastAPI app factory, CORS, lifespan
│   │   ├── configs/                    # Multi-environment configuration system
│   │   │   ├── __init__.py
│   │   │   ├── config.py               # Pydantic Settings, YAML loader, APP_ENVIRONMENT
│   │   │   ├── config_local.yaml       # Local dev config (proxy, debug logs)
│   │   │   ├── config_dev.yaml         # Dev environment config
│   │   │   ├── config_prod.yaml        # Prod environment config
│   │   │   ├── log_config.py           # Loguru config (GCP JSON in prod, color in dev)
│   │   │   └── proxy.py                # Local proxy helpers
│   │   ├── models/                     # Request/Response schemas & domain entities
│   │   │   ├── __init__.py
│   │   │   ├── requests.py             # ScanRequest (repo_url, branch, jira_id, standard_repo_url)
│   │   │   ├── responses.py            # ScanResponse, StreamEvent, ReportResponse
│   │   │   └── domain.py               # AcceptanceCriteria, CodingStandardRule, RobustnessScore, DiffMatrix
│   │   ├── routers/                    # FastAPI route controllers
│   │   │   ├── __init__.py
│   │   │   ├── health.py               # Health check endpoint (/health)
│   │   │   ├── scan.py                 # Scan triggers & SSE streaming (/api/v1/scan, /api/v1/stream)
│   │   │   └── report.py               # Comparative report endpoints (/api/v1/report)
│   │   ├── services/                   # Business & orchestrator services
│   │   │   ├── __init__.py
│   │   │   └── scan_service.py         # Async task coordinator & SSE event emitter
│   │   ├── llm/                        # LLM provider clients, prompt templates & token handling
│   │   │   ├── __init__.py
│   │   │   ├── client.py               # LiteLLM / Gemini client wrapper & fallback handling
│   │   │   └── prompts.py              # Prompt templates for evaluation, synthesis & reflection
│   │   ├── agent/                      # Core agent workflows, state machines & self-healing
│   │   │   ├── __init__.py
│   │   │   ├── orchestrator.py         # Autonomous workflow controller
│   │   │   ├── evaluator.py            # Dual-dimension semantic evaluator
│   │   │   ├── synthesizer.py          # JUnit 5 & Mockito test generator
│   │   │   └── self_healer.py          # Test runner & feedback reflection loop
│   │   ├── engine/                     # Toolings, parsers & sandbox execution runners
│   │   │   ├── __init__.py
│   │   │   ├── git_client.py           # Git operations (clone, branch, commit, push)
│   │   │   ├── jira_client.py          # Jira API & fallback doc extractor
│   │   │   ├── coding_standard_client.py # Department Coding Standard repository fetcher & indexer
│   │   │   ├── java_ast_parser.py      # tree-sitter Java AST parser
│   │   │   └── maven_sandbox.py        # Subprocess `mvn test` execution & reflection loop
│   │   └── utils/                      # Shared helpers
│   │       ├── __init__.py
│   │       ├── path_utils.py           # Project & workspace directory helpers
│   │       └── validators.py           # Git URL & Jira ID sanitizers
│   └── test/                           # Pytest suite for backend
├── testbeds/                           # Demonstrative Java Sandboxes
│   └── spring-banking-demo/            # Target Spring Boot service with deliberate blindspots
└── cloudbuild.yaml                     # GCP Cloud Build pipeline for deploying to Cloud Run
```

---

## 6. Technology Stack Summary

| Component | Technology | Rationale |
| :--- | :--- | :--- |
| **Frontend Framework** | React 18 + Vite (TypeScript) | High performance, rapid component assembly, and rich charting ecosystem. |
| **Styling & Icons** | Tailwind CSS + Lucide Icons | Modern, sleek dark-mode aesthetic suitable for executive presentations. |
| **Backend API** | FastAPI (Python 3.12, pip) | Native async support, auto-generated OpenAPI docs, and lightweight SSE streaming. |
| **Agent Logic** | Python 3.12 + Pydantic v2 | Unmatched speed of iteration, AST extraction, and strict JSON validation. Managed via pip. |
| **Java AST Extraction** | `tree-sitter` (`tree-sitter-java`) | High-speed C-native syntax tree parsing without JVM dependency. |
| **Target Testbed** | Java 17/21 + Spring Boot + Maven | Standard enterprise financial technology stack. |
| **Real-time Protocol** | Server-Sent Events (SSE) | Lightweight, unidirectional live event streaming for agent progress. |
