#!/usr/local/autopkg/python

import csv
import os

from autopkglib import Processor, ProcessorError

__all__ = ["CSVWriter"]


class CSVWriter(Processor):
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
        softwaretitle_name = self.env.get("softwaretitle_name")        
        csv_file = "/Users/adrien.pichard/Desktop/packagesupload/PKG_Catalog.csv"

        with open(csv_file, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([app_name, app_version, category, softwaretitle_name])
            
        self.env["CSVWriter_summary_result"] = {
            "summary_text": "The following new items were downloaded:",
            "data": {
                "App_name": self.env["app_name"],
                "App_version": self.env["app_version"],
                "App_category": self.env["category"]
            }
        }

if __name__ == "__main__":
    PROCESSOR = CSVWriter()
    PROCESSOR.execute_shell()
