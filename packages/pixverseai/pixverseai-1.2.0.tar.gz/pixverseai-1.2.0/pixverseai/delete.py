#@title delete video
import requests
import os
import uuid

def eliminar_video():
    token = os.environ.get("JWT_TOKEN")
    video_ids = int(os.environ.get("VIDEO_ID"))  # Puedes agregar más IDs si es necesario
    url = "https://app-api.pixverse.ai/creative_platform/video/delete"

    headers = {
        "Host": "app-api.pixverse.ai",
        "Connection": "keep-alive",
        "X-Platform": "Web",
        "sec-ch-ua-platform": "Windows",
        "Accept-Language": "es-ES",
        "sec-ch-ua": "Not A(Brand;v=8, Chromium;v=132, Google Chrome;v=132",
        "sec-ch-ua-mobile": "?0",
        "Ai-Trace-Id": str(uuid.uuid4()),
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

    # Asegúrate de que video_ids esté en una lista, incluso si es un solo valor
    if not isinstance(video_ids, list):
        video_ids = [video_ids]

    data = {
        "video_ids": video_ids,
        "platform": "web"
    }

    response = requests.post(url, headers=headers, json=data)

    return response.json()
