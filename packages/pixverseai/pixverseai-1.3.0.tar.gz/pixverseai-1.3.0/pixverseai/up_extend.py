#@title upload video extend
import requests
import uuid
import os
import mimetypes
from datetime import datetime
import base64
import hmac
import hashlib

# Configuración global
BASE_API_URL = "https://app-api.pixverse.ai"
OSS_UPLOAD_URL = "https://pixverse-fe-upload.oss-accelerate.aliyuncs.com"

# ------------------------- FUNCIONES PRINCIPALES ------------------------- #

def obtener_ultimo_frame(token, video_path, duration):
    # Configuración global
    BASE_API_URL = "https://app-api.pixverse.ai"
    endpoint = f"{BASE_API_URL}/creative_platform/video/frame/last"

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
        "video_path": video_path,
        "duration": duration
    }

    try:
        # Realizar la solicitud POST
        response = requests.post(endpoint, headers=headers, json=data)
        response.raise_for_status()  # Lanza una excepción si la respuesta no es 200 OK

        # Extraer la URL del último frame
        last_frame_url = response.json()["Resp"]["last_frame"]
        os.environ["LAST_FRAME"] = last_frame_url
        return last_frame_url

    except Exception as e:
        print(f"🚨 Error al obtener el último frame: {str(e)}")
        if hasattr(e, 'response') and e.response:
            print(f"📄 Respuesta del servidor: {e.response.text[:300]}...")
        return None


def obtener_token_subida(headers):
    """
    Obtiene las credenciales de subida desde la API con validaciones mejoradas
    """
    url = f"{BASE_API_URL}/creative_platform/getUploadToken"

    try:
        response = requests.post(url, headers=headers, timeout=15, verify=True)
        response.raise_for_status()

        json_data = response.json()

        if json_data['ErrCode'] != 0:
            error_msg = json_data.get('ErrMsg', 'Error desconocido')
            raise ValueError(f"Error del API: {error_msg} (Código: {json_data['ErrCode']})")

        credenciales = json_data['Resp']
        required_keys = {'Ak', 'Sk', 'Token'}
        if not required_keys.issubset(credenciales.keys()):
            missing = required_keys - credenciales.keys()
            raise ValueError(f"Credenciales incompletas. Faltantes: {missing}")

        # Validaciones actualizadas
        if not isinstance(credenciales['Ak'], str) or not credenciales['Ak'].startswith('STS.'):
            raise ValueError("Access Key (Ak) inválida")

        if not isinstance(credenciales['Sk'], str) or len(credenciales['Sk']) < 30:
            raise ValueError("Formato de Secret Key (Sk) inválido")

        if not credenciales['Token'].startswith('CAIS'):
            raise ValueError("Token de seguridad inválido")

        return credenciales

    except Exception as e:
        raise RuntimeError(f"Falló la obtención del token: {str(e)}")

def subir_video_oss(video_path, upload_credentials):
    """Sube el video al servicio de almacenamiento OSS de Alibaba"""
    ak = upload_credentials['Ak']
    sk = upload_credentials['Sk']
    token = upload_credentials['Token']
    bucket_name = "pixverse-fe-upload"
    object_path = f"upload/{uuid.uuid4()}.mp4"  # Cambia la extensión a .mp4 o el formato de video que uses
    mime_type = 'video/mp4'  # Cambia el tipo MIME según el formato del video
    oss_date = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')

    # Construcción del string para firmar
    canonicalized_oss_headers = "\n".join(sorted([
        f'x-oss-content-type:{mime_type}',
        f'x-oss-date:{oss_date}',
        f'x-oss-forbid-overwrite:true',
        f'x-oss-security-token:{token}'
    ]))

    string_to_sign = "\n".join([
        "PUT",
        "",
        mime_type,
        oss_date,
        canonicalized_oss_headers,
        f"/{bucket_name}/{object_path}"
    ])

    # Generación de la firma
    signature = base64.b64encode(
        hmac.new(sk.encode('utf-8'), string_to_sign.encode('utf-8'), hashlib.sha1).digest()
    ).decode('utf-8')

    headers = {
        'Authorization': f"OSS {ak}:{signature}",
        'x-oss-date': oss_date,
        'x-oss-security-token': token,
        'x-oss-forbid-overwrite': 'true',
        'x-oss-content-type': mime_type,
        'Content-Type': mime_type,
        'Host': OSS_UPLOAD_URL.split('//')[1]  # Extrae el host de la URL OSS
    }

    try:
        with open(video_path, 'rb') as f:
            response = requests.put(
                f"https://{headers['Host']}/{object_path}",
                headers=headers,
                data=f,
                timeout=30
            )
        response.raise_for_status()
        return {
            'nombre': object_path.split('/')[-1],
            'ruta': object_path,
            'tamaño': os.path.getsize(video_path)
        }

    except Exception as e:
        print(f"\n🔍 Debug - String para firmar:\n{string_to_sign}")
        print(f"🔍 SK usado: {sk[:5]}...{sk[-5:]}")
        raise

def registrar_medios(media_info, headers):
    """Registra los medios subidos en el sistema"""
    url = f"{BASE_API_URL}/creative_platform/media/upload"
    payload = {
        "name": media_info['nombre'],
        "path": media_info['ruta'],
        "type": 1  # 1 para videos
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        json_data = response.json()

        if json_data['ErrCode'] != 0:
            raise ValueError(json_data['ErrMsg'])

        return json_data['Resp']
    except Exception as e:
        raise RuntimeError(f"Fallo en registro: {str(e)}")

# ------------------------- PROGRAMA PRINCIPAL ------------------------- #
def up_video_extend(video_local):
    API_KEY = os.environ.get("JWT_TOKEN")
    headers = {
        'X-Platform': 'Web',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
        'Token': API_KEY  # Reemplazar con tu token real
    }

    try:
        print("\n🎥 Paso 1/5: Subiendo video...")

        print("\n🔐 Paso 2/5: Obteniendo token...")
        creds = obtener_token_subida(headers)

        print("\n☁️ Paso 3/5: Subiendo a OSS...")
        media_info = subir_video_oss(video_local, creds)
        print(f"✔️ Subido: https://media.pixverse.ai/{media_info['ruta']}")
        os.environ["CUSTOMER_VIDEO_PATH"] = str(media_info['ruta'])
        os.environ["CUSTOMER_VIDEO_URL"] = str(f"https://media.pixverse.ai/{media_info['ruta']}")
        #print(str(media_info['ruta']))
        print(str(f"https://media.pixverse.ai/{media_info['ruta']}"))

        print("\n📝 Paso 4/5: Registrando...")
        registro_resp = registrar_medios(media_info, headers)
        #print(f"🆔 Respuesta Registro: {registro_resp}")

        if registro_resp:
          # Configuración de las variables de entorno (opcional)
          token = os.environ.get("JWT_TOKEN")
          # Parámetros editables
          video_path = os.environ.get("CUSTOMER_VIDEO_PATH")
          duration = 4
          # Llamar a la función para obtener el último frame
          last_frame_url = obtener_ultimo_frame(token, video_path, duration)
          # Mostrar el resultado
          if last_frame_url:
              print("🎉 Último frame obtenido con éxito!")
              print("URL del último frame:", last_frame_url)
          else:
              print("❌ No se pudo obtener el último frame.")

    except Exception as e:
        print(f"\n🚨 Error: {str(e)}")
        if hasattr(e, 'response') and e.response:
            print(f"📄 Respuesta servidor: {e.response.text[:300]}...")

