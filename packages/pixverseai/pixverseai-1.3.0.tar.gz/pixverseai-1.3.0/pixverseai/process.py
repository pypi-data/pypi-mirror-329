#@title Poroceso de descarga
import requests
import os
import time
import uuid


def obtener_detalle_video(video_id, token):
    url = "https://app-api.pixverse.ai/creative_platform/video/list/detail"

    headers = {
        "Host": "app-api.pixverse.ai",
        "Connection": "keep-alive",
        "X-Platform": "Web",
        "sec-ch-ua-platform": "\"Windows\"",
        "Accept-Language": "es-ES",
        "sec-ch-ua": "\"Not A(Brand\";v=\"8\", \"Chromium\";v=\"132\", \"Google Chrome\";v=\"132\"",
        "sec-ch-ua-mobile": "?0",
        "Ai-Trace-Id": str(uuid.uuid4()),
        "Ai-Sign": "a7dcb2925913caafd42441bed31b048e3423cdeb2529e37ee112ff17609998c0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "Token": token,
        "Origin": "https://app.pixverse.ai",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://app.pixverse.ai/",
        "Cache-Control": "no-cache",
        "Accept-Encoding": "gzip, deflate"
    }

    payload = {
        "video_id": video_id,
        "platform": "web"
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return None

def descargar_video(url, nombre_archivo="video.mp4"):
    print(f"📥 Descargando video desde: {url}")
    response = requests.get(url, stream=True)

    if response.status_code == 200:
        with open(nombre_archivo, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
        print(f"✅ Video descargado: {nombre_archivo}")
    else:
        print(f"❌ Error al descargar el video. Código: {response.status_code}")

# 🔹 Obtener credenciales desde variables de entorno
def process_download():
    API_KEY = os.environ.get("JWT_TOKEN")
    video_ids = os.environ.get("VIDEO_ID")

    if not API_KEY or not video_ids:
        print("⚠️ Falta definir API_KEY o VIDEO_ID en las variables de entorno.")
    else:
        video_id = int(video_ids)

        while True:
            resultado = obtener_detalle_video(video_id, API_KEY)

            if resultado and resultado.get("ErrCode") == 0:
                status = resultado["Resp"]["video_status"]
                print(f"⏳ Estado actual del video: {status}")

                if status == 1:  # Cuando el video_status llegue a 1, descargar video
                    video_url = resultado["Resp"]["url"]
                    if video_url:
                        descargar_video(video_url)
                    break  # Salir del bucle
            else:
                print(f"⚠️ Error en la respuesta: {resultado}")

            time.sleep(10)  # Esperar 10 segundos antes de volver a consultar