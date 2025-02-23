# MIT License
#
# Copyright (c) 2025 Clivern
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import requests
import json
from datetime import datetime


class PagerdutyClient:
    """Client for interacting with the PagerDuty Events API v2."""

    def __init__(self, integration_key):
        """Initialize with integration key.

        Args:
            integration_key (str): PagerDuty integration key (service key).
        """
        self.integration_key = integration_key
        self.events_api_url = "https://events.pagerduty.com/v2/enqueue"

    def trigger_alert(
        self, summary, severity, source, component, links=None, custom_details=None
    ):
        """Trigger a new alert in PagerDuty.

        Args:
            summary (str): Alert summary.
            severity (str): Alert severity (e.g., 'info', 'warning', 'error', 'critical').
            source (str): Alert source (e.g., monitoring tool name).
            component (str): Affected component.
            links (list, optional): List of link dictionaries (href, text). Defaults to None.
            custom_details (dict, optional): Custom alert details. Defaults to None.

        Returns:
            dict: PagerDuty API response.
        """
        payload = {
            "routing_key": self.integration_key,
            "event_action": "trigger",
            "payload": {
                "summary": summary,
                "timestamp": datetime.utcnow().isoformat(),
                "severity": severity,
                "source": source,
                "component": component,
            },
        }

        if links:
            payload["links"] = links

        if custom_details:
            if "custom_details" not in payload["payload"]:
                payload["payload"]["custom_details"] = {}
            payload["payload"]["custom_details"].update(custom_details)

        headers = {"Content-Type": "application/json"}

        response = requests.post(
            self.events_api_url, data=json.dumps(payload), headers=headers
        )
        response.raise_for_status()
        return response.json()

    def resolve_alert(self, dedup_key):
        """Resolve an alert in PagerDuty.

        Args:
            dedup_key (str): Deduplication key of the alert to resolve.

        Returns:
            dict: PagerDuty API response.
        """
        payload = {
            "routing_key": self.integration_key,
            "dedup_key": dedup_key,
            "event_action": "resolve",
        }

        headers = {"Content-Type": "application/json"}

        response = requests.post(
            self.events_api_url, data=json.dumps(payload), headers=headers
        )
        response.raise_for_status()
        return response.json()

    def acknowledge_alert(self, dedup_key):
        """Acknowledge an alert in PagerDuty.

        Args:
            dedup_key (str): Deduplication key of the alert to acknowledge.

        Returns:
            dict: PagerDuty API response.
        """
        payload = {
            "routing_key": self.integration_key,
            "dedup_key": dedup_key,
            "event_action": "acknowledge",
        }

        headers = {"Content-Type": "application/json"}

        response = requests.post(
            self.events_api_url, data=json.dumps(payload), headers=headers
        )
        response.raise_for_status()
        return response.json()


def get_pagerduty_client(integration_key: str) -> PagerdutyClient:
    """Get a PagerdutyClient instance.

    Args:
        integration_key (str): PagerDuty integration key.

    Returns:
        PagerdutyClient: An initialized client.
    """
    return PagerdutyClient(integration_key)


# Example usage:
if __name__ == "__main__":
    integration_key = (
        "xxxxxxxxxxxxxxxxxxxxxxxxxxx"  # Replace with your actual integration key
    )
    pagerduty_alert = PagerdutyClient(integration_key)

    links = [
        {
            "href": "https://example.com/890d2020-c132-41f3-bb55-d51d53c15bf0",
            "text": "AI Assistant Help",
        }
    ]

    response = pagerduty_alert.trigger_alert(
        summary="High CPU Usage",
        severity="error",
        source="MyServer",
        component="CPU",
        links=links,
        custom_details={
            "region": "us-west-2",
            "threshold": "90%",
            "vgid": "890d2020-c132-41f3-bb55-d51d53c15bf0",
        },
    )

    if response:
        print("PagerDuty API Response:", response)
    else:
        print("Failed to send PagerDuty alert.")

    print(pagerduty_alert.acknowledge_alert(response["dedup_key"]))
