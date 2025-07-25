import requests
from dotenv import load_dotenv
import os
import uuid

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
auth = os.getenv("AUTHORISATION")


def get_token():
    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
    payload = "scope=GIGACHAT_API_PERS"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'RqUID': str(uuid.uuid4()),
        'Authorization': f"Basic {auth}"
    }

    response = requests.post(url, headers=headers, data=payload, verify=False)

    response_json = response.json()
    print("Token response:", response_json)
    if "access_token" not in response_json:
        raise Exception(f"Failed to get access token: {response_json}")
    return response_json["access_token"]

def generate_examples(description):
    token = get_token()

    prompt = f"Сгенерируй 20 различных пользовательских фраз для следующего интента без нумераций и чтобы интенты были более разговорными: '{description}'."

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "GigaChat-Pro",
        "messages": [
            {"role": "system", "content": "Ты помощник по генерации NLU примеров."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.8,
        "top_p": 0.95,
        "n": 1
    }

    api_url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
    response = requests.post(api_url, headers=headers, json=data, verify=False)
    response.raise_for_status()
    result_text = response.json()["choices"][0]["message"]["content"]

    return [line.strip("- ").strip() for line in result_text.split("\n") if line.strip()]
