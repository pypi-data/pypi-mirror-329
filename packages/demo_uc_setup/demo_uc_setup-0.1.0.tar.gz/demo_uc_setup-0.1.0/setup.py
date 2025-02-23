"""
Script to run the Unity Catalog setup process.
"""
from demo_uc_setup.unity_catalog_setup import UnityCatalogSetupTask

if __name__ == "__main__":
    UnityCatalogSetupTask.entrypoint() 