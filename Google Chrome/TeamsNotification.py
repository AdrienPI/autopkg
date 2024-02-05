#!/usr/local/autopkg/python
# -*- coding: utf-8 -*-

import json
import requests

from autopkglib import Processor, ProcessorError

__all__ = ["TeamsNotification"]

class TeamsNotification(Processor):
    description = "Send notifications to Microsoft Teams via webhook."
    input_variables = {
        "webhook_url": {
            "required": True,
            "description": "The Microsoft Teams webhook URL.",
        },
    }
    output_variables = {
        "CSVWriter_summary_result": {
            "description": "The message to send to Microsoft Teams.",
        },
    }

    def send_notification(self, webhook_url, message):
        headers = {"Content-Type": "application/json"}
        payload = {
            "text": message,
        }

        try:
            response = requests.post(webhook_url, data=json.dumps(payload), headers=headers)
            response.raise_for_status()
            self.output(f"Notification sent successfully. Message: {message}")
        except requests.exceptions.RequestException as e:
            raise ProcessorError(f"Failed to send notification: {e}")

    def main(self):
        webhook_url = self.env.get("webhook_url")
        payload = self.env["CSVWriter_summary_result"]
        
        summary_text = payload.get('summary_text', {})
        data = payload.get('data', {})
        app_category = data.get('App_category', '')
        app_name = data.get('App_name', '')
        app_version = data.get('App_version', '')
        message = f"{summary_text} // Name: {app_name} Version: {app_version} Category: {app_category}"

        self.send_notification(webhook_url, message)

if __name__ == "__main__":
    processor = TeamsNotification()
    processor.execute_shell()
