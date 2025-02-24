import os
import threading
from pathlib import Path
from orionis.contracts.services.files.i_path_service import IPathService

class PathService(IPathService):
    """
    A thread-safe singleton class for resolving and validating absolute paths.

    This class resolves the absolute path for a given relative directory or file path
    based on the script's execution directory. It ensures that the requested path is valid
    (either a directory or a file) and provides methods to retrieve the resolved path.

    Attributes
    ----------
    base_path : Path
        The base path (current working directory) used for resolving relative paths.
    route : str
        The resolved absolute path to the directory or file.
    """

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        """
        Override the __new__ method to ensure only one instance of the class is created.

        Returns
        -------
        PathService
            The singleton instance of the PathService class.
        """
        # Use the lock to ensure thread-safe instantiation
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """
        Initializes the instance by setting the base path to the current working directory.
        """
        self.base_path = Path(os.getcwd())

    def resolve(self, route: str) -> str:
        """
        Resolves and returns the absolute path as a string.

        This method combines the base path (current working directory) with the provided
        relative path, resolves it to an absolute path, and validates that it exists
        and is either a directory or a file.

        Parameters
        ----------
        route : str
            The relative directory or file path to be resolved.

        Returns
        -------
        str
            The absolute path to the directory or file.

        Raises
        ------
        ValueError
            If the resolved path does not exist or is neither a directory nor a file.
        """
        # Combine base path with the relative route
        real_path = (self.base_path / route).resolve()

        # Validate that the path exists and is either a directory or a file
        if not real_path.exists():
            raise ValueError(f"The requested path does not exist: {real_path}")
        if not (real_path.is_dir() or real_path.is_file()):
            raise ValueError(f"The requested path is neither a directory nor a file: {real_path}")

        self.route = str(real_path)
        return self.route

    def __str__(self) -> str:
        """
        Returns the resolved absolute path as a string (dunder method).

        Returns
        -------
        str
            The absolute path to the directory or file.
        """
        return self.route