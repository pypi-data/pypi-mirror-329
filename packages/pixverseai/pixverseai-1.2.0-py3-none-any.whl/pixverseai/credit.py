#@title credit
import requests
import uuid
import os

def obtener_creditos():
    token = os.environ.get("JWT_TOKEN")
    url = "https://app-api.pixverse.ai/creative_platform/user/credits"

    headers = {
        "Host": "app-api.pixverse.ai",
        "Connection": "keep-alive",
        "X-Platform": "Web",
        "sec-ch-ua-platform": "\"Windows\"",
        "Accept-Language": "es-ES",
        "sec-ch-ua": "\"Not A(Brand\";v=\"8\", \"Chromium\";v=\"132\", \"Google Chrome\";v=\"132\"",
        "sec-ch-ua-mobile": "?0",
        "Ai-Trace-Id": str(uuid.uuid4()),  # Genera un nuevo Ai-Trace-Id dinámico
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Token": token,
        "Origin": "https://app.pixverse.ai",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://app.pixverse.ai/",
        "Accept-Encoding": "gzip, deflate"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()

        # Extraer el valor de 'credit_package'
        credit_package = data.get("Resp", {}).get("credit_package", 0)
        os.environ["CREDIT"] = str(credit_package)
        return credit_package
    else:
        return f"Error {response.status_code}: {response.text}"


