"""
Module for running live tests with pytest.

This script sets up the environment to run live tests by setting the necessary
environment variables and invoking pytest with appropriate arguments.
"""

import os
import subprocess
import sys


def run_live_tests(test_name=None):
    """
    Run live tests with pytest, setting the RUN_LIVE_TESTS environment variable.
    If test_name is provided, only the specified test will be run.
    Otherwise, all live test files (with '_live' in the name) will be run.

    Args:
        test_name (str, optional): Specific test name to run. Defaults to None.

    Returns:
        int: Return code from the pytest execution.
    """
    # Set the environment variable to enable live tests
    os.environ["RUN_LIVE_TESTS"] = "true"

    # Construct the pytest command
    pytest_args = ["pytest", "-v"]
    if test_name:
        pytest_args.extend(["-k", test_name])
    else:
        # Find all live test files in the tests directory
        test_files = [
            f for f in os.listdir("tests/") if "_live" in f and f.endswith(".py")
        ]
        if test_files:
            pytest_args.extend(["tests/" + f for f in test_files])
        else:
            pytest_args.append("tests/")

    print(f"Running live tests with command: {' '.join(pytest_args)}")
    try:
        result = subprocess.run(pytest_args, check=True, text=True, capture_output=True)
        print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        return result.returncode
    except subprocess.CalledProcessError as e:
        print(e.output, file=sys.stderr)
        return e.returncode
    except Exception as e:
        print(f"Error running live tests: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    TEST_NAME = None
    if len(sys.argv) > 1:
        TEST_NAME = sys.argv[1]
        print(f"Running specific live test: {TEST_NAME}")
    else:
        print(
            "Running all live tests. To run a specific test, provide the test name as an argument."
        )

    exit(run_live_tests(TEST_NAME))
