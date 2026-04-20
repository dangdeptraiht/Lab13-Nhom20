from __future__ import annotations
import os
from typing import Any

try:
    from langfuse import Langfuse, get_client, observe
    
    # Khởi tạo tường minh ngay khi import module
    if os.getenv("LANGFUSE_PUBLIC_KEY") and os.getenv("LANGFUSE_SECRET_KEY"):
        _client = Langfuse(
            public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
            secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
            host=os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com"),
        )
        # Verify credentials ngay — sẽ log lỗi nếu sai
        try:
            _client.auth_check()
            print("[tracing] Langfuse auth OK")
        except Exception as e:
            print(f"[tracing] Langfuse auth FAILED: {e}")
except Exception:
    def observe(*args, **kwargs):
        def decorator(func): return func
        return decorator
    def get_client():
        class _Dummy:
            def update_current_trace(self, **kw): pass
            def update_current_span(self, **kw): pass
            def update_current_generation(self, **kw): pass
            def flush(self): pass
        return _Dummy()

def tracing_enabled() -> bool:
    return bool(os.getenv("LANGFUSE_PUBLIC_KEY") and os.getenv("LANGFUSE_SECRET_KEY"))