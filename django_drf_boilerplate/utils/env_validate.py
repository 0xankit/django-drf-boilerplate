'''
Validate environment variables
'''
import os


def validate_env(env_vars: list):
    """
    Validates that all required environment variables are set and not empty.

    @param env_vars: list of environment variables to validate
    
    @raises ValueError: if any of the required environment variables are missing
    """
    missing_vars = [var for var in env_vars if not os.getenv(var)]
    if missing_vars:
        raise ValueError(
            f"Missing required environment variables: {', '.join(missing_vars)}")
