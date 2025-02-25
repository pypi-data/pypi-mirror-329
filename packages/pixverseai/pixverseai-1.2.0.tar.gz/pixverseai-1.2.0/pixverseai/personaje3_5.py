#@title PERSONAJE V3.5 + ESTILO
import requests
import uuid
import os  # Asegura que puedes acceder a variables de entorno

def ptv(PROMPT, ASPECT_RATIO, negative_prompt, SEED, DURATION, QUALITY, CAMERA_MOVEMENT, MOTION_MODE, MODEL, style=""):
    TOKEN = os.environ.get("JWT_TOKEN")
    ASSET_ID = int(os.environ.get("ASSET_ID"))

    url = "https://app-api.pixverse.ai/creative_platform/video/c2v"

    headers = {
        "Host": "app-api.pixverse.ai",
        "Connection": "keep-alive",
        "X-Platform": "Web",
        "sec-ch-ua-platform": "\"Windows\"",
        "Accept-Language": "es-ES",
        "sec-ch-ua": "\"Not A(Brand\";v=\"8\", \"Chromium\";v=\"132\", \"Google Chrome\";v=\"132\"",
        "sec-ch-ua-mobile": "?0",
        "Ai-Trace-Id": str(uuid.uuid4()),
        "Refresh": "credit",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "Token": TOKEN,
        "Origin": "https://app.pixverse.ai",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://app.pixverse.ai/",
        "Accept-Encoding": "gzip, deflate"
    }

    payload = {
        "asset_id": ASSET_ID,
        "prompt": PROMPT,
        "aspect_ratio": ASPECT_RATIO,
        "negative_prompt": negative_prompt,
        "seed": SEED,
        "duration": DURATION,
        "quality": QUALITY,
        "camera_movement": CAMERA_MOVEMENT,
        "motion_mode": MOTION_MODE,
        "model": MODEL
    }

    # Añadir el campo "style" solo si no está vacío
    if style:
        payload["style"] = style


    response = requests.post(url, headers=headers, json=payload)
    data = response.json()

    # Validar si la respuesta es exitosa y tiene video_id
    if data.get("ErrCode") == 0 and data.get("Resp") and "video_id" in data["Resp"]:
        os.environ["VIDEO_ID"] = str(data["Resp"]["video_id"])
        return data["Resp"]["video_id"]
    elif data.get("ErrCode") == 500043:  # Error de créditos agotados
        return "❌ No quedan créditos disponibles. Considera actualizar tu membresía o comprar más créditos."
    else:
        return f"⚠️ Error inesperado: {data}"

