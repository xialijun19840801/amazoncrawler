"""Base crawler class."""

import time
from typing import Optional, Dict, Any
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from loguru import logger

from src.config.settings import settings
from src.utils.rate_limiter import RateLimiter


class BaseCrawler:
    """Base crawler with common functionality."""
    
    def __init__(self):
        """Initialize base crawler with session and rate limiter."""
        self.session = requests.Session()
        self.rate_limiter = RateLimiter(delay=settings.request_delay)
        self._setup_session()
    
    def _setup_session(self) -> None:
        """Configure HTTP session with retry strategy and headers."""
        # Configure retry strategy
        retry_strategy = Retry(
            total=settings.max_retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        # Set default headers
        self.session.headers.update({
            "User-Agent": settings.user_agent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
        })
        
        logger.info("Base crawler session initialized")
    
    def fetch(self, url: str, params: Optional[Dict[str, Any]] = None) -> Optional[requests.Response]:
        """
        Fetch a URL with rate limiting and error handling.
        
        Args:
            url: URL to fetch
            params: Optional query parameters
            
        Returns:
            Response object or None if failed
        """
        self.rate_limiter.wait()
        
        try:
            logger.debug(f"Fetching URL: {url}")
            response = self.session.get(
                url,
                params=params,
                timeout=settings.request_timeout
            )
            response.raise_for_status()
            logger.debug(f"Successfully fetched URL: {url} (Status: {response.status_code})")
            return response
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching {url}: {e}")
            return None
    
    def close(self) -> None:
        """Close the session."""
        self.session.close()
        logger.info("Crawler session closed")

