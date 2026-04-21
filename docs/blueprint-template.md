# Day 13 Observability Lab Report

> **Instruction**: Fill in all sections below. This report is designed to be parsed by an automated grading assistant. Ensure all tags (e.g., `[GROUP_NAME]`) are preserved.

## 1. Team Metadata
- [GROUP_NAME]: Nhom20
- [REPO_URL]: https://github.com/dangdeptraiht/Lab13-Nhom20.git
- [MEMBERS]:
  - Member A: arthur105204 | Role: Logging & PII
  - Member B: arthur105204 | Role: Tracing & Enrichment
  - Member C: dangdeptraiht | Role: SLO & Alerts
  - Member D: Tin Duong | Role: Load Test & Dashboard
  - Member E: Ngo Van Long | Role: Demo & Report

---

## 2. Group Performance (Auto-Verified)
- [VALIDATE_LOGS_FINAL_SCORE]: 100/100
- [TOTAL_TRACES_COUNT]: >10
- [PII_LEAKS_FOUND]: 0

---

## 3. Technical Evidence (Group)

### 3.1 Logging & Tracing
- [EVIDENCE_CORRELATION_ID_SCREENSHOT]: docs/evidence/correlation-id.png
- [EVIDENCE_PII_REDACTION_SCREENSHOT]: docs/evidence/redacted.png
- [EVIDENCE_TRACE_WATERFALL_SCREENSHOT]: docs/evidence/full-trace.png
- [TRACE_WATERFALL_EXPLANATION]: The trace waterfall shows the full execution of the request, identifying individual spans for the agent, the retrieval component (`rag`), and the LLM generation. It correctly propagates the session trace and helps visualize timing bottlenecks.

### 3.2 Dashboard & SLOs
- [DASHBOARD_6_PANELS_SCREENSHOT]: docs/evidence/dashboard.png
- [SLO_TABLE]:
| SLI | Target | Window | Current Value |
|---|---:|---|---:|
| Latency P95 | < 3000ms | 28d | 152.0 ms |
| Error Rate | < 2% | 28d | 0% |
| Cost Budget | < $2.5/day | 1d | $0.0197 |

### 3.3 Alerts & Runbook
- [ALERT_RULES_SCREENSHOT]: docs/evidence/alert.png
- [SAMPLE_RUNBOOK_LINK]: docs/alerts.md#L41

---

## 4. Incident Response (Group)
- [SCENARIO_NAME]: rag_slow
- [SYMPTOMS_OBSERVED]: P95 latency spiked from 152.0 ms to 2654.0 ms. Total cost slightly increased.
- [ROOT_CAUSE_PROVED_BY]: `rag_slow` incident toggle was enabled, identified via slow retrieval span in trace.
- [FIX_ACTION]: Disable `rag_slow` toggle in incidents configuration.
- [PREVENTIVE_MEASURE]: Set timeout on retrieval API and implement fallback retrieval source.

---

## 5. Individual Contributions & Evidence

### arthur105204
- [TASKS_COMPLETED]: Implemented logging PII redaction and tracing tags.
- [EVIDENCE_LINK]: commit 98bd99e and 8e20b17

### arthur105204
- [TASKS_COMPLETED]: Handled Tracing and enrichment.
- [EVIDENCE_LINK]: commit 8e20b17

### dangdeptraiht
- [TASKS_COMPLETED]: Handled SLO & Alerts rules configuration.
- [EVIDENCE_LINK]: commit 9ba56c2

### Tin Duong
- [TASKS_COMPLETED]: Set up template, dashboard metrics structure and load testing baseline.
- [EVIDENCE_LINK]: commit e3735b0

### Ngo Van Long
- [TASKS_COMPLETED]: Collected demo evidence and initiated the report.
- [EVIDENCE_LINK]: commit 62a94be

---

## 6. Bonus Items (Optional)
- [BONUS_COST_OPTIMIZATION]: N/A
- [BONUS_AUDIT_LOGS]: N/A
- [BONUS_CUSTOM_METRIC]: N/A
