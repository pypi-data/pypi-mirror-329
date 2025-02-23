from pydantic_settings import BaseSettings
from typing import Optional

class Config(BaseSettings):
    """
    Configuration class using Pydantic BaseSettings.
    By default, each field can be overridden by environment
    variables matching the field name (in uppercase).
    For example, DATABRICKS_HOST, DATABRICKS_TOKEN, etc.
    """

    # Databricks connection settings - optional for notebook execution
    databricks_host: Optional[str] = None
    databricks_token: Optional[str] = None

    # Default names for Unity Catalog demo objects
    demo_catalog_name: str = "demo_catalog"
    demo_schemas: list[str] = ["demo_schema_1", "demo_schema_2"]  # List of schemas
    demo_volume_name: str = "demo_volume"  # This could also be a list if needed

    class Config:
        env_file = ".env"  # or any custom file, if desired
        env_file_encoding = "utf-8" 