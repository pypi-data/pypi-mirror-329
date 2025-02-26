#@title verificar
import requests
import re
import random
import string
import uuid
import time
import os
from bs4 import BeautifulSoup


COMMON_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'es-ES,es;q=0.9',
    'Accept-Encoding': 'gzip, deflate'
}

def extraer_dominios(response_text):
    """Extrae dominios de un texto utilizando expresiones regulares."""
    dominios = re.findall(r'id="([^"]+\.[^"]+)"', response_text)
    return dominios

def extraer_codigo(html):
    soup = BeautifulSoup(html, "html.parser")

    # Buscar el código en un párrafo con estilo específico
    codigo_tag = soup.find("p", style="margin: 30px 0; font-size: 24px")
    if codigo_tag:
        return codigo_tag.text.strip()

    # Si el código no se encuentra en el estilo esperado, buscar con regex
    codigo_match = re.search(r"\b\d{6}\b", soup.get_text())
    if codigo_match:
        return codigo_match.group()

    return None  # Retorna None si no encuentra el código
    

def delete_temp_mail(username_email, dominios_dropdown, extracted_string):
    """Borra el correo temporal especificado."""
    EMAIL_FAKE_URL = 'https://email-fake.com/'
    url = f"{EMAIL_FAKE_URL}/del_mail.php"

    headers = {
        'Host': 'email-fake.com',
        'Connection': 'keep-alive',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'Accept': '*/*',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
        'Origin': 'https://email-fake.com',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Accept-Language': 'es-ES,es;q=0.9',
        'Cookie': f'embx=%5B%22{username_email}%40{dominios_dropdown}%22%2C',
    }

    data = f'delll={extracted_string}'

    response = requests.post(url, headers=headers, data=data)

    if "Message deleted successfully" in response.text:
        print("Temporary mail deleted...")
        return True
    else:
        print("Error deleting temporary email...")
        return False

def generar_contrasena():
    """Genera una contraseña aleatoria."""
    caracteres = string.ascii_letters + "0123456789" + "#$%&/()@_-*+[]"
    longitud = 10
    contraseña = ''.join(random.choice(caracteres) for _ in range(longitud))
    return contraseña

def enviar_formulario(url, datos):
    """Envía una solicitud POST a un formulario web."""
    response = requests.post(url, data=datos)
    return response

def obtener_sitio_web_aleatorio(response_text):
    """Obtiene un sitio web aleatorio de los dominios extraídos."""
    dominios = extraer_dominios(response_text)
    sitio_web_aleatorio = random.choice(dominios)
    return sitio_web_aleatorio

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

    apellidos = ["Garcia", "Rodriguez", "Gonzalez", "Fernandez", "Lopez", "Martinez", "Sanchez", "Perez", "Alonso", "Diaz",
                 "Martin", "Ruiz", "Hernandez", "Jimenez", "Torres", "Moreno", "Gomez", "Romero", "Alvarez", "Vazquez",
                 "Gil", "Lopez", "Ramirez", "Santos", "Castro", "Suarez", "Munoz", "Gomez", "Gonzalez", "Navarro",
                 "Dominguez", "Lopez", "Rodriguez", "Sanchez", "Perez", "Garcia", "Gonzalez", "Martinez", "Fernandez", "Lopez",
                 # Apellidos comunes de EE.UU.
                 "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez",
                 "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
                 "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson",
                 "Walker", "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores",
                 "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell", "Carter", "Roberts",
                 "Gomez", "Phillips", "Evans", "Turner", "Diaz", "Parker", "Cruz", "Edwards", "Collins", "Reyes",
                 "Stewart", "Morris", "Morales", "Murphy", "Cook", "Rogers", "Gutierrez", "Ortiz", "Morgan", "Cooper",
                 "Peterson", "Bailey", "Reed", "Kelly", "Howard", "Ward", "Cox", "Diaz", "Richardson", "Wood"]


    nombre = random.choice(nombres)
    apellido = random.choice(apellidos)
    numero = random.randint(100, 999)

    nombre_completo = f"{nombre}_{apellido}_{numero}"
    return nombre_completo

def get_verification_code(username_email, dominios_dropdown):
    """Obtiene el código de verificación del correo y el identificador."""
    EMAIL_FAKE_URL = 'https://email-fake.com/'
    url = f"{EMAIL_FAKE_URL}/"

    headers = {
        'Host': 'email-fake.com',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        **COMMON_HEADERS,
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': 'Windows',
        'Cookie': f'surl={dominios_dropdown}%2F{username_email}',
    }

    response = requests.get(url, headers=headers)

    #print(response.text)

    # Utiliza una expresión regular para encontrar el código de 6 dígitos
    verification_code = extraer_codigo(response.text)
    #verification_code_match = re.search(r'<strong>(\d{6})</strong>', response.text)

    # Utiliza una expresión regular para encontrar el identificador largo
    identifier_match = re.search(r'delll:\s*"([a-zA-Z0-9]+)"', response.text)

    # Extrae y retorna los valores si fueron encontrados
    if verification_code and identifier_match:
        #verification_code = verification_code_match.group(1)
        identifier = identifier_match.group(1)
        return verification_code, identifier
    else:
        return None, None


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
        "x-device-id": "4fa8c75370c89711155735e73ec78d8eab5a3288",
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
        "x-device-id": "4fa8c75370c89711155735e73ec78d8eab5a3288",
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


def extract_code_from_text(body_text):
    # Buscar un patrón de 6 dígitos en el texto
    match = re.search(r'\b\d{6}\b', body_text)
    if match:
        return match.group(0)
    return None

def check_code_with_retries(username_email, dominios_dropdown, retries=6, delay=10):
    for attempt in range(retries):
        print(f"Intento {attempt + 1} de {retries}...")
        code, identifier = get_verification_code(username_email, dominios_dropdown)
        if code:
            print(f"Código de verificación: {code}")
            delete_temp_mail(username_email, dominios_dropdown, identifier)
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
    password_segura = generar_contrasena()
    url = 'https://email-fake.com/'
    # Supongamos que el formulario en el sitio web tiene un campo llamado 'campo_correo'
    datos = {'campo_correo': 'ejemplo@dominio.com'}
    # Enviar la solicitud POST al formulario
    response = enviar_formulario(url, datos)
    # Obtener un sitio web aleatorio de los dominios extraídos
    sitio_domain = obtener_sitio_web_aleatorio(response.text)
    # Generar y mostrar un nombre completo
    nombre_completo = generar_nombre_completo()
    time.sleep(3)
    # Llamar a la función con valores personalizados
    correo = f'{nombre_completo}@{sitio_domain}'
    username = nombre_completo
    password = password_segura
    email = correo

    # Solicitar verificación
    text_status = solicitar_verificacion(email, username, password)
    if text_status == "This username is already taken.":
        print("❌ El nombre de usuario ya está en uso. Generando uno nuevo...\n")
        register()  # Llamada recursiva para generar un nuevo usuario
    else:
        print("✅ Solicitud de verificación enviada.\n")

    # Esperar y obtener el código de verificación
    print("⏳ Esperando el código de verificación...\n")
    verification_code = check_code_with_retries(nombre_completo, sitio_domain)
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
