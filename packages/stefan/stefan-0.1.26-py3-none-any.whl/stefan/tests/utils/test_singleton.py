import pytest
from stefan.utils.singleton import singleton

def test_singleton_creates_single_instance():
    """Test that singleton decorator creates only one instance of a class."""
    
    @singleton
    class TestClass:
        def __init__(self):
            self.value = 0
    
    # Create two instances
    instance1 = TestClass()
    instance2 = TestClass()
    
    # Verify they are the same object
    assert instance1 is instance2
    
def test_singleton_maintains_state():
    """Test that singleton maintains state between instances."""
    
    @singleton
    class TestClass:
        def __init__(self):
            self.value = 0
            
        def increment(self):
            self.value += 1
    
    # Create first instance and modify state
    instance1 = TestClass()
    instance1.increment()
    
    # Create second instance and verify state is maintained
    instance2 = TestClass()
    assert instance2.value == 1
    
def test_singleton_with_arguments():
    """Test that singleton works with class initialization arguments."""
    
    @singleton
    class TestClass:
        def __init__(self, initial_value):
            self.value = initial_value
    
    # Create instance with argument
    instance1 = TestClass(5)
    assert instance1.value == 5
    
    # Verify second instance maintains first instance's state
    instance2 = TestClass(10)  # This argument should be ignored
    assert instance2.value == 5
    assert instance1 is instance2

def test_different_singleton_classes():
    """Test that different singleton classes maintain separate instances."""
    
    @singleton
    class TestClass1:
        pass
        
    @singleton
    class TestClass2:
        pass
    
    instance1 = TestClass1()
    instance2 = TestClass2()
    
    assert instance1 is not instance2
