import time
from typing import Callable, Optional
from pydantic import BaseModel


class OnRetryParams(BaseModel):
    retry_count: int
    exception: Exception
    delay: float

    class Config:
        arbitrary_types_allowed = True # Allow error to be an Exception

def wrap_with_retry(
    func: Callable,
    *args,
    max_tries: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    on_retry: Optional[Callable[[OnRetryParams], None]] = None,
    should_retry: Callable[[Exception], bool] = lambda _: True,
    **kwargs
):
    """
    A flexible retry function that handles exceptions and retries the function.
    
    Args:
        func: The function to retry
        max_tries: Maximum number of attempts (default: 3)
        delay: Initial delay between retries in seconds (default: 1)
        backoff: Multiplier for delay between retries (default: 2)
        on_retry: Optional callback function to execute between retries
        should_retry: A function that takes an exception and returns True if it should retry
        *args: Positional arguments to pass to the function
        **kwargs: Keyword arguments to pass to the function
    """
    retry_count = 0
    current_delay = delay

    while True:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if not should_retry(e):
                raise e
            
            if retry_count >= max_tries:
                raise e
            
            retry_count += 1
            
            if on_retry:
                params = OnRetryParams(retry_count=retry_count, exception=e, delay=current_delay)
                on_retry(params)
            
            time.sleep(current_delay)
            current_delay *= backoff

    raise Exception("Retry function should never reach here")