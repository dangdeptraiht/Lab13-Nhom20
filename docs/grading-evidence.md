# Evidence Collection Sheet

Use this file as a working checklist during implementation and demo prep.

## 0. Current status snapshot
- Validate logs score: 100/100 (verified locally)
- Core TODO implementation: completed
- Tracing status: enabled (health endpoint shows tracing_enabled = true)
- Langfuse ingestion status: OK (trace count increased after load test)
- Alert drill status: completed for rag_slow, tool_fail, cost_spike with measured metrics
- Remaining work: capture and save all required screenshots to docs/evidence

## 1. Langfuse key setup (for trace evidence)

### Where to get keys
1. Open https://cloud.langfuse.com and sign in.
2. Create or open your project.
3. Go to Project Settings -> API Keys.
4. Create a key pair and copy:
	 - Public key
	 - Secret key

### Add keys to local env
Update .env with:

LANGFUSE_PUBLIC_KEY=<your_public_key>
LANGFUSE_SECRET_KEY=<your_secret_key>
LANGFUSE_HOST=https://us.cloud.langfuse.com

### Verify tracing is enabled
1. Start app.
2. Call GET /health.
3. Confirm tracing_enabled is true.

## 2. Required evidence (must have)

### 2.1 Logging and tracing
- [ ] Langfuse trace list with >= 10 traces
	- Evidence path: docs/evidence/trace-list.png
	- How to capture:
	  1. Open Langfuse -> Tracing.
	  2. Clear all filters.
	  3. Set time range to Last 1 hour.
	  4. Sort by latest and ensure at least 10 rows are visible.
	  5. Capture full table including time and trace names.
- [ ] One full trace waterfall
	- Evidence path: docs/evidence/trace-waterfall.png
	- How to capture:
	  1. Click one recent trace in Tracing list.
	  2. Open detailed trace view with span tree or timeline.
	  3. Capture the full waterfall including latency and child spans.
- [ ] JSON logs showing correlation_id
	- Evidence path: docs/evidence/log-correlation-id.png
	- How to capture:
	  1. Open data/logs.jsonl in editor.
	  2. Find one request_received or response_sent line.
	  3. Ensure correlation_id is visible in the JSON record.
	  4. Capture the line(s) with field names clearly shown.
- [ ] Log line showing PII redaction
	- Evidence path: docs/evidence/log-pii-redaction.png
	- How to capture:
	  1. In data/logs.jsonl search for REDACTED_EMAIL, REDACTED_PHONE_VN, or REDACTED_CREDIT_CARD.
	  2. Capture at least one line proving raw PII was masked.

### 2.2 Dashboard and SLO
- [ ] Dashboard with all 6 panels (latency, traffic, error, cost, tokens, quality)
	- Evidence path: docs/evidence/dashboard-6-panels.png
	- How to capture:
	  1. Show all six panels in one screen if possible.
	  2. Ensure panel titles and units are visible.
	  3. Ensure SLO threshold lines are visible.

### 2.3 Alerts and runbook
- [ ] Alert rules screenshot
	- Evidence path: docs/evidence/alert-rules.png
	- How to capture:
	  1. Open config/alert_rules.yaml and show all 3 rules.
	  2. Capture trigger conditions and severity in one screenshot.
- [ ] Runbook link attached in report
	- Example: docs/alerts.md
	- Suggested link text in report: docs/alerts.md
	- Tested scenarios summary is documented in docs/alerts.md section 4.

## 3. Optional evidence (bonus)
- [ ] Incident before/after fix comparison
	- Evidence path: docs/evidence/incident-before-after.png
- [ ] Cost comparison before/after optimization
	- Evidence path: docs/evidence/cost-before-after.png
	- Suggested proof: compare avg_cost_usd or total_cost_usd from metrics snapshots before and after optimization.
- [ ] Auto-instrumentation or custom script proof
	- Evidence path: docs/evidence/auto-instrumentation.png
- [ ] Separate audit logs proof
	- Evidence path: docs/evidence/audit-log.png

## 4. Capture flow (recommended order)
1. Start app and generate traffic.
2. Capture logs evidence (correlation_id, PII redaction).
3. Confirm tracing_enabled is true via GET /health.
4. Generate 10-20 requests and wait 10-30 seconds for ingestion.
5. Capture trace list and one waterfall.
6. Capture dashboard 6 panels with visible SLO lines.
7. Capture alert rules and runbook link.

## 5. Quick command sheet
1. Start app:
	 C:/Users/nmp10/AppData/Local/Programs/Python/Python312/python.exe -m uvicorn app.main:app --reload --port 8000
2. Verify tracing:
	 Invoke-RestMethod -Uri "http://localhost:8000/health"
3. Generate traffic:
	 C:/Users/nmp10/AppData/Local/Programs/Python/Python312/python.exe scripts/load_test.py --concurrency 5
4. Validate logs:
	 C:/Users/nmp10/AppData/Local/Programs/Python/Python312/python.exe scripts/validate_logs.py
5. Check local logs quickly:
	 Select-String -Path data/logs.jsonl -Pattern "correlation_id|REDACTED" | Select-Object -First 10

## 6. Final handoff checklist
- [ ] docs/blueprint-template.md filled with all group members
- [ ] VALIDATE_LOGS_FINAL_SCORE updated (suggested: 100/100)
- [ ] TOTAL_TRACES_COUNT updated (set from Langfuse trace list screenshot)
- [ ] All required screenshot paths replaced with real files
- [ ] Incident RCA includes concrete evidence (trace id or log lines)

## 8. Alert drill evidence values (copy into report)
Use these values in the Incident Response section and alert analysis:

1. Baseline:
	- latency_p95 = 152.0 ms
	- avg_cost_usd = 0.0020
	- total_cost_usd = 0.0197
	- tokens_out_total = 1245
	- error_breakdown = {}

2. rag_slow enabled:
	- latency_p95 = 2654.0 ms
	- Observation: latency spike confirmed.

3. tool_fail enabled:
	- error_breakdown = {"RuntimeError": 10}
	- Observation: error-rate incident confirmed.

4. cost_spike enabled:
	- avg_cost_usd = 0.0035
	- total_cost_usd = 0.1058
	- tokens_out_total = 6851
	- Observation: cost and token spike confirmed.

## 7. What to fill in blueprint-template now
1. VALIDATE_LOGS_FINAL_SCORE: 100/100
2. PII_LEAKS_FOUND: 0
3. TOTAL_TRACES_COUNT: copy exact number from Langfuse Tracing page at capture time
4. EVIDENCE paths:
	- EVIDENCE_CORRELATION_ID_SCREENSHOT: docs/evidence/log-correlation-id.png
	- EVIDENCE_PII_REDACTION_SCREENSHOT: docs/evidence/log-pii-redaction.png
	- EVIDENCE_TRACE_WATERFALL_SCREENSHOT: docs/evidence/trace-waterfall.png
	- DASHBOARD_6_PANELS_SCREENSHOT: docs/evidence/dashboard-6-panels.png
	- ALERT_RULES_SCREENSHOT: docs/evidence/alert-rules.png
