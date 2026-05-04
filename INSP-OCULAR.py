import streamlit as st
import json
from datetime import datetime
from streamlit_drawable_canvas import st_canvas
from fpdf import FPDF
from io import BytesIO
from PIL import Image
import numpy as np

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="S.I.V. Bloque 6 - Inspección y Cámaras", layout="wide")

# --- ESTILOS CSS PARA VISTA PREVIA ---
st.markdown("""
    <style>
    .acta-previa {
        background-color: white;
        color: black;
        padding: 40px;
        border: 1px solid #000;
        font-family: 'Arial', sans-serif;
        line-height: 1.5;
    }
    .titulo-pdf { text-align: center; font-weight: bold; text-decoration: underline; font-size: 18px; margin-bottom: 20px; }
    .firma-img { border-bottom: 1px solid black; width: 200px; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER Y AUTORÍA ---
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Escudo_de_la_Provincia_de_Santa_Fe.svg/1200px-Escudo_de_la_Provincia_de_Santa_Fe.svg.png", width=100)
st.sidebar.title("S.I.V. Bloque 6")
st.sidebar.write("**Autoría:** Sub Comisario CASTAÑEDA Juan")

# --- BLOQUE 1: DATOS DEL ACTANTE ---
st.header("👤 Identificación del Oficial Actante")
with st.container():
    c1, c2, c3 = st.columns(3)
    with c1: grade = st.selectbox("Grado:", ["Sub Comisario", "Principal", "Inspector", "Sub Inspector", "Oficial"])
    with c2: name_actante = st.text_input("Apellido y Nombre:", "CASTAÑEDA Juan")
    with c3: legajo = st.text_input("Legajo / NI:", "123.456")

# --- BLOQUE 2: DATOS DE LA CAUSA ---
st.header("📝 Datos de la Causa")
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        causa = st.text_input("Causa / Sumario N°:", "775/26")
        lugar = st.text_input("Lugar del Hecho:", "Mendoza y Martín Rodríguez")
    with col2:
        hecho = st.text_input("Carátula:", "ROBO CALIFICADO")
        fecha = st.date_input("Fecha del Procedimiento:")

# --- BLOQUE 3: INSPECCIÓN (IA) ---
st.header("🔍 Resultado de Inspección Técnica")
resultado_ia = st.text_area("Pegue aquí el informe descriptivo de la IA:", height=150)

# --- BLOQUE 4: CÁMARAS Y FIRMA DEL CIVIL ---
st.header("📹 Relevamiento de Cámaras y Compromiso")
hay_camaras = st.checkbox("¿Se detectaron cámaras de seguridad en el perímetro?")

datos_civil = {}
firma_image = None

if hay_camaras:
    with st.expander("Detalles del Responsable y Firma", expanded=True):
        cx1, cx2 = st.columns(2)
        with cx1:
            datos_civil['nombre'] = st.text_input("Nombre y Apellido (Civil):")
            datos_civil['dni'] = st.text_input("DNI:")
            datos_civil['vinculo'] = st.selectbox("Vínculo con el lugar:", ["Propietario", "Empleado", "Inquilino", "Otro"])
        with cx2:
            datos_civil['celular'] = st.text_input("Celular de contacto:")
            datos_civil['email'] = st.text_input("Correo Electrónico:")
            estado_camara = st.selectbox("Situación del Registro:", [
                "ENTREGA VOLUNTARIA: Soporte preservado para PDI.",
                "NEGATIVA / ORDEN JUDICIAL: Requiere orden de secuestro.",
                "MANIFESTACIÓN TÉCNICA: No graba o está dañado.",
                "SOLICITUD DE PERITOS: Desconoce manejo técnico.",
                "RE-FILMACIÓN DE URGENCIA: Captación digital por riesgo de pérdida."
            ])
            datos_civil['estado'] = estado_camara

        st.warning("🖋️ **FIRMA DEL RESPONSABLE:** El civil debe firmar en el recuadro de abajo (Táctil/Mouse)")
        canvas_result = st_canvas(
            fill_color="rgba(255, 255, 255, 0)", 
            stroke_width=3,
            stroke_color="#000000",
            background_color="#ffffff",
            height=150,
            width=400,
            key="canvas_firma"
        )
        if canvas_result.image_data is not None:
            firma_image = canvas_result.image_data

# --- FUNCIONES DE EXPORTACIÓN ---

def generar_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "POLICÍA DE LA PROVINCIA DE SANTA FE", ln=True, align="C")
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 5, "UNIDAD REGIONAL II - ROSARIO | S.I.V. SISTEMA DE VALIDACIÓN", ln=True, align="C")
    pdf.ln(10)
    
    pdf.set_font("Arial", "BU", 12)
    pdf.cell(0, 10, "ACTA DE INSPECCIÓN OCULAR", ln=True, align="C")
    pdf.ln(5)
    
    pdf.set_font("Arial", "B", 10)
    pdf.cell(0, 8, f"CAUSA: {causa} | FECHA: {fecha.strftime('%d/%m/%Y')}", ln=True)
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(0, 8, f"LUGAR: {lugar}\nHECHO: {hecho}\nACTANTE: {grade} {name_actante} (Legajo: {legajo})")
    pdf.ln(5)
    
    pdf.set_font("Arial", "B", 10)
    pdf.cell(0, 8, "1. INFORME TÉCNICO DE INSPECCIÓN:", ln=True)
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(0, 6, resultado_ia)
    pdf.ln(5)
    
    if hay_camaras:
        pdf.set_font("Arial", "B", 10)
        pdf.cell(0, 8, "2. RELEVAMIENTO DE CÁMARAS Y COMPROMISO DE RESGUARDO:", ln=True)
        pdf.set_font("Arial", "", 10)
        texto_cam = (f"Se identifica como responsable al Sr./Sra. {datos_civil['nombre']}, DNI {datos_civil['dni']}, "
                     f"en carácter de {datos_civil['vinculo']}, contacto {datos_civil['celular']} y email {datos_civil['email']}. "
                     f"Situación del registro: {datos_civil['estado']}. El responsable se compromete al resguardo de las imágenes.")
        pdf.multi_cell(0, 6, texto_cam)
        
        if firma_image is not None:
            img = Image.fromarray(firma_image.astype('uint8'), 'RGBA')
            pdf.image(img, x=10, y=pdf.get_y()+5, w=60)
            pdf.ln(25)
            pdf.cell(0, 5, f"Firma Responsable Cámara: {datos_civil['nombre']}", ln=True)

    pdf.ln(20)
    pdf.cell(0, 5, "__________________________", ln=True, align="R")
    pdf.cell(0, 5, f"Firma {grade} {name_actante}", ln=True, align="R")
    
    return pdf.output()

# --- PROCESO FINAL ---
st.divider()
if st.button("🏁 PROCESAR Y VALIDAR BLOQUE 6"):
    # VISTA PREVIA HTML
    st.markdown(f"""
    <div class="acta-previa">
        <div class="titulo-pdf">ACTA DE INSPECCIÓN OCULAR</div>
        <p><b>CAUSA N°:</b> {causa} | <b>FECHA:</b> {fecha}</p>
        <p><b>ACTANTE:</b> {grade} {name_actante} (Leg. {legajo})</p>
        <hr>
        <p><b>INFORME:</b><br>{resultado_ia}</p>
    </div>
    """, unsafe_allow_html=True)

    # BOTONES DE DESCARGA (OBLIGATORIOS)
    st.subheader("⬇️ Descargas Oficiales")
    c_pdf, c_json = st.columns(2)
    
    # PDF
    pdf_bytes = generar_pdf()
    c_pdf.download_button(
        label="📄 Descargar Acta PDF",
        data=pdf_bytes,
        file_name=f"Acta_B6_{causa}.pdf",
        mime="application/pdf"
    )
    
    # JSON
    full_data = {
        "actante": {"grado": grade, "nombre": name_actante, "legajo": legajo},
        "causa": {"numero": causa, "hecho": hecho, "lugar": lugar},
        "inspeccion": resultado_ia,
        "camaras": datos_civil if hay_camaras else "N/A"
    }
    c_json.download_button(
        label="💾 Exportar JSON (S.I.V. Base)",
        data=json.dumps(full_data, indent=4),
        file_name=f"Data_B6_{causa}.json",
        mime="application/json"
    )

st.info("💡 Nota: El croquis se realizará en un bloque independiente para garantizar máxima precisión planimétrica.")
