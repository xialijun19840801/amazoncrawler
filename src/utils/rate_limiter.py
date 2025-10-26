"""Rate limiting utility."""

import time
from typing import Callable, Any
from functools import wraps
from loguru import logger


class RateLimiter:
    """Rate limiter for controlling request frequency."""
    
    def __init__(self, delay: float = 2.0):
        """
        Initialize rate limiter.
        
        Args:
            delay: Time to wait between requests in seconds
        """
        self.delay = delay
        self.last_request_time = 0.0
    
    def wait(self) -> None:
        """Wait for the specified delay since the last request."""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.delay:
            wait_time = self.delay - time_since_last
            logger.debug(f"Rate limiting: waiting {wait_time:.2f} seconds")
            time.sleep(wait_time)
        
        self.last_request_time = time.time()
    
    def __call__(self, func: Callable) -> Callable:
        """Decorator to rate limit a function."""
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            self.wait()
            return func(*args, **kwargs)
        return wrapper

