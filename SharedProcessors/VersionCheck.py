#!/usr/local/bin/pythoncipeo

import os
from autopkglib import Processor, ProcessorError

__all__ = ["VersionCheck"]

class VersionCheck(Processor):
    description = "Checks if a specific version of a package is already downloaded."
    input_variables = {
        "version": {
            "required": True,
            "description": "The version of the package to check."
        },
        "pkg_path": {
            "required": True,
            "description": "The directory to check for the existence of the package version."
        }
    }
    output_variables = {
        "version_exists": {
            "description": "Boolean indicating if the specified version exists in the directory."
        }
    }

    def main(self):
        version = self.env.get("version")
        pkg_path = self.env.get("pkg_path")

        # Check if the specified version exists in the directory
        if version in pkg_path:
            self.env["version_exists"] = True
            self.output(f"Version {version} is already downloaded.")
            return
        # Version not found
        self.env["version_exists"] = False
        self.output(f"Version {version} is not yet downloaded.")


if __name__ == "__main__":
    processor = VersionCheck()
    processor.execute_shell()