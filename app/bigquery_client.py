# Cliente oficial de Google BigQuery
from google.cloud import bigquery

# Inicializa el cliente usando credenciales del entorno (Cloud Run)
client = bigquery.Client()

# ID completo de la tabla en BigQuery:
# proyecto.dataset.tabla
TABLE_ID = "fif-platform-test-rod-espinoza.ventas_ds.ventas_mensuales"


def insertar_bigquery(data):
    try:
        # Log para debugging (ver qué se está enviando)
        print("📤 Insertando en BigQuery:", data)

        # Inserta el registro en formato JSON
        # Se envía como lista porque la API permite múltiples filas
        errors = client.insert_rows_json(TABLE_ID, [data])

        # Si hay errores, los imprime
        if errors:
            print("❌ Error insertando:", errors)
        else:
            # Inserción exitosa
            print("✅ Insert exitoso")

    except Exception as e:
        # Error general (credenciales, conexión, etc.)
        print("🔥 Error BigQuery:", str(e))

        # Relanza el error para que lo capture main.py
        raise