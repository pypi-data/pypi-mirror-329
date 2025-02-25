#@title verificar
import requests
import re
import random
import string
import uuid
import time
import os
def generar_contrasena(longitud=10):
    if longitud < 10:
        raise ValueError("La contraseña debe tener al menos 10 caracteres.")

    letras_minusculas = string.ascii_lowercase
    letras_mayusculas = string.ascii_uppercase
    numeros = string.digits
    caracteres = letras_minusculas + letras_mayusculas + numeros

    # Garantizar que la contraseña tenga al menos una mayúscula y un número
    contrase = random.choice(letras_mayusculas) + random.choice(numeros)

    # Completar el resto de la contraseña con caracteres aleatorios
    contrase += ''.join(random.choices(caracteres, k=longitud-2))

    # Mezclar la contraseña para que no siempre empiece con mayúscula y número
    contrase = ''.join(random.sample(contrase, len(contrase)))

    return contrase

def iniciar_sesion(username, password):
    url = "https://app-api.pixverse.ai/creative_platform/login"

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
        "Content-Type": "application/json",
        "Origin": "https://app.pixverse.ai",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://app.pixverse.ai/",
        "Accept-Encoding": "gzip, deflate"
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

def registrar_usuario(mail, username, code, password):
    """
    Registra un usuario en PixVerse y retorna el Token si la solicitud es exitosa.

    :param mail: Correo electrónico del usuario.
    :param username: Nombre de usuario.
    :param code: Código de verificación.
    :param password: Contraseña del usuario.
    :return: Token si la solicitud es exitosa, None en caso contrario.
    """
    # URL del endpoint
    url = "https://app-api.pixverse.ai/app/v1/account/register"

    # Headers de la solicitud
    headers = {
        "user-agent": "PixVerse 1.5.7 /(Android 9;2304FPN6DG)",
        "ai-trace-id": str(uuid.uuid4()),  # Genera un nuevo Ai-Trace-Id dinámico
        "accept-language": "en-US",
        "accept-encoding": "gzip",
        "content-length": "100",
        "x-device-id": "4fa8c75370c89711155735e73ec78d8eab5a3272",
        "host": "app-api.pixverse.ai",
        "content-type": "application/json",
        "x-app-version": "1.5.7",
        "x-platform": "Android",
        "token": ""  # Aquí deberías agregar el token si lo tienes
    }

    # Cuerpo de la solicitud (payload) con los datos ingresados por el usuario
    payload = {
        "Mail": mail,
        "Username": username,
        "Code": code,
        "Password": password
    }

    # Realizar la solicitud POST
    response = requests.post(url, headers=headers, json=payload)

    # Verificar si la solicitud fue exitosa
    if response.status_code == 200:
        response_data = response.json()
        if response_data.get("ErrMsg") == "Success":
            print("✅ La solicitud fue exitosa.")
            # Extraer el Token de la respuesta
            token = response_data["Resp"]["Result"]["Token"]
            #print("Token generado:", token)
            return token  # Retornar el Token
        else:
            print("❌ La solicitud no fue exitosa. Mensaje de error:", response_data.get("ErrMsg"))
            return None  # Retornar None si no es exitosa
    else:
        print("❌ Error en la solicitud. Código de estado:", response.status_code)
        return None  # Retornar None si hay un error en la solicitud



def solicitar_verificacion(mail, username, password):
    # Solicitar datos al usuario

    # URL del endpoint
    url = "https://app-api.pixverse.ai/app/v1/account/getVerificationCode"

    # Headers de la solicitud
    headers = {
        "user-agent": "PixVerse 1.5.7 /(Android 9;2304FPN6DG)",
        "ai-trace-id": str(uuid.uuid4()),  # Genera un nuevo Ai-Trace-Id dinámico
        "accept-language": "en-US",
        "accept-encoding": "gzip",
        "content-length": "84",
        "x-device-id": "4fa8c75370c89711155735e73ec78d8eab5a3272",
        "host": "app-api.pixverse.ai",
        "content-type": "application/json",
        "x-app-version": "1.5.7",
        "x-platform": "Android",
        "token": ""  # Aquí deberías agregar el token si lo tienes
    }

    # Cuerpo de la solicitud (payload) con los datos ingresados por el usuario
    payload = {
        "Mail": mail,
        "Username": username,
        "Password": password
    }

    # Realizar la solicitud POST
    response = requests.post(url, headers=headers, json=payload)
    #print(response.text)
    #print(response.status_code)

    # Verificar si la solicitud fue exitosa
    if response.status_code == 200:
        response_data = response.json()
        if response_data.get("ErrMsg") == "Success":
            #print("✅ La solicitud fue exitosa.")
            #print("Respuesta completa:", response_data)
            return "✅ La solicitud fue exitosa."
        else:
            #print("❌ La solicitud no fue exitosa. Mensaje de error:", response_data.get("ErrMsg"))
            return "This username is already taken."
    else:
        #print("❌ Error en la solicitud. Código de estado:", c)
        return "This username is already taken."


