from typing import Type
from databricks.sdk.service import catalog
from demo_uc_setup.common import Task, T
from demo_uc_setup.config import Config

class UnityCatalogSetupTask(Task[Config]):
    """
    A task to ensure catalogs, schemas, and volumes exist
    in the Databricks workspace. Uses typed config for
    resource names, credentials, etc.
    """

    def __init__(self, config_class: Type[T] = Config):
        super().__init__(config_class)

    def run(self):
        self.logger.info("Starting Unity Catalog setup...")

        # 1) Ensure the catalog exists
        catalog_name = self.config.demo_catalog_name
        self.logger.info(f"Ensuring catalog '{catalog_name}'")
        try:
            self.workspace_client.catalogs.get(name=catalog_name)
            self.logger.info(f"Catalog '{catalog_name}' already exists.")
        except Exception:
            self.logger.info(f"Catalog '{catalog_name}' not found; creating it.")
            self.workspace_client.catalogs.create(
                name=catalog_name,
                comment="Demo Catalog for Databricks demos"
            )

        # 2) Ensure all schemas exist and create volumes within each schema
        for schema_name in self.config.demo_schemas:
            # Create schema
            self.logger.info(f"Ensuring schema '{catalog_name}.{schema_name}'")
            try:
                self.workspace_client.schemas.get(
                    name=schema_name,
                    catalog_name=catalog_name
                )
                self.logger.info(f"Schema '{catalog_name}.{schema_name}' already exists.")
            except Exception:
                try:
                    self.logger.info(f"Schema '{catalog_name}.{schema_name}' not found; creating it.")
                    self.workspace_client.schemas.create(
                        name=schema_name,
                        catalog_name=catalog_name,
                        comment=f"Demo Schema {schema_name} for Databricks demos"
                    )
                except Exception as e:
                    if "already exists" in str(e):
                        self.logger.info(f"Schema '{catalog_name}.{schema_name}' already exists (caught during creation).")
                    else:
                        raise e

            # Create volume within this schema
            volume_name = self.config.demo_volume_name
            self.logger.info(f"Ensuring volume '{catalog_name}.{schema_name}.{volume_name}'")
            try:
                self.workspace_client.volumes.get(
                    name=volume_name,
                    catalog_name=catalog_name,
                    schema_name=schema_name
                )
                self.logger.info(f"Volume '{catalog_name}.{schema_name}.{volume_name}' already exists.")
            except Exception:
                try:
                    self.logger.info(f"Volume '{catalog_name}.{schema_name}.{volume_name}' not found; creating it.")
                    self.workspace_client.volumes.create(
                        name=volume_name,
                        catalog_name=catalog_name,
                        schema_name=schema_name,
                        volume_type=catalog.VolumeType.MANAGED,
                        comment=f"Demo Volume for schema {schema_name}"
                    )
                except Exception as e:
                    if "already exists" in str(e):
                        self.logger.info(f"Volume '{catalog_name}.{schema_name}.{volume_name}' already exists (caught during creation).")
                    else:
                        raise e

        self.logger.info("Unity Catalog setup complete!") 