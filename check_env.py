import os
from dotenv import load_dotenv

load_dotenv()
host = os.getenv('LANGFUSE_HOST')
print(f"Original Host: {host}")
