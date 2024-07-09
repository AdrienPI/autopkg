#!/usr/bin/python
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

    def send_notification(self, webhook_url, message, app_name, app_category, app_version):
        headers = {"Content-Type": "application/json"}
        payload = {
            "type": "message",
            "attachments": [
                {
                    "contentType": "application/vnd.microsoft.card.adaptive",
                    "content": {
                        "type": "AdaptiveCard",
                        "body": [
                            {
                                "type": "TextBlock",
                                "text": "Patch Management",
                                "weight": "bolder",
                                "size": "medium"
                            },
                            {
                                "type": "Container",
                                "items": [
                                    {
                                        "type": "TextBlock",
                                        "text": message,
                                        "wrap": True
                                    },
                                    {
                                        "type": "FactSet",
                                        "facts": [
                                            {
                                                "title": "Nom Application:",
                                                "value": app_name
                                            },
                                            {
                                                "title": "Version:",
                                                "value": app_version
                                            },
                                            {
                                                "title": "Categorie:",
                                                "value": app_category
                                            },
                                        ]
                                    }
                                ]
                            }
                        ]
                    }
                }
            ]
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
        message = f"\u2705 {summary_text}:"

        self.send_notification(webhook_url, message, app_name, app_category, app_version)


if __name__ == "__main__":
    processor = TeamsNotification()
    processor.execute_shell()
