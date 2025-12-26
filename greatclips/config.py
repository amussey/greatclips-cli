"""Configuration management for Great Clips CLI."""

import os
from dataclasses import dataclass, field

from dotenv import load_dotenv


@dataclass
class Config:
    """Configuration for Great Clips API client.

    Loads configuration from environment variables or .env file.

    Environment Variables:
        # Embedded Authentication (stylewaretouch.net)
        SECRET_KEY_CSV: Secret key as CSV string for HMAC authentication
        ENCRYPTION_KEY: Encryption key for token generation

        # Optional Configuration
        DEBUG: Enable debug mode (default: False)
        TIMEOUT: Request timeout in seconds (default: 30)
    """

    # Embedded Authentication Configuration
    secret_key_csv: str
    encryption_key: str

    # Optional Configuration
    debug: bool = field(default=False)
    timeout: int = field(default=30)

    @classmethod
    def from_env(cls, env_file: str | None = None) -> "Config":
        """Load configuration from environment variables and optional .env file.

        Args:
            env_file: Path to .env file. If None, looks for .env in current directory.

        Returns:
            Config instance with loaded values
        """
        # Load .env file using python-dotenv
        # If env_file is None, load_dotenv will search for .env automatically
        load_dotenv(dotenv_path=env_file)

        # Load values from environment
        secret_key = os.getenv("SECRET_KEY_CSV")
        encryption_key = os.getenv("ENCRYPTION_KEY")

        if not secret_key:
            raise ValueError("SECRET_KEY_CSV environment variable is required")
        if not encryption_key:
            raise ValueError("ENCRYPTION_KEY environment variable is required")

        return cls(
            secret_key_csv=secret_key,
            encryption_key=encryption_key,
            debug=os.getenv("DEBUG", "").lower() in ("true", "1", "yes"),
            timeout=int(os.getenv("TIMEOUT", "30")),
        )


def get_config(env_file: str | None = None) -> Config:
    """Get the global configuration instance.

    Args:
        env_file: Path to .env file (only used on first load or reload)

    Returns:
        Config instance
    """
    return Config.from_env(env_file)
