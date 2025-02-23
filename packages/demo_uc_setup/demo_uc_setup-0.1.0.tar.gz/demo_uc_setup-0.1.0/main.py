"""
Main entrypoint to run the Unity Catalog resource creation using
the Databricks Python SDK and the flexible Pydantic-based config.

Usage:
    python main.py setup     # Run setup
    python main.py teardown  # Run teardown
"""

import sys
from demo_uc_setup.unity_catalog_setup import UnityCatalogSetupTask
from demo_uc_setup.unity_catalog_teardown import UnityCatalogTeardownTask

def print_usage():
    print("Usage: python main.py [setup|teardown]")
    print("  setup    - Run Unity Catalog setup")
    print("  teardown - Run Unity Catalog teardown")

if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in ["setup", "teardown"]:
        print_usage()
        sys.exit(1)

    if sys.argv[1] == "setup":
        UnityCatalogSetupTask.entrypoint()
    else:
        UnityCatalogTeardownTask.entrypoint()

    # Option B) Or instantiate directly:
    # task = UnityCatalogSetupTask()
    # task.run() 