#!/usr/bin/env python3
"""
Auto-Debugging Terminal - Interactive Code Execution with LLM Error Fixing

This tool allows you to run Python code, and if there's an error,
multiple LLMs will automatically analyze and fix it.
"""

import asyncio
import sys
import os
from pathlib import Path
from typing import Optional
import re

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from code_executor import CodeExecutor, CodeExecutionResult
from llm_fusion import LLMFusionEngine
import yaml


class Colors:
    """Terminal colors"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class AutoDebugger:
    """Auto-debugging system with LLM integration"""

    def __init__(self, config_path: str = "config.yaml"):
        # Load configuration
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        # Initialize components
        self.executor = CodeExecutor(timeout=30)
        self.fusion_engine = LLMFusionEngine(self.config)

        self.max_iterations = 5  # Maximum auto-fix attempts
        self.iteration = 0

    def print_header(self):
        """Print application header"""
        print(f"\n{Colors.BOLD}{Colors.OKCYAN}{'='*70}")
        print("🤖 Auto-Debugging Terminal with Multi-LLM Fusion")
        print(f"{'='*70}{Colors.ENDC}\n")
        print(f"{Colors.OKBLUE}Models active: {', '.join([m['name'] for m in self.config['models'] if m.get('enabled')])}{Colors.ENDC}")
        print(f"{Colors.OKBLUE}Refiner model: {self.config.get('refiner_model')}{Colors.ENDC}\n")

    def print_section(self, title: str, color: str = Colors.OKCYAN):
        """Print a section header"""
        print(f"\n{color}{Colors.BOLD}{'─'*70}")
        print(f"  {title}")
        print(f"{'─'*70}{Colors.ENDC}\n")

    def extract_code_from_response(self, response: str) -> str:
        """Extract Python code from LLM response"""
        # Try to find code blocks
        code_block_pattern = r'```python\s*(.*?)\s*```'
        matches = re.findall(code_block_pattern, response, re.DOTALL)

        if matches:
            return matches[0].strip()

        # Try generic code blocks
        code_block_pattern = r'```\s*(.*?)\s*```'
        matches = re.findall(code_block_pattern, response, re.DOTALL)

        if matches:
            return matches[0].strip()

        # If no code blocks, return the whole response stripped
        return response.strip()

    async def fix_code_with_llm(self, result: CodeExecutionResult) -> Optional[str]:
        """Use LLM fusion to fix the code"""
        self.print_section("🤖 Analyzing Error with Multi-LLM Fusion", Colors.WARNING)

        prompt = result.get_error_prompt()
        print(f"{Colors.WARNING}Sending error to LLMs for analysis...{Colors.ENDC}\n")

        # Get fusion response
        fusion_result = await self.fusion_engine.fuse_responses(prompt)

        fused_response = fusion_result['fused_response']

        # Extract code from response
        fixed_code = self.extract_code_from_response(fused_response)

        return fixed_code

    async def run_code_with_auto_fix(self, initial_code: str, auto_mode: bool = False):
        """
        Run code and automatically fix errors

        Args:
            initial_code: The initial Python code to execute
            auto_mode: If True, auto-fix without asking user
        """
        self.iteration = 0
        current_code = initial_code

        while self.iteration < self.max_iterations:
            self.iteration += 1

            # Print iteration info
            if self.iteration > 1:
                self.print_section(
                    f"🔄 Iteration {self.iteration}/{self.max_iterations}",
                    Colors.OKCYAN
                )

            # Display current code
            print(f"{Colors.BOLD}Current Code:{Colors.ENDC}")
            print(f"{Colors.OKBLUE}{'─'*70}")
            print(current_code)
            print(f"{'─'*70}{Colors.ENDC}\n")

            # Execute code
            print(f"{Colors.BOLD}▶️  Executing code...{Colors.ENDC}\n")
            result = self.executor.execute(current_code, use_subprocess=True)

            if result.success:
                # Code executed successfully
                self.print_section("✅ Execution Successful!", Colors.OKGREEN)

                if result.output:
                    print(f"{Colors.OKGREEN}Output:{Colors.ENDC}")
                    print(result.output)
                else:
                    print(f"{Colors.OKGREEN}Code executed successfully with no output.{Colors.ENDC}")

                print()
                break

            else:
                # Code failed
                self.print_section("❌ Execution Failed", Colors.FAIL)
                print(f"{Colors.FAIL}Error Type: {result.error_type}{Colors.ENDC}")
                print(f"\n{Colors.FAIL}Error Message:{Colors.ENDC}")
                print(result.error)
                print()

                # Check if we've hit max iterations
                if self.iteration >= self.max_iterations:
                    print(f"{Colors.WARNING}Maximum iterations ({self.max_iterations}) reached.{Colors.ENDC}")
                    print(f"{Colors.WARNING}Unable to fix the code automatically.{Colors.ENDC}\n")
                    break

                # Ask user if they want to fix
                if not auto_mode:
                    print(f"{Colors.BOLD}Do you want the LLMs to fix this error? (yes/no): {Colors.ENDC}", end='')
                    user_input = input().strip().lower()

                    if user_input not in ['yes', 'y']:
                        print(f"{Colors.WARNING}Auto-fix cancelled by user.{Colors.ENDC}\n")
                        break

                # Try to fix with LLM
                fixed_code = await self.fix_code_with_llm(result)

                if not fixed_code:
                    print(f"{Colors.FAIL}LLMs could not generate a fix.{Colors.ENDC}\n")
                    break

                # Show proposed fix
                self.print_section("🔧 Proposed Fix from LLMs", Colors.OKCYAN)
                print(f"{Colors.OKBLUE}{'─'*70}")
                print(fixed_code)
                print(f"{'─'*70}{Colors.ENDC}\n")

                # Update current code for next iteration
                current_code = fixed_code

        # Final summary
        self.print_section("📊 Summary", Colors.BOLD)
        print(f"Total iterations: {self.iteration}")
        print(f"Final status: {'✅ Success' if result.success else '❌ Failed'}")
        print()

    def interactive_mode(self):
        """Interactive terminal mode"""
        self.print_header()

        print(f"{Colors.BOLD}Interactive Mode{Colors.ENDC}")
        print("Enter your Python code (type 'END' on a new line when done)")
        print("Commands: 'exit' to quit, 'help' for help\n")

        while True:
            print(f"{Colors.OKCYAN}>>> Enter code (END to finish):{Colors.ENDC}")

            lines = []
            while True:
                try:
                    line = input()
                    if line.strip() == 'END':
                        break
                    if line.strip() == 'exit':
                        print(f"{Colors.OKGREEN}Goodbye!{Colors.ENDC}")
                        return
                    if line.strip() == 'help':
                        self.print_help()
                        lines = []
                        break
                    lines.append(line)
                except EOFError:
                    print(f"\n{Colors.OKGREEN}Goodbye!{Colors.ENDC}")
                    return
                except KeyboardInterrupt:
                    print(f"\n{Colors.WARNING}Cancelled.{Colors.ENDC}")
                    lines = []
                    break

            if not lines:
                continue

            code = '\n'.join(lines)

            # Run with auto-fix
            asyncio.run(self.run_code_with_auto_fix(code, auto_mode=False))

            print(f"\n{Colors.OKCYAN}{'='*70}{Colors.ENDC}\n")

    def print_help(self):
        """Print help message"""
        print(f"\n{Colors.BOLD}Help:{Colors.ENDC}")
        print("  - Write your Python code line by line")
        print("  - Type 'END' on a new line to execute")
        print("  - Type 'exit' to quit")
        print("  - If code has errors, LLMs will analyze and propose fixes")
        print("  - You'll be asked to confirm before applying fixes")
        print()


async def main():
    """Main entry point"""
    debugger = AutoDebugger()

    # Check if code is provided via argument
    if len(sys.argv) > 1:
        # File mode
        file_path = sys.argv[1]

        if not os.path.exists(file_path):
            print(f"{Colors.FAIL}Error: File not found: {file_path}{Colors.ENDC}")
            return

        with open(file_path, 'r') as f:
            code = f.read()

        debugger.print_header()
        print(f"{Colors.BOLD}Running code from: {file_path}{Colors.ENDC}\n")

        # Check for --auto flag
        auto_mode = '--auto' in sys.argv

        await debugger.run_code_with_auto_fix(code, auto_mode=auto_mode)

    else:
        # Interactive mode
        debugger.interactive_mode()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n{Colors.OKGREEN}Goodbye!{Colors.ENDC}")
    except Exception as e:
        print(f"{Colors.FAIL}Fatal error: {e}{Colors.ENDC}")
        import traceback
        traceback.print_exc()
