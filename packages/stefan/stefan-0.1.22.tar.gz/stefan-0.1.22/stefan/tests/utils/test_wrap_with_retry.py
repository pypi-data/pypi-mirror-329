import pytest
from unittest.mock import Mock, patch
import time
from stefan.utils.wrap_with_retry import wrap_with_retry

@pytest.fixture
def mock_sleep():
    with patch('time.sleep', return_value=None) as mock_sleep:
        yield mock_sleep

def test_successful_execution_no_retry(mock_sleep):
    # Test that function executes successfully without needing retries
    mock_fn = Mock(return_value="success")
    result = wrap_with_retry(mock_fn, max_tries=3)
    
    assert result == "success"
    assert mock_fn.call_count == 1

def test_retry_until_success(mock_sleep):
    # Test that function retries on failure and eventually succeeds
    mock_fn = Mock(side_effect=[ValueError, ValueError, "success"])
    result = wrap_with_retry(mock_fn, max_tries=3)
    
    assert result == "success"
    assert mock_fn.call_count == 3

def test_max_retries_exceeded(mock_sleep):
    # Test that function raises exception after max retries
    mock_fn = Mock(side_effect=ValueError("Test error"))
    
    with pytest.raises(ValueError, match="Test error"):
        wrap_with_retry(mock_fn, max_tries=2)
    
    assert mock_fn.call_count == 3  # Initial try + 2 retries

def test_retry_specific_exceptions(mock_sleep):
    # Test that only specified exceptions trigger retry
    mock_fn = Mock(side_effect=[ValueError, TypeError, "success"])
    
    with pytest.raises(TypeError):
        wrap_with_retry(mock_fn, max_tries=2, should_retry=lambda e: isinstance(e, ValueError))
    
    assert mock_fn.call_count == 2  # Stops at TypeError

def test_with_args_and_kwargs(mock_sleep):
    # Test that arguments are properly passed through
    mock_fn = Mock(return_value="success")
    args = (1, 2)  # Example positional arguments
    kwargs = {'key': 'value'}  # Example keyword arguments
    result = wrap_with_retry(mock_fn, *args, max_tries=3, **kwargs)
    
    mock_fn.assert_called_once_with(*args, **kwargs)
    assert result == "success"

def test_zero_retries(mock_sleep):
    # Test behavior when max_retries is 0
    mock_fn = Mock(side_effect=ValueError("Test error"))
    with pytest.raises(ValueError, match="Test error"):
        wrap_with_retry(mock_fn, max_tries=0)
    
    assert mock_fn.call_count == 1

def test_custom_retry_delay(mock_sleep):
    # Test that retry delay is respected
    mock_fn = Mock(side_effect=[ValueError, "success"])
    
    result = wrap_with_retry(mock_fn, max_tries=1, delay=0.1)
    
    # Ensure time.sleep was called with the correct delay
    mock_sleep.assert_called_once_with(0.1)
    assert result == "success"
    assert mock_fn.call_count == 2