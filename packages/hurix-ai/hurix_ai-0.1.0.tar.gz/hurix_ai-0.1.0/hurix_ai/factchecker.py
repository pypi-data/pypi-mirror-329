import requests
import json

class FactChecker:
    def __init__(self, api_key: str, base_url: str, model_name: str):
        self.api_key = api_key
        self.model_name = model_name
        self.base_url = base_url

    def fact_check(self, text: str):
        headers = {"Authorization": self.api_key}
        payload = {"model": self.model_name, "text": text}

        response = requests.post(f"{self.base_url}/factverification", json=payload, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            return {"error": response.text, "status_code": response.status_code}
        
    def fact_check_streaming(self, text: str):
        headers = {"Authorization": self.api_key}
        payload = {"model": self.model_name, "text": text}

        with requests.post(f"{self.base_url}/factverification-streaming", json=payload, headers=headers, stream=True) as response:
            if response.status_code != 200:
                yield {"error": response.text, "status_code": response.status_code}
            else:
                for line in response.iter_lines(decode_unicode=True):
                    if line.strip():
                        yield json.loads(line.strip())