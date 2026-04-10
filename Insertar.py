import csv
import json
import base64
import requests

# URL de tu servicio Cloud Run
URL = "https://ventas-service-489749636379.us-central1.run.app/"

# Archivo CSV
CSV_FILE = "ventas.csv"


def enviar_fila(row):
    try:
        # Construir JSON
        data = {
            "producto": row["producto"],
            "region": row["region"],
            "mes": row["mes"],
            "ventas_mensuales": int(row["ventas_mensuales"])
        }

        json_str = json.dumps(data, ensure_ascii=False)

        # Convertir a base64
        base64_data = base64.b64encode(json_str.encode("utf-8")).decode("utf-8")

        # Formato Pub/Sub
        payload = {
            "message": {
                "data": base64_data
            }
        }

        # Enviar request
        response = requests.post(URL, json=payload)

        if response.status_code == 204:
            print(f"✅ Insertado: {data}")
        else:
            print(f"❌ Error {response.status_code}: {response.text}")

    except Exception as e:
        print(f"🔥 Error procesando fila {row}: {str(e)}")


def main():
    with open(CSV_FILE, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            enviar_fila(row)


if __name__ == "__main__":
    main()