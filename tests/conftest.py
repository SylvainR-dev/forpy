"""
Shared pytest configuration and fixtures.

All tests must be run from the project root:
    python -m pytest
"""
import os
import sys

# Ensure the project root is always on sys.path so imports work.
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
