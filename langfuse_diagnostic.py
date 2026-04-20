import os
from dotenv import load_dotenv
from langfuse import Langfuse

load_dotenv()

public_key = os.getenv('LANGFUSE_PUBLIC_KEY')
secret_key = os.getenv('LANGFUSE_SECRET_KEY')
host = os.getenv('LANGFUSE_BASE_URL') or os.getenv('LANGFUSE_HOST') or "https://cloud.langfuse.com"

print(f"Env vars check:")
print(f"  LANGFUSE_PUBLIC_KEY exists: {bool(public_key)}")
print(f"  LANGFUSE_SECRET_KEY exists: {bool(secret_key)}")
print(f"  LANGFUSE_HOST: {host}")

try:
    print("\nAttempting to initialize Langfuse Client...")
    langfuse = Langfuse(public_key=public_key, secret_key=secret_key, host=host)
    
    print("Checking auth status...")
    langfuse.auth_check()
    print("Auth check successful.")
    
    # Try using trace method based on the dir() which has create_trace_id 
    # but the langfuse 2.x/3.x client should have trace()
    # Let's inspect the object one more time and try a direct generation
    
    print("Calling trace via name directly...")
    try:
        # Some versions use a different approach. Let's try what's in the dir()
        # Events can be created via create_event
        event = langfuse.create_event(name="diagnostic-event")
        print(f"Event created: ID={event.id}")
        
    except Exception as ie:
        print(f"Inner Exception: {ie}")
        
    langfuse.flush()
    print("\nLangfuse events created and flushed successfully.")
except Exception as e:
    print(f"\nError Type: {type(e).__name__}")
    print(f"Error Message: {str(e)}")
