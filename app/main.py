# Importa Flask para levantar el servicio HTTP 
# Roderick Espinoza
from flask import Flask, request

# Librerías para decodificar el mensaje y trabajar JSON
import base64
import json
import re

# Importa funciones propias del proyecto
from processor import procesar_venta
from bigquery_client import insertar_bigquery

# Inicializa la aplicación Flask
app = Flask(__name__)


def fix_json(payload_str):
    """
    Corrige JSON mal formado:
    Ejemplo:
    {producto:Mouse} -> {"producto":"Mouse"}

    Esto pasa porque a veces Pub/Sub o pruebas manuales
    envían JSON sin comillas válidas.
    """
    try:
        # Elimina caracteres de escape innecesarios
        payload_str = payload_str.replace("\\", "")

        # Agrega comillas a las claves
        # producto:Mouse -> "producto":Mouse
        payload_str = re.sub(r'([{,])\s*([a-zA-Z_]+)\s*:', r'\1"\2":', payload_str)

        # Agrega comillas a los valores
        # :Mouse -> :"Mouse"
        payload_str = re.sub(r':\s*([^",}{]+)', r':"\1"', payload_str)

        # Convierte el string corregido a JSON válido
        return json.loads(payload_str)

    except Exception as e:
        print("❌ Error corrigiendo JSON:", str(e))
        raise


# Endpoint principal (Cloud Run recibe POST aquí)
@app.route("/", methods=["POST"])
def receive_message():
    try:
        # Obtiene el cuerpo completo de la request
        envelope = request.get_json()

        # Validación básica
        if not envelope:
            print("❌ No envelope")
            return ("No message", 400)

        # Extrae estructura de Pub/Sub
        pubsub_message = envelope.get("message")

        if not pubsub_message:
            print("❌ No pubsub_message:", envelope)
            return ("Invalid Pub/Sub message", 400)

        # Obtiene el campo data (viene en base64)
        data = pubsub_message.get("data")

        if not data:
            print("❌ No data field:", pubsub_message)
            return ("No data in message", 400)

        # Decodifica base64 → string JSON
        decoded_data = base64.b64decode(data).decode("utf-8")

        print("📩 RAW decoded:", decoded_data)

        # Intenta parsear JSON directamente
        try:
            venta = json.loads(decoded_data)

        except:
            # Si falla, intenta corregir JSON mal formado
            print("⚠️ JSON mal formado, intentando corregir...")
            venta = fix_json(decoded_data)

        print("✅ JSON final:", venta)

        # Procesa/normaliza los datos (limpieza, tipos, etc.)
        venta_procesada = procesar_venta(venta)

        # Inserta en BigQuery
        insertar_bigquery(venta_procesada)

        # Respuesta exitosa (sin contenido)
        return ("", 204)

    except Exception as e:
        # Manejo global de errores
        print("🔥 ERROR GENERAL:", str(e))
        return ("Internal error", 500)


# Permite ejecutar localmente (no se usa en Cloud Run)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)