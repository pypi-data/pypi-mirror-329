"""
Script to see the big picture of failing modules.
For debugging the specific error of each module use: 
> python -c "import royalflush.agent"
"""

import importlib

# List of modules to test for circular imports
modules_to_test = [
    "royalflush.agent",
    "royalflush.agent.premiofl",
    "royalflush.agent.base",
    "royalflush.behaviour",
    "royalflush.commands",
    "royalflush.dataset",
    "royalflush.log",
    "royalflush.nn",
    "royalflush.similarity",
    "royalflush.utils",
]

print("Starting import tests...\n")

# Test importing each module individually
for module in modules_to_test:
    print(f"Importing {module}...")
    try:
        importlib.import_module(module)
        print(f"Successfully imported {module}\n")
    except Exception as e:
        print(f"Failed to import {module}: {e}\n")
