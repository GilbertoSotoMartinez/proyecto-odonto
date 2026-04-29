from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles # para el manejo de imagenes
from fastapi.responses import HTMLResponse, StreamingResponse
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from pydantic import BaseModel
import psycopg2
import json
import io
import os

print("CWD:", os.getcwd())

app = FastAPI()

# templates
env = Environment(loader=FileSystemLoader("plantillas/templates"))
# manejo de archivos estaticos
app.mount("/static", StaticFiles(directory="plantillas/templates/static"), name="static")

# Clase historial general
class HistorialGeneral(BaseModel):
    paciente: str
    diagnostico: str
    tratamiento: str
    observaciones: str
    fecha: str

# DB
conn = psycopg2.connect(
    dbname="db0",
    user="postgres",
    password="frijolito23",
    host="localhost",
    port="5432"
)
cur = conn.cursor()


# Mostrar formulario
@app.get("/", response_class=HTMLResponse)
def formulario():
    return env.get_template("formulario.html").render()

# Respuesta para ley federal

@app.get("/leyfederal", response_class=HTMLResponse)
def ley():
    return env.get_template("leyfederal.html").render()

@app.get("/contacto", response_class=HTMLResponse)
def contacto():
    return env.get_template("contacto.html").render()

# Mostrar formulario de historial general
@app.get("/historial-general", response_class=HTMLResponse)
def mostrar_historial_general():
    return env.get_template("historial_form.html").render()

@app.post("/generar-historial-general")
def generar_pdf(data: HistorialGeneral):
    from datetime import datetime
    fecha_actual = datetime.now().strftime("%Y-%m-%d")

    html = env.get_template("historial.html").render(
        paciente=data.paciente,
        diagnostico=data.diagnostico,
        tratamiento=data.tratamiento,
        observaciones=data.observaciones,
        fecha=fecha_actual
    )

    pdf = HTML(string=html).write_pdf()

    return StreamingResponse(
        io.BytesIO(pdf),
        media_type="application/pdf",
        headers = {"Content-Disposition": "attachment; filename=historial.pdf"}
    )
'''
@app.post("/historial-general")

def historial(data: dict):

    # buscar paciente
    cur.execute("SELECT id_paciente FROM pacientes WHERE curp=%s", (data["curp"],))
    res = cur.fetchone()

    if not res:
        return {"error": "Paciente no encontrado"}

    id_paciente = res[0]

    # guardar historial
    cur.execute("""
        INSERT INTO historiales_clinicos (id_paciente, tipo_historial, datos_json)
        VALUES (%s, %s, %s)
    """, (
        id_paciente,
        "general",
        json.dumps(data)
    ))
    conn.commit()

    # generar HTML
    html = env.get_template("historial.html").render(**data)

    # generar PDF
    pdf = HTML(string=html).write_pdf()

    return StreamingResponse(
        io.BytesIO(pdf),
        media_type="application/pdf",
        headers={"Content-Disposition": "inline; filename=historial.pdf"}
    )
'''