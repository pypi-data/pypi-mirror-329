#@title login
import requests
import os

def obtener_token(username, password):
    """Realiza una solicitud POST para autenticarse y devuelve el token."""

    url = "https://app-api.pixverse.ai/creative_platform/login"

    headers = {
        "X-Platform": "Web",
        "sec-ch-ua-platform": "\"Windows\"",
        "Accept-Language": "es-ES",
        "sec-ch-ua": "\"Not A(Brand\";v=\"8\", \"Chromium\";v=\"132\", \"Google Chrome\";v=\"132\"",
        "sec-ch-ua-mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "Origin": "https://app.pixverse.ai",
        "Referer": "https://app.pixverse.ai/",
    }

    payload = {
        "Username": username,
        "Password": password
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Lanza un error si el código de estado no es 2xx

        data = response.json()

        # Extraer el token si existe
        if "Resp" in data and "Result" in data["Resp"] and "Token" in data["Resp"]["Result"]:
            return data["Resp"]["Result"]["Token"]
        else:
            return None  # Retorna None si no se encuentra el token

    except requests.RequestException as e:
        print("Error en la solicitud:", e)
        return None

