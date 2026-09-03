import os
from dotenv import load_dotenv

# Loads local values from .env if that file exists.
load_dotenv()


def get_secret(name: str, default: str | None = None) -> str | None:
    """
    Returns an environment variable or the supplied default value.
    Returns None when the variable is not configured.
    """
    return os.getenv(name, default)