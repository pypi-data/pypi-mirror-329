#@title imagen a video V3.5 + ESTILO
import requests
import uuid
import os

def itv35(prompt, aspect_ratio, negative_prompt, seed, model, duration, quality, camera_movement, motion_mode, lip_sync_tts_speaker_id, style=""):
    token = os.environ.get("JWT_TOKEN")
    customer_img_path = os.environ.get("CUSTOMER_IMG_PATH")
    customer_img_url = os.environ.get("CUSTOMER_IMG_URL")
    url = "https://app-api.pixverse.ai/creative_platform/video/i2v"

    headers = {
        "Host": "app-api.pixverse.ai",
        "Connection": "keep-alive",
        "X-Platform": "Web",
        "Sec-CH-UA-Platform": "\"Windows\"",
        "Accept-Language": "es-ES",
        "Sec-CH-UA": "\"Not A(Brand\";v=\"8\", \"Chromium\";v=\"132\", \"Google Chrome\";v=\"132\"",
        "Sec-CH-UA-Mobile": "?0",
        "Ai-Trace-Id": str(uuid.uuid4()),
        "Refresh": "credit",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "Token": token,  # Reemplaza con tu token
        "Origin": "https://app.pixverse.ai",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://app.pixverse.ai/",
        "Accept-Encoding": "gzip, deflate"
    }

    payload = {
        "customer_img_path": customer_img_path,
        "prompt": prompt,
        "aspect_ratio": aspect_ratio,
        "negative_prompt": negative_prompt,
        "seed": seed,
        "model": model,
        "duration": duration,
        "quality": quality,
        "camera_movement": camera_movement,
        "motion_mode": motion_mode,
        "customer_img_url": customer_img_url,
        "lip_sync_tts_speaker_id": lip_sync_tts_speaker_id
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
