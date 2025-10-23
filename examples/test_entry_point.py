#!/usr/bin/env python3
"""Test script to verify the mtg-mcp-server entry point works correctly."""

import subprocess
import sys
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_entry_point():
    """Test that the mtg-mcp-server command works without coroutine warnings."""
    logger.info("Testing mtg-mcp-server entry point...")

    try:
        # Start the server process
        proc = subprocess.Popen(
            ["mtg-mcp-server"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        # Let it run for a few seconds
        time.sleep(3)

        # Terminate the process
        proc.terminate()
        stdout, stderr = proc.communicate(timeout=5)

        # Check for expected output
        if "Starting MTG MCP Server..." in stderr:
            logger.info("✓ Server started successfully")
        else:
            logger.error("✗ Expected startup message not found")
            logger.error(f"STDERR: {stderr}")
            return False

        if "MTG MCP Server initialized successfully" in stderr:
            logger.info("✓ Server initialized successfully")
        else:
            logger.error("✗ Expected initialization message not found")
            logger.error(f"STDERR: {stderr}")
            return False

        # Check for coroutine warnings (should not be present)
        if "RuntimeWarning: coroutine" in stderr:
            logger.error("✗ Coroutine warning still present!")
            logger.error(f"STDERR: {stderr}")
            return False
        else:
            logger.info("✓ No coroutine warnings found")

        # Check for other warnings
        if "RuntimeWarning" in stderr:
            logger.warning(f"Other runtime warnings found: {stderr}")

        logger.info("✓ Entry point test passed!")
        return True

    except subprocess.TimeoutExpired:
        logger.error("✗ Process did not terminate in time")
        proc.kill()
        return False
    except FileNotFoundError:
        logger.error(
            "✗ mtg-mcp-server command not found. Make sure to run 'pip install -e .' first"
        )
        return False
    except Exception as e:
        logger.error(f"✗ Unexpected error: {e}")
        return False


def test_python_module():
    """Test running the server as a Python module."""
    logger.info("Testing Python module execution...")

    try:
        # Start the server process using Python module
        proc = subprocess.Popen(
            [sys.executable, "-m", "mtg_mcp_server.main"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        # Let it run for a few seconds
        time.sleep(3)

        # Terminate the process
        proc.terminate()
        stdout, stderr = proc.communicate(timeout=5)

        # Check for expected output
        if (
            "Starting MTG MCP Server..." in stderr
            and "MTG MCP Server initialized successfully" in stderr
        ):
            logger.info("✓ Python module execution works")
            return True
        else:
            logger.error("✗ Python module execution failed")
            logger.error(f"STDERR: {stderr}")
            return False

    except Exception as e:
        logger.error(f"✗ Python module test failed: {e}")
        return False


def main():
    """Run all entry point tests."""
    logger.info("MTG MCP Server Entry Point Tests")
    logger.info("=" * 40)

    tests_passed = 0
    total_tests = 2

    # Test entry point command
    if test_entry_point():
        tests_passed += 1

    # Test Python module
    if test_python_module():
        tests_passed += 1

    logger.info("=" * 40)
    logger.info(f"Tests passed: {tests_passed}/{total_tests}")

    if tests_passed == total_tests:
        logger.info(
            "✓ All entry point tests passed! The server is ready for MCP client connection."
        )
        return True
    else:
        logger.error("✗ Some tests failed. Check the output above.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
