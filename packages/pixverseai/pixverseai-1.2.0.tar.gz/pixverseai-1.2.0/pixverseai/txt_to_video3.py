#@title texto a video v3 ESTILO TEST
import requests
import os
import uuid

def ttv3(prompt, aspect_ratio, negative_prompt, seed, model, duration, quality, motion_mode, lip_sync_tts_speaker_id, style=""):
    token = os.environ.get("JWT_TOKEN")
    url = "https://app-api.pixverse.ai/creative_platform/video/t2v"

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
        "Token": token,
        "Origin": "https://app.pixverse.ai",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://app.pixverse.ai/",
        "Accept-Encoding": "gzip, deflate"
    }

    data = {
        "prompt": prompt,
        "aspect_ratio": aspect_ratio,
        "negative_prompt": negative_prompt,
        "seed": seed,
        "model": model,
        "duration": duration,
        "quality": quality,
        "motion_mode": motion_mode,
        "lip_sync_tts_speaker_id": lip_sync_tts_speaker_id
    }

    # Añadir el campo "style" solo si no está vacío
    if style:
        data["style"] = style

    response = requests.post(url, headers=headers, json=data)
    data = response.json()

    # Validar si la respuesta es exitosa y tiene video_id
    if data.get("ErrCode") == 0 and data.get("Resp") and "video_id" in data["Resp"]:
        os.environ["VIDEO_ID"] = str(data["Resp"]["video_id"])
        return data["Resp"]["video_id"]
    elif data.get("ErrCode") == 500043:  # Error de créditos agotados
        return "❌ No quedan créditos disponibles. Considera actualizar tu membresía o comprar más créditos."
    else:
        return f"⚠️ Error inesperado: {data}"

