import os
from dotenv import load_dotenv
load_dotenv()

pk = os.getenv("LANGFUSE_PUBLIC_KEY", "")
sk = os.getenv("LANGFUSE_SECRET_KEY", "")
host = os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com")

print(f"PK: {pk[:10]}... (len={len(pk)})")
print(f"SK: {sk[:10]}... (len={len(sk)})")
print(f"Host: {host}")

if not pk or not sk:
    print("❌ Env vars TRỐNG — load_dotenv không tìm thấy .env hoặc key rỗng")
    exit(1)

from langfuse import Langfuse, observe

lf = Langfuse(public_key=pk, secret_key=sk, host=host)

print("→ Auth check:", lf.auth_check())

@observe(name="diagnostic-manual-test")
def ping():
    return {"status": "test trace from diagnostic script"}

ping()
lf.flush()
print("✅ Đã gửi 1 trace tên 'diagnostic-manual-test'. Refresh dashboard sau 10s.")