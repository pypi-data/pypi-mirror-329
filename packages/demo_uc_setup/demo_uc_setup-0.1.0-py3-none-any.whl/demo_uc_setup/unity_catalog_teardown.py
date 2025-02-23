from typing import Type
from databricks.sdk import WorkspaceClient
from demo_uc_setup.common import Task, T
from demo_uc_setup.config import Config

class UnityCatalogTeardownTask(Task[Config]):
    """
    A task to delete (teardown) the Unity Catalog resources in
    the configured Databricks workspace. Uses typed config for
    resource names, credentials, etc.
    """

    def __init__(self, config_class: Type[T] = Config):
        super().__init__(config_class)

    def run(self):
        self.logger.info("Starting teardown of Unity Catalog resources...")

        catalog_name = self.config.demo_catalog_name
        self.logger.info(f"Deleting catalog '{catalog_name}' and its dependencies (force=True).")

        try:
            self.workspace_client.catalogs.delete(name=catalog_name, force=True)
            self.logger.info(f"Catalog '{catalog_name}' (and its contents) successfully deleted.")
        except Exception as e:
            self.logger.error(f"Failed to delete catalog '{catalog_name}'. Reason: {e}")

        self.logger.info("Unity Catalog teardown complete!") 