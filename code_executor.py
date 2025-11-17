"""
Code Execution Engine with Error Capture
Safely executes Python code and captures output/errors for LLM analysis
"""

import sys
import io
import traceback
import contextlib
from typing import Dict, Any, Optional
import subprocess
import tempfile
import os


class CodeExecutionResult:
    """Container for code execution results"""

    def __init__(
        self,
        success: bool,
        output: str = "",
        error: str = "",
        error_type: str = "",
        code: str = ""
    ):
        self.success = success
        self.output = output
        self.error = error
        self.error_type = error_type
        self.code = code

    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "output": self.output,
            "error": self.error,
            "error_type": self.error_type,
            "code": self.code
        }

    def get_error_prompt(self) -> str:
        """Generate a prompt for LLM to fix the error"""
        if self.success:
            return ""

        return f"""The following Python code has an error:

```python
{self.code}
```

Error Type: {self.error_type}
Error Message:
{self.error}

Please analyze the error and provide a corrected version of the code that fixes the issue.
Only return the corrected Python code without any explanation."""


class CodeExecutor:
    """Executes Python code safely and captures results"""

    def __init__(self, timeout: int = 30):
        self.timeout = timeout

    def execute_inline(self, code: str) -> CodeExecutionResult:
        """
        Execute code inline (in same process)
        Safer for simple code but shares the same interpreter
        """
        # Capture stdout and stderr
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()

        try:
            with contextlib.redirect_stdout(stdout_capture), \
                 contextlib.redirect_stderr(stderr_capture):
                # Execute the code
                exec(code, {})

            output = stdout_capture.getvalue()
            return CodeExecutionResult(
                success=True,
                output=output,
                code=code
            )

        except Exception as e:
            error_msg = stderr_capture.getvalue()
            if not error_msg:
                error_msg = traceback.format_exc()

            return CodeExecutionResult(
                success=False,
                output=stdout_capture.getvalue(),
                error=error_msg,
                error_type=type(e).__name__,
                code=code
            )

    def execute_subprocess(self, code: str) -> CodeExecutionResult:
        """
        Execute code in a subprocess (isolated)
        Safer for untrusted code
        """
        # Create temporary file with the code
        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.py',
            delete=False
        ) as tmp_file:
            tmp_file.write(code)
            tmp_file_path = tmp_file.name

        try:
            # Run the code in subprocess
            result = subprocess.run(
                [sys.executable, tmp_file_path],
                capture_output=True,
                text=True,
                timeout=self.timeout
            )

            if result.returncode == 0:
                return CodeExecutionResult(
                    success=True,
                    output=result.stdout,
                    code=code
                )
            else:
                # Extract error type from stderr
                error_lines = result.stderr.strip().split('\n')
                error_type = "Unknown"

                for line in error_lines:
                    if "Error:" in line or "Exception:" in line:
                        error_type = line.split(':')[0].strip().split()[-1]
                        break

                return CodeExecutionResult(
                    success=False,
                    output=result.stdout,
                    error=result.stderr,
                    error_type=error_type,
                    code=code
                )

        except subprocess.TimeoutExpired:
            return CodeExecutionResult(
                success=False,
                error=f"Code execution timed out after {self.timeout} seconds",
                error_type="TimeoutError",
                code=code
            )

        except Exception as e:
            return CodeExecutionResult(
                success=False,
                error=str(e),
                error_type=type(e).__name__,
                code=code
            )

        finally:
            # Clean up temporary file
            try:
                os.unlink(tmp_file_path)
            except:
                pass

    def execute(
        self,
        code: str,
        use_subprocess: bool = True
    ) -> CodeExecutionResult:
        """
        Execute code with chosen method

        Args:
            code: Python code to execute
            use_subprocess: If True, run in subprocess (safer), else inline

        Returns:
            CodeExecutionResult object
        """
        if use_subprocess:
            return self.execute_subprocess(code)
        else:
            return self.execute_inline(code)


def test_executor():
    """Test the code executor"""
    executor = CodeExecutor()

    # Test 1: Successful code
    print("Test 1: Successful code")
    result = executor.execute("""
print("Hello, World!")
x = 5 + 3
print(f"Result: {x}")
""")
    print(f"Success: {result.success}")
    print(f"Output: {result.output}")
    print()

    # Test 2: Code with error
    print("Test 2: Code with error")
    result = executor.execute("""
print("Starting...")
x = 10 / 0  # Division by zero
print("This won't print")
""")
    print(f"Success: {result.success}")
    print(f"Error Type: {result.error_type}")
    print(f"Error: {result.error[:100]}...")
    print()

    # Test 3: Syntax error
    print("Test 3: Syntax error")
    result = executor.execute("""
print("Hello"
# Missing closing parenthesis
""")
    print(f"Success: {result.success}")
    print(f"Error Type: {result.error_type}")
    print()


if __name__ == "__main__":
    test_executor()
