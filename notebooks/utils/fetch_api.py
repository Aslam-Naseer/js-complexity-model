import requests
import json


def fetch_features(js_code, url, show_logs=True):
    payload = {"code": js_code}

    try:
        response = requests.post(url, json=payload, timeout=5)

        if response.status_code in [200, 201]:
            data = response.json()
            if show_logs:
                print("Features fetched successfully.")

            return data["analysisTree"]["nestedFunctions"][0]["analysis"]["features"]
        else:
            if show_logs:
                print(f"Error: Received status code {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Connection Error: {e}")
