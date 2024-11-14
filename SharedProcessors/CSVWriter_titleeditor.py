#!/usr/local/autopkg/python

import csv
import os
import subprocess

from autopkglib import Processor, ProcessorError

__all__ = ["CSVWriter_titleeditor"]


class CSVWriter_titleeditor(Processor):
    """Writes app version and category to a CSV file."""

    input_variables = {
        "app_name": {
            "required": True,
            "description": "The app name."
        },
        "app_version": {
            "required": True,
            "description": "The app version."
        },
        "category": {
            "required": True,
            "description": "The app category."
        },
        "softwaretitle_name": {
            "required": True,
            "description": "The softwaretitle app name."
        },
        "app_minimum_version": {
            "required": False,
            "description": "The minimum supported OS for the app, may not exist"
        },
        "bundle_identifier": {
            "required": True,
            "description": "Bundle identifier of the app"
        }
    }
    output_variables = {
        "CSVWriter_summary_result": {
            "description": "App data to output"
        }
    }

    def main(self):
        app_name = self.env.get("app_name")
        app_version = self.env.get("app_version")
        category = self.env.get("category")
        bundle_identifier = self.env.get("bundle_identifier")
        softwaretitle_name = self.env.get("softwaretitle_name")
        app_minimum_version = self.env.get("app_minimum_version")
        from_patch_management = 1
        command = "scutil <<< 'show State:/Users/ConsoleUser' | awk '/Name :/ && ! /loginwindow/ { print $3 }'"
        loggedInUser = subprocess.check_output(command, shell=True).decode("utf-8").rstrip("\n")
        csv_file = f"/Users/{loggedInUser}/Desktop/packagesupload/PKG_Catalog.csv"

        with open(csv_file, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(
                [app_name, app_version, bundle_identifier, app_minimum_version, category, softwaretitle_name,
                 from_patch_management])

        self.env["CSVWriter_summary_result"] = {
            "summary_text": "The following new items were downloaded:",
            "data": {
                "App_name": self.env["app_name"],
                "App_version": self.env["app_version"],
                "App_category": self.env["category"],
                "App_minimum_version": self.env["app_minimum_version"],
                "App_bundle_identifier": self.env["bundle_identifier"]
            }
        }


if __name__ == "__main__":
    PROCESSOR = CSVWriter_titleeditor()
    PROCESSOR.execute_shell()
