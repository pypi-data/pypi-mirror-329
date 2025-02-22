import pytest
from stefan.utils.command_executor import CommandExecutor

class TestCommandExecutor:
    def test_successful_command(self):
        # Test a simple echo command
        success, output = CommandExecutor.execute("echo Hello World")
        assert success is True
        assert "Hello World" in output

    def test_failed_command(self):
        # Test a non-existent command
        success, output = CommandExecutor.execute("nonexistentcommand")
        assert success is False
        # Check for the actual shell error message
        assert "command not found" in output
        assert "nonexistentcommand" in output

    def test_command_with_arguments(self):
        # Test command with multiple arguments
        success, output = CommandExecutor.execute("python --version")
        assert success is True
        assert "Python" in output

    def test_command_with_spaces(self):
        # Test command with multiple spaces
        success, output = CommandExecutor.execute("echo   \"Hello   World\"")
        assert success is True
        assert "Hello   World" in output

    def test_command_with_simultaneous_stdout_stderr(self):
        """
        Test that both stdout and stderr are captured when they occur simultaneously.
        Uses a Python command that prints to both stdout and stderr.
        """
        python_cmd = 'python -c "import sys; print(\'stdout message\'); print(\'stderr message\', file=sys.stderr)"'
        success, output = CommandExecutor.execute(python_cmd)
        
        assert success is True  # The command should succeed
        assert "stdout message" in output, "stdout should be in the output"
        assert "stderr message" in output, "stderr should be in the output"
