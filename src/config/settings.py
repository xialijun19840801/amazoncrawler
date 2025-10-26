"""Application settings and configuration."""

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Rate limiting
    request_delay: float = Field(default=2.0, description="Delay between requests in seconds")
    
    # User agent
    user_agent: str = Field(
        default="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        description="User agent string"
    )
    
    # Timeout settings
    request_timeout: int = Field(default=30, description="Request timeout in seconds")
    max_retries: int = Field(default=3, description="Maximum retry attempts")
    
    # Output settings
    output_dir: str = Field(default="output", description="Directory for output files")
    
    class Config:
        """Pydantic config."""
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
settings = Settings()
