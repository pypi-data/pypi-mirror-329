import logging
from typing import TypeVar, Generic
from databricks.sdk import WorkspaceClient

from demo_uc_setup.config import Config

# Example of a type variable bound to our Config class
T = TypeVar("T", bound=Config)

class Task(Generic[T]):
    """
    A reusable Task base class that works both locally and in Databricks notebooks.
    When running locally, requires databricks_host and databricks_token.
    When running in a notebook, these parameters are optional.
    """

    def __init__(self, config_class: type[T]):
        # Instantiate the typed configuration
        self.config: T = config_class()
        # Setup a basic logger
        self.logger = logging.getLogger(self.__class__.__name__)
        logging.basicConfig(level=logging.INFO)
        
        # Create a Databricks workspace client with or without credentials
        if self.config.databricks_host and self.config.databricks_token:
            # Local execution with credentials
            self.workspace_client = WorkspaceClient(
                host=self.config.databricks_host,
                token=self.config.databricks_token
            )
        else:
            # Notebook execution - no credentials needed
            self.workspace_client = WorkspaceClient()

    @classmethod
    def entrypoint(cls, *args, **kwargs):
        """
        Creates an instance of the task and runs it. If you
        want a consistent run pattern, place it here.
        """
        instance = cls(*args, **kwargs)
        instance.run()

    def run(self):
        """
        The main entrypoint for the task's execution.
        Override this in subclasses to implement custom logic.
        """
        self.logger.info("Base Task run method. Override in subclasses.") 