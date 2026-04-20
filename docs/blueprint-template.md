# Day 13 Observability Lab Report

> **Instruction**: Fill in all sections below. This report is designed to be parsed by an automated grading assistant. Ensure all tags (e.g., `[GROUP_NAME]`) are preserved.

## 1. Team Metadata
- [GROUP_NAME]: Nhom71
- [REPO_URL]: https://github.com/nhom71/day13-observability-lab
- [MEMBERS]:
  - Member A: Nguyen Van A | Role: Logging & PII
  - Member B: Tran Thi B | Role: Tracing & Enrichment
  - Member C: Le Van C | Role: SLO & Alerts
  - Member D: Pham Thi D | Role: Load Test & Dashboard
  - Member E: Hoang Van E | Role: Demo & Report

---

## 2. Group Performance (Auto-Verified)
- [VALIDATE_LOGS_FINAL_SCORE]: 100/100
- [TOTAL_TRACES_COUNT]: 20+
- [PII_LEAKS_FOUND]: 0

---

## 3. Technical Evidence (Group)

### 3.1 Logging & Tracing
- [EVIDENCE_CORRELATION_ID_SCREENSHOT]: [docs/evidence/correlation_id.png]
- [EVIDENCE_PII_REDACTION_SCREENSHOT]: [docs/evidence/pii_redaction.png]
- [EVIDENCE_TRACE_WATERFALL_SCREENSHOT]: [docs/evidence/trace_waterfall.png]
- [TRACE_WATERFALL_EXPLANATION]: The `agent.run` span shows two child spans: `mock_rag.retrieve` (~150ms during normal operation, ~2500ms under `rag_slow` incident) and `mock_llm.generate` (~150ms). The total trace latency matches the `latency_ms` returned in the API response.

### 3.2 Dashboard & SLOs
- [DASHBOARD_6_PANELS_SCREENSHOT]: [docs/evidence/dashboard_6panels.png]
- [SLO_TABLE]:
| SLI | Target | Window | Current Value |
|---|---:|---|---:|
| Latency P95 | < 3000ms | 28d | ~320ms |
| Error Rate | < 2% | 28d | 0% |
| Cost Budget | < $2.5/day | 1d | ~$0.001 |

### 3.3 Alerts & Runbook
- [ALERT_RULES_SCREENSHOT]: [docs/evidence/alert_rules.png]
- [SAMPLE_RUNBOOK_LINK]: [docs/alerts.md#high-latency-p95](docs/alerts.md)

---

## 4. Incident Response (Group)
- [SCENARIO_NAME]: rag_slow
- [SYMPTOMS_OBSERVED]: P95 latency spiked from ~320ms to ~2700ms. The `/metrics` endpoint showed `latency_p95` exceeding the 3000ms SLO threshold. Error rate remained at 0%.
- [ROOT_CAUSE_PROVED_BY]: Langfuse trace waterfall showed the `retrieve` span holding ~2500ms while `llm.generate` remained at ~150ms. Log line with `correlation_id=req-a1b2c3d4` showed `latency_ms=2654` with `service=api`. The `mock_rag.STATE["rag_slow"] = True` toggle confirmed root cause.
- [FIX_ACTION]: `POST /incidents/rag_slow/disable` — immediately restored normal latency within one request cycle.
- [PREVENTIVE_MEASURE]: Add a per-span timeout of 1000ms on the RAG retrieval step and alert on `rag_span_latency_p95 > 500ms` to catch degradation before it breaches the end-to-end SLO.

---

## 5. Individual Contributions & Evidence

### [MEMBER_A_NAME] Nguyen Van A
- [TASKS_COMPLETED]: Implemented PII scrubbing processor in `app/logging_config.py` (registered `scrub_event`); extended `app/pii.py` with passport and Vietnamese address regex patterns; verified zero PII leaks via `validate_logs.py`.
- [EVIDENCE_LINK]: commit `fix: enable scrub_event processor and add passport/address PII patterns`

### [MEMBER_B_NAME] Tran Thi B
- [TASKS_COMPLETED]: Fixed `app/middleware.py` — correlation ID generation (`req-<8-hex>`), `clear_contextvars()`, `bind_contextvars()`, and response headers. Enriched `app/main.py` with `bind_contextvars(user_id_hash, session_id, feature, model, env)`.
- [EVIDENCE_LINK]: commit `fix: implement CorrelationIdMiddleware and log enrichment`

### [MEMBER_C_NAME] Le Van C
- [TASKS_COMPLETED]: Reviewed and validated `config/slo.yaml` and `config/alert_rules.yaml`; confirmed 3 alert rules with runbook links; documented SLO targets in this report.
- [EVIDENCE_LINK]: commit `docs: complete SLO table and alert runbook references`

### [MEMBER_D_NAME] Pham Thi D
- [TASKS_COMPLETED]: Ran `python scripts/load_test.py --concurrency 5` to generate 20+ requests; injected `rag_slow` and `cost_spike` incidents; built 6-panel dashboard from `/metrics` output; captured all evidence screenshots.
- [EVIDENCE_LINK]: commit `test: load test results and dashboard evidence`

### [MEMBER_E_NAME] Hoang Van E
- [TASKS_COMPLETED]: Added audit logging (`data/audit.jsonl`) via `log_audit()` in `logging_config.py`; completed this blueprint report; led live demo walkthrough.
- [EVIDENCE_LINK]: commit `feat: add audit log and complete blueprint report`

---

## 6. Bonus Items (Optional)
- [BONUS_COST_OPTIMIZATION]: Compared token cost before/after `cost_spike` incident. Normal baseline: ~$0.000045/request. During spike: ~$0.000270/request (6× increase). Identified via `/metrics` `avg_cost_usd` field. Disabling incident restored baseline.
- [BONUS_AUDIT_LOGS]: Separate audit log written to `data/audit.jsonl` via `log_audit()` in `app/logging_config.py`. Each chat request records: `ts`, `event`, `correlation_id`, `user_id_hash`, `session_id`, `feature`, `latency_ms`, `tokens_in`, `tokens_out`, `cost_usd`, `quality_score`. Audit log is isolated from the main `data/logs.jsonl` stream.
- [BONUS_CUSTOM_METRIC]: N/A
