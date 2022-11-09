"""
File with environment variables that will be used in the API
"""

import os

DB_CONNECTION_URL = os.getenv("DB_TODO_URL")
DB_TEST_URL = os.getenv("TEST_DB_URL")
