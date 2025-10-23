#!/usr/bin/env python3
"""Test script to verify MCP server connection approaches."""

import subprocess
import sys
import time
import os


def test_python_module():
    """Test running as Python module."""
    print("Testing: python -m mtg_mcp_server.main")
    try:
        proc = subprocess.Popen(
            [sys.executable, "-m", "mtg_mcp_server.main"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=os.getcwd(),
        )
        time.sleep(2)
        proc.terminate()
        stdout, stderr = proc.communicate(timeout=3)

        if "Starting MTG MCP Server" in stderr and "coroutine" not in stderr:
            print("✓ Python module approach works!")
            return True
        else:
            print("✗ Python module approach failed")
            print(f"STDERR: {stderr}")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_with_pythonpath():
    """Test with explicit PYTHONPATH."""
    print("Testing: python -m mtg_mcp_server.main with PYTHONPATH")
    try:
        env = os.environ.copy()
        env["PYTHONPATH"] = os.getcwd()

        proc = subprocess.Popen(
            [sys.executable, "-m", "mtg_mcp_server.main"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=env,
        )
        time.sleep(2)
        proc.terminate()
        stdout, stderr = proc.communicate(timeout=3)

        if "Starting MTG MCP Server" in stderr and "coroutine" not in stderr:
            print("✓ PYTHONPATH approach works!")
            return True
        else:
            print("✗ PYTHONPATH approach failed")
            print(f"STDERR: {stderr}")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def main():
    print("MTG MCP Server Connection Test")
    print("=" * 40)
    print(f"Current directory: {os.getcwd()}")
    print(f"Python executable: {sys.executable}")
    print()

    # Test approaches
    approaches = [
        ("Python Module", test_python_module),
        ("With PYTHONPATH", test_with_pythonpath),
    ]

    working_approaches = []

    for name, test_func in approaches:
        print(f"--- {name} ---")
        if test_func():
            working_approaches.append(name)
        print()

    print("=" * 40)
    if working_approaches:
        print("✓ Working approaches:")
        for approach in working_approaches:
            print(f"  - {approach}")
        print("\nRecommended MCP configuration:")
        print(
            """
{
  "mcpServers": {
    "mtg-mcp-server": {
      "command": "python",
      "args": ["-m", "mtg_mcp_server.main"],
      "cwd": "%s",
      "env": {
        "PYTHONPATH": "%s"
      },
      "disabled": false,
      "autoApprove": ["search_cards"]
    }
  }
}
        """
            % (os.getcwd().replace("\\", "/"), os.getcwd().replace("\\", "/"))
        )
    else:
        print("✗ No working approaches found. Check installation.")


if __name__ == "__main__":
    main()
