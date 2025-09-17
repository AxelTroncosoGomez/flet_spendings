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

# Add both the project root and src directory to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
src_dir = os.path.join(project_root, "src")

# Insert src directory first so imports work for tests
sys.path.insert(0, src_dir)
sys.path.insert(1, project_root)