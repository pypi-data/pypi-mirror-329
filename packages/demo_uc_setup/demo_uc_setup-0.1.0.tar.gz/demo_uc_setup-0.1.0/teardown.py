"""
Script to run the Unity Catalog teardown process.
"""
from demo_uc_setup.unity_catalog_teardown import UnityCatalogTeardownTask

if __name__ == "__main__":
    UnityCatalogTeardownTask.entrypoint() 