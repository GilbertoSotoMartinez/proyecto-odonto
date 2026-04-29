import json
import os

print("CWD:", os.getcwd())


def cargar_plantilla(tipo):
    ruta = f"plantillas/{tipo}.json"
    with open(ruta, "r", encoding="utf-8") as f:
        return json.load(f)


def llenar_formulario(plantilla):
    resultado = {}

    for campo, tipo in plantilla.items():
        valor = input(f"Ingrese {campo} ({tipo}): ")
        resultado[campo] = valor

    return resultado


def guardar_json(datos, nombre_archivo):
    ruta_salida = f"{nombre_archivo}.json"
    with open(ruta_salida, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)

    print(f"\n✔ Archivo guardado en: {ruta_salida}")


# 🚀 FLUJO COMPLETO
plantilla = cargar_plantilla("general")
datos = llenar_formulario(plantilla)
guardar_json(datos, "historial_1")