import os
import sys
from dotenv import load_dotenv
from pathlib import Path

def pytest_configure():
	# Load .env from the root directory
	env_path = Path(__file__).parent.parent / ".env"
	print(f"env_path: {env_path}")
	if env_path.exists():
		load_dotenv(env_path)

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))