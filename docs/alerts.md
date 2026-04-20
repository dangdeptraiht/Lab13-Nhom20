# Alert Rules and Runbooks

## 1. High latency P95
- Severity: P2
- Trigger: `latency_p95_ms > 5000 for 30m`
- Impact: tail latency breaches SLO
- First checks:
  1. Open top slow traces in the last 1h
  2. Compare RAG span vs LLM span
  3. Check if incident toggle `rag_slow` is enabled
- Mitigation:
  - truncate long queries
  - fallback retrieval source
  - lower prompt size

## 2. High error rate
- Severity: P1
- Trigger: `error_rate_pct > 5 for 5m`
- Impact: users receive failed responses
- First checks:
  1. Group logs by `error_type`
  2. Inspect failed traces
  3. Determine whether failures are LLM, tool, or schema related
- Mitigation:
  - rollback latest change
  - disable failing tool
  - retry with fallback model

## 3. Cost budget spike
- Severity: P2
- Trigger: `hourly_cost_usd > 2x_baseline for 15m`
- Impact: burn rate exceeds budget
- First checks:
  1. Split traces by feature and model
  2. Compare tokens_in/tokens_out
  3. Check if `cost_spike` incident was enabled
- Mitigation:
  - shorten prompts
  - route easy requests to cheaper model
  - apply prompt cache
# Alert Rules and Runbooks

## 1. High latency P95
- Severity: P2
- Trigger: `latency_p95_ms > 5000 for 30m`
- Impact: tail latency breaches SLO
- First checks:
  1. Open top slow traces in the last 1h
  2. Compare RAG span vs LLM span
  3. Check if incident toggle `rag_slow` is enabled
- Mitigation:
  - truncate long queries
  - fallback retrieval source
  - lower prompt size

## 2. High error rate
- Severity: P1
- Trigger: `error_rate_pct > 5 for 5m`
- Impact: users receive failed responses
- First checks:
  1. Group logs by `error_type`
  2. Inspect failed traces
  3. Determine whether failures are LLM, tool, or schema related
- Mitigation:
  - rollback latest change
  - disable failing tool
  - retry with fallback model

## 3. Cost budget spike
- Severity: P2
- Trigger: `hourly_cost_usd > 2x_baseline for 15m`
- Impact: burn rate exceeds budget
- First checks:
  1. Split traces by feature and model
  2. Compare tokens_in/tokens_out
  3. Check if `cost_spike` incident was enabled
- Mitigation:
  - shorten prompts
  - route easy requests to cheaper model
  - apply prompt cache

---

## 4. Lab Test Evidence (2026-04-20)

The team executed all 3 incident scenarios and captured metrics from GET /metrics.

### Baseline (all incidents disabled)
- traffic: 10
- latency_p95: 152.0 ms
- avg_cost_usd: 0.0020
- total_cost_usd: 0.0197
- tokens_out_total: 1245
- error_breakdown: {}

### Scenario A: rag_slow enabled (High latency)
- traffic: 20
- latency_p95: 2654.0 ms (increased strongly vs baseline)
- avg_cost_usd: 0.0020
- total_cost_usd: 0.0393
- tokens_out_total: 2487
- error_breakdown: {}

### Scenario B: tool_fail enabled (High error rate)
- traffic: 20
- latency_p95: 2654.0 ms
- avg_cost_usd: 0.0020
- total_cost_usd: 0.0393
- tokens_out_total: 2487
- error_breakdown: {"RuntimeError": 10}

### Scenario C: cost_spike enabled (Cost spike)
- traffic: 30
- latency_p95: 2653.0 ms
- avg_cost_usd: 0.0035 (increased vs baseline)
- total_cost_usd: 0.1058 (increased vs baseline)
- tokens_out_total: 6851 (increased strongly vs baseline)
- error_breakdown: {"RuntimeError": 10}

### Notes
- Metrics are cumulative in-memory counters, so values increase across phases.
- error_breakdown persists after Scenario B because counters are not reset automatically.
