from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from pydantic import BaseModel
import io

app = FastAPI()

env = Environment(loader=FileSystemLoader("plantillas/templates"))

class Historial(BaseModel):
    paciente: str
    diagnostico: str
    tratamiento: str
    observaciones: str


@app.post("/generar-pdf")
def generar_pdf(data: Historial):

    html = env.get_template("historial.html").render(
        paciente=data.paciente,
        diagnostico=data.diagnostico,
        tratamiento=data.tratamiento,
        observaciones=data.observaciones
    )

    pdf = HTML(string=html).write_pdf()

    return StreamingResponse(
        io.BytesIO(pdf),
        media_type="application/pdf",
        headers = {"Content-Disposition": "attachment; filename=historial.pdf"}
    )