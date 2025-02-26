#@title extender video 5 segundos
import requests
import os
import uuid

def extender_video(prompt, negative_prompt, seed, duration, quality, motion_mode, model, customer_video_duration):
    # Configuración global
    token = os.environ.get("JWT_TOKEN")
    customer_video_path = os.environ.get("CUSTOMER_VIDEO_PATH")
    customer_video_url = os.environ.get("CUSTOMER_VIDEO_URL")
    customer_video_last_frame_url = os.environ.get("LAST_FRAME")
    BASE_API_URL = "https://app-api.pixverse.ai"
    endpoint = f"{BASE_API_URL}/creative_platform/video/extend"

    # Headers fijos
    headers = {
        "Host": "app-api.pixverse.ai",
        "Connection": "keep-alive",
        "X-Platform": "Web",
        "sec-ch-ua-platform": "Windows",
        "Accept-Language": "es-ES",
        "sec-ch-ua": "Not A(Brand;v=8, Chromium;v=132, Google Chrome;v=132",
        "sec-ch-ua-mobile": "?0",
        "Ai-Trace-Id": str(uuid.uuid4()),
        "Refresh": "credit",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "Token": token,  # Usa el token JWT desde las variables de entorno
        "Origin": "https://app.pixverse.ai",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://app.pixverse.ai/",
        "Accept-Encoding": "gzip, deflate"
    }

    # Datos del cuerpo de la solicitud
    data = {
        "customer_video_path": customer_video_path,
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "seed": seed,
        "duration": duration,
        "quality": quality,
        "motion_mode": motion_mode,
        "model": model,
        "customer_video_url": customer_video_url,
        "customer_video_duration": customer_video_duration,
        "customer_video_last_frame_url": customer_video_last_frame_url
    }

    # Realizar la solicitud POST
    response = requests.post(endpoint, headers=headers, json=data)
    response.raise_for_status()  # Lanza una excepción si la respuesta no es 200 OK

    data = response.json()

    # Validar si la respuesta es exitosa y tiene video_id
    if data.get("ErrCode") == 0 and data.get("Resp") and "video_id" in data["Resp"]:
        os.environ["VIDEO_ID"] = str(data["Resp"]["video_id"])
        return data["Resp"]["video_id"]
    elif data.get("ErrCode") == 500043:  # Error de créditos agotados
        return "❌ No quedan créditos disponibles. Considera actualizar tu membresía o comprar más créditos."
    else:
        return f"⚠️ Error inesperado: {data}"
