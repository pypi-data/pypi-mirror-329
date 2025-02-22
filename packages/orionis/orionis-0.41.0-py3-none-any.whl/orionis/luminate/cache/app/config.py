from typing import Dict, Any
from orionis.luminate.contracts.cache.app.config_interface import ICacheConfig

class CacheConfig(ICacheConfig):
    """
    CacheConfig is a class that manages the registration, unregistration, and retrieval of configuration sections.

    Methods
    -------
    __init__()
        Initializes a new instance of the class with an empty configuration dictionary.
    register(section: str, data: Dict[str, Any])
        Registers a configuration section with its associated data.
    unregister(section: str)
        Unregisters a previously registered configuration section.
    get(section: str)
        Retrieves the configuration data for a specific section.
    """

    def __init__(self) -> None:
        """
        Initializes a new instance of the class with an empty configuration dictionary.

        Attributes:
            config (dict): A dictionary to store configuration settings.
        """
        self.config = {}

    def register(self, section: str, data: Dict[str, Any]) -> None:
        """
        Registers a configuration section.

        Parameters
        ----------
        section : str
            The name of the configuration section to register.
        data : dict
            The configuration data associated with the section.

        Raises
        ------
        ValueError
            If the section is already registered.
        """
        if section in self.config:
            raise ValueError(f"Configuration section '{section}' is already registered.")

        self.config[section] = data

    def unregister(self, section: str) -> None:
        """
        Unregisters a previously registered configuration section.

        Parameters
        ----------
        section : str
            The name of the configuration section to remove.

        Raises
        ------
        KeyError
            If the section is not found in the registered configurations.
        """
        if section not in self.config:
            raise KeyError(f"Configuration section '{section}' is not registered.")

        del self.config[section]

    def get(self, section: str) -> Dict[str, Any]:
        """
        Retrieves the configuration for a specific section.

        Parameters
        ----------
        section : str
            The name of the configuration section to retrieve.

        Returns
        -------
        dict
            The configuration data for the specified section.

        Raises
        ------
        KeyError
            If the requested section is not found.
        """
        if section not in self.config:
            raise KeyError(f"Configuration section '{section}' is not registered.")

        return self.config[section]
