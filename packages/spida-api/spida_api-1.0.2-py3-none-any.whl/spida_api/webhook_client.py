import json
import requests
from typing import Literal, List


class WebhookClient:
    def __init__(self, url_server: str, api_key: str):
        self.url_server = url_server
        self.api_key = api_key
        self.base_url = f"https://{self.url_server}/projectmanager/webhookAPI"

    def register_webhook(self, target_url: str, channel: Literal["Project", "Status", "Phase", "Form", "File", "Tag", "Action"],
                         event: str = ".*", lease_time: int = 86400) -> requests.Response:
        url = f"{self.base_url}/register?apiToken={self.api_key}"
        headers = {'content-type': 'application/json'}
        data = {
            'url': target_url,
            'channel': channel,
            'leaseTime': lease_time,
            'eventFilter': event
        }

        return requests.post(url=url, data=json.dumps(data), headers=headers)

    def unregister_webhook(self, hook_ids: List[str]) -> List[requests.Response]:
        url = f"{self.base_url}/unregister?apiToken={self.api_key}"
        headers = {'content-type': 'application/json'}

        responses = []
        for hook_id in hook_ids:
            data = {'hookId': hook_id}
            r = requests.post(url=url, data=json.dumps(data), headers=headers)
            responses.append(r)

        return responses

    def renew_webhook(self, hook_ids: List[str], lease_time: int = 86400) -> List[requests.Response]:
        url = f"{self.base_url}/renew?apiToken={self.api_key}"
        headers = {'content-type': 'application/json'}

        responses = []
        for hook_id in hook_ids:
            data = {'hookId': hook_id, "leaseTime": lease_time}
            r = requests.post(url=url, data=json.dumps(data), headers=headers)
            responses.append(r)

        return responses

    def view_webhooks(self) -> requests.Response:
        url = f"{self.base_url}/view?apiToken={self.api_key}"
        return requests.get(url=url)
