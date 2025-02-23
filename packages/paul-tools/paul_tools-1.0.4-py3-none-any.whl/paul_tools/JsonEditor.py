from .__init__ import *

__all__ = ["JsonEditor"]


class JsonEditor:
    """
    Attributes:
        json (module): The json module for handling JSON operations.
        os (module): The os module for handling file paths.
        time (module): The time module for handling time operations.
        dirRoot (str): The root directory for JSON files.
        jsonDict (dict): The dictionary to store JSON data.
        jsonPath (str): The file path of the JSON file.
    Methods:
        write_json(mode: str = "wt"):
            Writes the current JSON dictionary to the file.
        save():
            Saves the JSON file with an updated timestamp.
        del_from_key(key: str | None = None):
            Deletes a key from the JSON dictionary.
        edit():
            Interactively edits the JSON dictionary.
    """

    def __init__(self, path: str | None = None):
        """
        Initializes the JsonEditor instance.
        Args:
            path (str | None): The path to the JSON file. If None, the user will be prompted to enter the path.
        Attributes:
            json (module): The imported json module.
            os (module): The imported os module.
            time (module): The imported time module.
            jsonDict (dict[str, str]): A dictionary to store JSON data.
            dirRoot (str): The root directory, default is ".".
            jsonPath (str): The path to the JSON file.
        Raises:
            FileNotFoundError: If the JSON file is not found, a new file will be created.
        """
        import json
        import os
        import time

        self.json = json
        self.os = os
        self.time = time
        self.jsonDict: dict[str, str] = {}
        self.dirRoot: str = "."

        if path is not None:
            self.jsonPath = path
        else:
            self.jsonPath = input("Enter the path to the JSON file: ")
        logger.debug(f"jsonPath: {self.jsonPath}")

        try:
            with open(self.jsonPath, "rt", encoding="utf-8") as f:
                self.jsonDict = self.json.load(f)
        except FileNotFoundError:
            self.write_json("xt")
            logger.debug(f"File not found: {self.jsonPath}")

    def write_json(self, mode: str = "wt"):
        """
        Write the contents of jsonDict to a JSON file specified by jsonPath.

        Args:
            mode (str): The file mode to open the file with. Defaults to "wt" (write text mode).

        Raises:
            IOError: If the file cannot be opened or written to.
        """
        with open(self.jsonPath, mode, encoding="utf-8") as f:
            self.json.dump(self.jsonDict, f, indent=2)
            f.write("\n")
            logger.debug(f"jsonDict: {self.jsonDict}")

    def save(self):
        """
        Save the current state of the JSON data to a file.

        This method writes the JSON data to a file in write text mode ("wt").
        """
        self.write_json("wt")
        logger.debug(f"Saved: {self.jsonPath}")

    def del_from_key(self, key: str | None = None):
        """
        Deletes an entry from the jsonDict attribute based on the provided key.

        Args:
            key (str | None): The key of the entry to delete. If None, the user will be prompted to input the key.

        Raises:
            KeyError: If the key is not found in the dictionary.
        """
        if key is None:
            delKey = input("key: ")
        else:
            delKey = key
        self.jsonDict.pop(delKey)
        logger.debug(f"Deleted: {delKey}")

    def edit(self):
        """
        Interactively edit the jsonDict attribute of the instance.
        This method enters an interactive loop where the current state of jsonDict is printed,
        and the user can input commands to modify it. The following commands are supported:
        - "save": Calls the save() method.
        - "del": Calls the del_from_key() method.
        - "del <key>": Deletes the specified key from jsonDict.
        - "<key>": Prints the value associated with the specified key in jsonDict.
        - "<key>=<value>": Updates jsonDict with the specified key-value pair.
        The loop continues until an EOFError is encountered (e.g., Ctrl+D is pressed).
        Raises:
            EOFError: When the end of input is reached.
        """
        import re

        try:
            while True:
                print(self.jsonDict)
                ip = input(">")
                match ip:
                    case "exit":
                        break
                    case "save":
                        self.save()
                        logger.debug("Saved")
                    case "del":
                        self.del_from_key()
                        logger.debug("Deleted")
                    case _:
                        reDel = re.search(r"^(del )(\S+)", ip)
                        if reDel:
                            logger.debug(f"reDel: {reDel.group(2)}")
                            self.del_from_key(reDel.group(2))
                            continue

                        _ = ip.split("=")
                        key: str = ""
                        value: str | None = None

                        if len(_) == 2:
                            key, value = _
                            logger.debug(f"key: {key}, value: {value}")
                        elif len(_) == 1:
                            key = _[0]
                            logger.debug(f"key: {key}")

                        if key == "":
                            continue
                        elif value is None:
                            logger.info(f"<{self.jsonDict.get(key, None)}")
                        else:
                            self.jsonDict.update(
                                {key: eval(value, globals={}, locals={})}
                            )
                            logger.debug(f"jsonDict: {self.jsonDict}")
        except EOFError:
            logger.debug("EOF")