def create_email(min_name_length=10, max_name_length=10):
    url = "https://api.internal.temp-mail.io/api/v3/email/new"
    headers = {
        "Host": "api.internal.temp-mail.io",
        "Connection": "keep-alive",
        "Application-Name": "web",
        "sec-ch-ua-platform": "\"Windows\"",
        "Application-Version": "3.0.0",
        "sec-ch-ua": "\"Not A(Brand\";v=\"8\", \"Chromium\";v=\"132\", \"Google Chrome\";v=\"132\"",
        "sec-ch-ua-mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "Origin": "https://temp-mail.io",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://temp-mail.io/",
        "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate"
    }
    data = {
        "min_name_length": min_name_length,
        "max_name_length": max_name_length
    }

    # Hacer la solicitud
    response = requests.post(url, json=data, headers=headers)

    # Extraer el email de la respuesta JSON
    if response.status_code == 200:
        email = response.json().get("email")
        return email
    else:
        return None


def get_verification_code(email):
    url = f"https://api.internal.temp-mail.io/api/v3/email/{email}/messages"
    headers = {
        "Host": "api.internal.temp-mail.io",
        "Connection": "keep-alive",
        "Application-Name": "web",
        "sec-ch-ua-platform": "\"Windows\"",
        "Application-Version": "3.0.0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "sec-ch-ua": "\"Not A(Brand\";v=\"8\", \"Chromium\";v=\"132\", \"Google Chrome\";v=\"132\"",
        "sec-ch-ua-mobile": "?0",
        "Origin": "https://temp-mail.io",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://temp-mail.io/",
        "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate"
    }

    # Hacer la solicitud GET
    response = requests.get(url, headers=headers)
    #print("Correo código:", response.text)  # Para depuración

    if response.status_code == 200:
        messages = response.json()
        if messages:
            # Extraer el cuerpo del texto del primer mensaje
            body_text = messages[0].get("body_text", "")

            # Usar una expresión regular para extraer el código de verificación
            code_pattern = r"Your PixVerse verification code is:\s*(\d{6})"
            match = re.search(code_pattern, body_text)

            if match:
                code = match.group(1)  # Extraer el código
                return code
            else:
                print("❌ No se encontró un código de verificación en el correo.")
                return None
        else:
            print("❌ No hay mensajes en el correo.")
            return None
    else:
        print(f"❌ Error en la solicitud. Código de estado: {response.status_code}")
        return None

def extract_code_from_text(body_text):
    # Buscar un patrón de 6 dígitos en el texto
    match = re.search(r'\b\d{6}\b', body_text)
    if match:
        return match.group(0)
    return None

def check_code_with_retries(email, retries=6, delay=10):
    for attempt in range(retries):
        print(f"Intento {attempt + 1} de {retries}...")
        code = get_verification_code(email)
        if code:
            print(f"Código de verificación: ******")
            return code
        #print("Código no encontrado. Esperando 10 segundos antes de reintentar...")
        time.sleep(delay)
    print("Se alcanzó el máximo de intentos sin éxito.")
    return None


def guardar_credenciales(username, password):
    """
    Guarda las credenciales en un archivo de texto sin sobrescribir las anteriores.
    """
    ruta_archivo = "/content/cuenta.txt"
    with open(ruta_archivo, "a") as archivo:
        archivo.write(f"{username}:{password}\n")
    print(f"📂 Credenciales guardadas en {ruta_archivo}")

# Ejemplo de uso
def register():
    """
    Función generadora que registra un usuario y envía actualizaciones en tiempo real.
    """
    email = create_email()
    time.sleep(1)
    username = email.split("@")[0]
    password = generar_contrasena(10)

    # Enviar el email y username generados
    #print(f"Email: {email}\nUsername: {username}\nPassword: {password}\n")

    # Solicitar verificación
    text_status = solicitar_verificacion(email, username, password)
    if text_status == "This username is already taken.":
        print("❌ El nombre de usuario ya está en uso. Generando uno nuevo...\n")
        register()  # Llamada recursiva para generar un nuevo usuario
    else:
        print("✅ Solicitud de verificación enviada.\n")

    # Esperar y obtener el código de verificación
    print("⏳ Esperando el código de verificación...\n")
    verification_code = check_code_with_retries(email)
    if verification_code:
        print(f"✅ Código de verificación recibido: ******\n")
    else:
        print("❌ No se pudo obtener el código de verificación.\n")
        return

    # Registrar el usuario
    print("⏳ Registrando usuario...\n")
    jwt_token = registrar_usuario(email, username, verification_code, password)
    if jwt_token:
        print("✅ Usuario registrado exitosamente.\n")
        print("🔥 Iniciando sesión...\n")
        token = iniciar_sesion(username, password)
        if token:
            print("🔐 Sesión iniciada. Token obtenido: ***********\n")
            os.environ["JWT_TOKEN"] = token

            # Guardar credenciales en el archivo
            guardar_credenciales(email, password)

        else:
            print("❌ No se pudo iniciar sesión.\n")
    else:
        print("❌ No se pudo registrar el usuario.\n")
