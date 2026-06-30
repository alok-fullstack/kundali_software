"""
Run the FastAPI backend server.

Usage:
    python run.py

Or:
    python -m uvicorn main:app --reload --port 8000
"""

import sys
from pathlib import Path

# Ensure parent directory is in path for src imports
parent_dir = Path(__file__).resolve().parent.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

# Also add backend directory itself
backend_dir = Path(__file__).resolve().parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))


def main():
    import uvicorn

    print("\n" + "=" * 60)
    print("   KUNDALI SOFTWARE - FastAPI Backend")
    print("=" * 60)
    print("   Server URL:  http://localhost:8000")
    print("   API Docs:    http://localhost:8000/docs")
    print("   ReDoc:       http://localhost:8000/redoc")
    print("=" * 60)
    print("\n   Press Ctrl+C to stop the server\n")

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )


if __name__ == "__main__":
    main()
