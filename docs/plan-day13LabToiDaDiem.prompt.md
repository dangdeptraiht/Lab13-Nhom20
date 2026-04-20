## Plan: Day 13 Lab Toi Da Diem
Hoan thanh nhanh cac TODO bat buoc de vuot cong diem (validate >=80), sau do mo rong dashboard-alert-incident-evidence de toi da diem nhom va diem ca nhan. Cach lam uu tien theo critical path, nhung tach cac viec co the song song theo role nhom.

**Steps**
1. Phase 1 - Baseline va chia vai tro (blocking):
1.1. Chay baseline hien trang de chup moc ban dau: khoi dong app, gui traffic mau, chay validate logs, chup diem baseline.
1.2. Chot role theo nhom 5 nguoi: Logging+PII, Tracing+Enrichment, SLO+Alerts, LoadTest+Dashboard, Demo+Report.
1.3. Tao bang phan cong dau viec + commit convention de gom bang chung ca nhan.
2. Phase 2 - Pass gate ky thuat (critical path):
2.1. Hoan thanh correlation ID middleware trong [app/middleware.py](app/middleware.py) (clear contextvars, lay/tao x-request-id, bind contextvars, set response headers).
2.2. Hoan thanh log enrichment trong [app/main.py](app/main.py) cho endpoint chat: bind user_id_hash, session_id, feature, model, env; dung ham hash_user_id.
2.3. Bat PII scrub processor trong [app/logging_config.py](app/logging_config.py) de redact truoc khi ghi log.
2.4. Kiem tra lai voi load test + validator; fix toi khi dat >=80 va khong con PII leak.
3. Phase 3 - Tracing khi chua co khoa Langfuse (co the song song voi Phase 4):
3.1. Chot fallback tam thoi: van tiep tuc hoan tat toan bo logging/metrics/alerts khi tracing cloud chua available.
3.2. Chuan bi checklist bien moi truong Langfuse (public key, secret key, host neu can) de bat tracing ngay khi co khoa.
3.3. Khi co khoa: tao it nhat 10-20 request, xac nhan trace list >=10 va chon 1 trace waterfall de phan tich.
4. Phase 4 - Dashboard, SLO, Alerts (parallel):
4.1. Dung metric tu endpoint va script load test de lap dashboard 6 panel theo spec trong [docs/dashboard-spec.md](docs/dashboard-spec.md).
4.2. Can threshold/SLO line theo [config/slo.yaml](config/slo.yaml) va don vi ro rang.
4.3. Hoan thien 3 alert rules + runbook link theo [config/alert_rules.yaml](config/alert_rules.yaml) va [docs/alerts.md](docs/alerts.md).
4.4. Chay incident drills (rag_slow, tool_fail, cost_spike) de thu flow Metrics -> Traces -> Logs.
5. Phase 5 - Evidence va bao cao toi da diem (blocking truoc demo):
5.1. Thu thap day du screenshot bat buoc trong [docs/grading-evidence.md](docs/grading-evidence.md).
5.2. Dien mau [docs/blueprint-template.md](docs/blueprint-template.md): team metadata, score tu validate, trace count, incident RCA, evidence commit/PR tung thanh vien.
5.3. Chuan bi kich ban demo 7-10 phut: middleware flow, logging pipeline, 1 incident RCA.
6. Phase 6 - Bonus (neu con thoi gian):
6.1. Cost optimization truoc/sau (so sanh token/cost trong metrics va trace).
6.2. Tach audit log rieng (neu pipeline cho phep) va ghi bang chung.
6.3. Them custom metric hoac tu dong hoa script nho cho incident/evidence.

**Relevant files**
- [README.md](README.md) - Luong lab va cong viec theo thu tu.
- [day13-rubric-for-instructor.md](day13-rubric-for-instructor.md) - Tieu chi cham 60/40, dieu kien pass.
- [app/middleware.py](app/middleware.py) - Correlation ID propagation, response headers.
- [app/main.py](app/main.py) - Log enrichment cho request context.
- [app/logging_config.py](app/logging_config.py) - Dang ky scrub_event de chong PII leak.
- [app/pii.py](app/pii.py) - Pattern redact va hash_user_id.
- [scripts/load_test.py](scripts/load_test.py) - Tao traffic de sinh log/trace.
- [scripts/validate_logs.py](scripts/validate_logs.py) - Cong diem ky thuat, pass gate >=80.
- [docs/dashboard-spec.md](docs/dashboard-spec.md) - Tieu chuan dashboard 6 panel.
- [docs/alerts.md](docs/alerts.md) - Trigger + runbook.
- [docs/grading-evidence.md](docs/grading-evidence.md) - Checklist screenshot bat buoc.
- [docs/blueprint-template.md](docs/blueprint-template.md) - Mau bao cao nhom + ca nhan.
- [config/slo.yaml](config/slo.yaml) - Nguong muc tieu SLO.
- [config/alert_rules.yaml](config/alert_rules.yaml) - 3 alert rules.

**Verification**
1. Tu dong: chay [tests/test_pii.py](tests/test_pii.py) va [tests/test_metrics.py](tests/test_metrics.py).
2. Tu dong: chay [scripts/load_test.py](scripts/load_test.py) de tao traffic, sau do [scripts/validate_logs.py](scripts/validate_logs.py) dat >=80/100.
3. Thu cong: goi endpoint metrics de xac nhan 6 nhom chi so (latency, traffic, error, cost, tokens, quality).
4. Thu cong: xac nhan log co correlation_id, enrichment fields, va PII da redact.
5. Thu cong: (khi co khoa) xac nhan >=10 traces tren Langfuse + 1 waterfall co giai thich span.
6. Thu cong: verify dashboard du 6 panels, co SLO lines, auto refresh 15-30s.
7. Thu cong: test 3 alert scenarios va lien ket runbook hop le.

**Decisions**
- Muc tieu: toi da diem, khong chi dung o pass gate.
- Cach to chuc: theo nhom, chia role theo rubric de toi uu diem ca nhan + diem nhom.
- Rang buoc hien tai: chua co khoa Langfuse, nen uu tien xong toan bo phan co the hoan thanh offline truoc, trace evidence se bo sung ngay khi co khoa.
- Included scope: TODO bat buoc, dashboard 6 panels, alerts+runbook, incident RCA, evidence pack, script demo.
- Excluded scope tam thoi: tich hop he thong observability ben ngoai phuc tap vuot yeu cau de bai.

**Further Considerations**
1. Quy uoc commit de cham diem ca nhan: Option A commit theo role; Option B commit theo feature ticket. Khuyen nghi Option A de de map vao rubric.
2. Cong cu dashboard: Option A Grafana; Option B Google Sheets/Looker Studio tu export metrics. Khuyen nghi Option A neu nhom da quen.
3. Phan bo thoi gian 1 buoi: Option A 70% implementation + 30% evidence; Option B 60% implementation + 40% evidence. Khuyen nghi Option B cho muc tieu toi da diem.
