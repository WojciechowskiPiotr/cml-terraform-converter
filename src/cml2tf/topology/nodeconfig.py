from typing import Dict, List, Union


class NodeConfig:
    """Handle node configurations. With 2.7.0, CML supports multiple configuration
    files per node. This class handles the two variants:
        - a simple string (pre 2.7 behavior)
        - a list of objects, key is "name", value is "content"
    This class can then serialize the content either into the proper HCL for
    multi-line configs (to be done as the provider does not support it, yet)
    or into a string representation.
    """

    def __init__(self, label: str, config: Union[str, List[Dict[str, str]]]) -> None:
        self._config = config
        self._label = label

    def empty(self) -> bool:
        "returns True when the configuration is empty."
        return len(self.out()) == 0

    def oneline(self) -> bool:
        "returns True when the configuration has exactly one line."
        return len(self.out().split("\n")) == 1

    def out(self, indent=0) -> str:
        """simply return the configuration string, indented to fit into the HCL
        here-doc. For the 2.7.0 / list configuration object, it returns only
        the first configuration from the list. To be changed when the CML2 TF
        provider supports multi-line configs.
        """
        if isinstance(self._config, list):
            if len(self._config) == 0:
                return ""
            config = self._config[0]["content"]
            # TODO: need to process multi-configs when TF provider supports them!
            # for item in self._config:
            #     if item["name"] == "default":
            #         return item["content"]
        elif isinstance(self._config, str):
            config = self._config
        else:
            raise ValueError("unhandled config type", type(self._config))
        lines = [" " * indent + line for line in config.split("\n")]
        return "\n".join(lines)

    def fileout(self) -> str:
        """return the filename of the file that has been created and where the
        configuration for the node is stored.
        """
        filename = ""
        if isinstance(self._config, list):
            # this should never be called for an empty file
            assert len(self._config) > 0
            name = self._config[0]["name"]
            config = self._config[0]["content"]
            # TODO: need to process multi-configs when TF provider supports them!
            # for item in self._config:
            #     if item["name"] == "default":
            #         return item["content"]
            filename = f"{self._label}-{name}.cfg"
        elif isinstance(self._config, str):
            config = self._config
            filename = f"{self._label}.cfg"
        else:
            raise ValueError("unhandled config type", type(self._config))

        with open(filename, "w") as fh:
            fh.write(config)
        return filename
