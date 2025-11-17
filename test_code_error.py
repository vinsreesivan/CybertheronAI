#!/usr/bin/env python3
"""
Test file for auto-debugging feature
This code has a deliberate error that the LLMs should fix
"""

print("Starting calculation...")

# This will cause a ZeroDivisionError
x = 10
y = 0
result = x / y

print(f"The result is: {result}")
print("Calculation complete!")
