#@title upload personaje
import requests
import uuid
import os
import mimetypes
from datetime import datetime
import base64
import hmac
import hashlib
import random
import string

# Configuración global
BASE_API_URL = "https://app-api.pixverse.ai"
OSS_UPLOAD_URL = "https://pixverse-fe-upload.oss-accelerate.aliyuncs.com"

# ------------------------- FUNCIONES PRINCIPALES ------------------------- #
# ------------------------- FUNCIONES PRINCIPALES ------------------------- #
def generar_nombre_completo():
    """Genera un nombre completo triplicando el nombre y apellido, junto con un número aleatorio de 3 dígitos."""
    nombres = ["Juan", "Pedro", "Maria", "Ana", "Luis", "Sofia", "Diego", "Laura", "Javier", "Isabel",
               "Pablo", "Marta", "David", "Elena", "Sergio", "Irene", "Daniel", "Alicia", "Carlos", "Sandra",
               "Antonio", "Lucia", "Miguel", "Sara", "Jose", "Cristina", "Alberto", "Blanca", "Alejandro", "Marta",
               "Francisco", "Esther", "Roberto", "Silvia", "Manuel", "Patricia", "Marcos", "Victoria", "Fernando", "Rosa",
               # Nombres comunes de EE.UU.
               "James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph", "Charles", "Thomas",
               "Christopher", "Daniel", "Matthew", "Anthony", "Mark", "Donald", "Steven", "Paul", "Andrew", "Joshua",
               "Kenneth", "Kevin", "Brian", "George", "Edward", "Ronald", "Timothy", "Jason", "Jeffrey", "Ryan",
               "Jacob", "Gary", "Nicholas", "Eric", "Jonathan", "Stephen", "Larry", "Justin", "Scott", "Brandon",
               "Benjamin", "Samuel", "Frank", "Gregory", "Raymond", "Alexander", "Patrick", "Jack", "Dennis", "Jerry",
               "Tyler", "Aaron", "Henry", "Douglas", "Jose", "Peter", "Adam", "Zachary", "Nathan", "Walter", 
               "Kyle", "Harold", "Carl", "Arthur", "Gerald", "Roger", "Keith", "Jeremy", "Terry", "Lawrence",
               "Sean", "Christian", "Ethan", "Austin", "Joe", "Jordan", "Albert", "Jesse", "Willie", "Billy"]

    nombre = random.choice(nombres)

    nombre_completo = f"{nombre}"
    return nombre_completo

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

def subir_imagen_oss(image_path, upload_credentials):
    """Sube la imagen al servicio de almacenamiento OSS de Alibaba"""
    ak = upload_credentials['Ak']
    sk = upload_credentials['Sk']
    token = upload_credentials['Token']
    bucket_name = "pixverse-fe-upload"
    object_path = f"upload/{uuid.uuid4()}.png"
    mime_type = 'image/png'
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
        'Host': "pixverse-fe-upload.oss-accelerate.aliyuncs.com"
    }

    try:
        with open(image_path, 'rb') as f:
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
            'tamaño': os.path.getsize(image_path)
        }

    except Exception as e:
        print(f"\n🔍 Debug - String para firmar:\n{string_to_sign}")
        print(f"🔍 SK usado: {sk[:5]}...{sk[-5:]}")
        raise

def registrar_medios(media_info, headers):
    """Registra los medios subidos en el sistema"""
    url = f"{BASE_API_URL}/creative_platform/media/batch_upload_media"
    payload = {"images": [{
        "name": media_info['nombre'],
        "size": media_info['tamaño'],
        "path": media_info['ruta']
    }]}

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        json_data = response.json()

        if json_data['ErrCode'] != 0:
            raise ValueError(json_data['ErrMsg'])

        return json_data['Resp']['result'][0]['id']
    except Exception as e:
        raise RuntimeError(f"Fallo en registro: {str(e)}")

def validar_imagen(image_id, headers):
    """Realiza la validación de la imagen subida"""
    url = f"{BASE_API_URL}/creative_platform/media/character_check_media"
    try:
        response = requests.post(url, json={"img_id": image_id}, headers=headers)
        response.raise_for_status()
        return response.json()['ErrCode'] == 0
    except Exception as e:
        raise RuntimeError(f"Error en validación: {str(e)}")

def crear_asset(nombre_asset, image_id, headers):
    """Crea el asset final con la imagen validada"""
    url = f"{BASE_API_URL}/creative_platform/asset/create"
    payload = {
        "AssetName": nombre_asset,
        "AssetType": 1,
        "VideoStyle": "anime",
        "ImgIds": [image_id]
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        json_data = response.json()

        if json_data['ErrCode'] != 0:
            raise ValueError(json_data['ErrMsg'])

        return json_data['Resp']['AssetId']
    except Exception as e:
        raise RuntimeError(f"Error creando asset: {str(e)}")

# ------------------------- PROGRAMA PRINCIPAL ------------------------- #
def upload_pers(imagen_local):
    API_KEY = os.environ.get("JWT_TOKEN")
    headers = {
        'X-Platform': 'Web',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
        'Token': API_KEY # Reemplazar con tu token real
    }

    try:
        print("\n🖼️ Paso 1/5: Subiendo imagen...")

        print("\n🔐 Paso 2/5: Obteniendo token...")
        creds = obtener_token_subida(headers)

        print("\n☁️ Paso 3/5: Subiendo a OSS...")
        media_info = subir_imagen_oss(imagen_local, creds)
        print(f"✔️ Subido:https://media.pixverse.ai/{media_info['ruta']}")
        os.environ["CUSTOMER_IMG_PATH"] = str(media_info['ruta'])
        os.environ["CUSTOMER_IMG_URL"] = str(f"https://media.pixverse.ai/{media_info['ruta']}")

        print("\n📝 Paso 4/5: Registrando...")
        image_id = registrar_medios(media_info, headers)
        print(f"🆔 ID Imagen: *******")

        print("\n🔍 Paso 5/5: Validando...")
        if validar_imagen(image_id, headers):
            nombre = generar_nombre_completo()
            asset_id = crear_asset(nombre, image_id, headers)
            os.environ["ASSET_ID"] = str(asset_id)
            print(f"\n🎉 ¡Éxito! Asset ID: *********")
        else:
            print("❌ Validación fallida")

    except Exception as e:
        print(f"\n🚨 Error: {str(e)}")
        if hasattr(e, 'response') and e.response:
            print(f"📄 Respuesta servidor: {e.response.text[:300]}...")
