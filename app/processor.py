def procesar_venta(data):
    try:
        # Se construye un nuevo diccionario limpio y estructurado
        data_procesada = {

            # Obtiene el producto
            # - Si no existe, usa string vacío ""
            # - strip() elimina espacios al inicio y final
            "producto": data.get("producto", "").strip(),

            # Obtiene la región
            # - Limpia espacios
            "region": data.get("region", "").strip(),

            # Obtiene el mes (ej: "Abril 2026")
            # - Se mantiene como string
            "mes": data.get("mes", "").strip(),

            # Convierte ventas_mensuales a entero
            # - Si no viene el dato, usa 0 por defecto
            # - Esto asegura consistencia para BigQuery (INT64)
            "ventas_mensuales": int(data.get("ventas_mensuales", 0))
        }

        # Retorna el objeto listo para insertar en BigQuery
        return data_procesada

    except Exception as e:
        # Log de error si algo falla (ej: conversión a int)
        print("❌ Error procesando venta:", str(e))

        # Relanza la excepción para que la capture el main.py
        raise