"""Configuration for the x8 package."""

import os
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:8080')
SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
DEFAULT_TIMEOUT = int(os.getenv('DEFAULT_TIMEOUT', '30'))
DEFAULT_PAGE_SIZE = int(os.getenv('DEFAULT_PAGE_SIZE', '10'))
