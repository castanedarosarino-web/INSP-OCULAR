import streamlit as st
import json
from datetime import datetime
from streamlit_drawable_canvas import st_canvas
from fpdf import FPDF
from io import BytesIO
from PIL import Image

st.set_page_config(page_title="S.I.V. Bloque 6 - Inspección y Cámaras", layout="wide")

st.markdown("""
    <style>
    .acta-previa { background-color: white; color: black; padding: 40px; border: 1px solid #000; font-family: 'Arial', sans-serif; line-height: 1.5; }
    .titulo-pdf { text-align: center; font-weight: bold; text-decoration: underline; font-size: 18px; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.sidebar.title("S.I.V. Bloque 6")
st.sidebar.write("**Autoría:** Sub Comisario CASTAÑEDA Juan")

st.header("👤 Identificación del Oficial Actante")
c1, c2, c3 = st.columns(3)
with c1: grade = st.selectbox("Grado:", ["Sub Comisario", "Principal", "Inspector", "Sub Inspector", "Oficial"])
with c2: name_actante = st.text_input("Apellido y Nombre:", "CASTAÑEDA Juan")
with c3: legajo = st.text_input("Legajo / NI:", "123.456")

st.header("📝 Datos de la Causa")
col1, col2 = st.columns(2)
with col1:
    causa = st.text_input("Causa / Sumario N°:", "775/26")
    lugar = st.text_input("Lugar del Hecho:", "Mendoza y Martín Rodríguez")
with col2:
    hecho = st.text_input("Carátula:", "ROBO CALIFICADO")
    fecha = st.date_input("Fecha del Procedimiento:")

st.header("🔍 Resultado de Inspección Técnica")
resultado_ia = st.text_area("Pegue aquí el informe descriptivo de la IA:", height=150)

st.header("🛡️ Preservación y Perímetro")
perimetro = st.radio("¿Se procedió al encintado perimetral?", ["SÍ", "NO"], horizontal=True)

st.header("📹 Relevamiento de Cámaras")
hay_camaras = st.checkbox("¿Se detectaron cámaras de seguridad?")

datos_civil = {}
firma_b64 = None

if hay_camaras:
    cx1, cx2 = st.columns(2)
    with cx1:
        datos_civil['nombre'] = st.text_input("Nombre y Apellido (Civil):")
        datos_civil['dni'] = st.text_input("DNI:")
        datos_civil['vinculo'] = st.selectbox("Vínculo:", ["Propietario", "Empleado", "Inquilino", "Otro"])
    with cx2:
        datos_civil['celular'] = st.text_input("Celular:")
        datos_civil['email'] = st.text_input("E-mail:")
        datos_civil['estado'] = st.selectbox("Situación del Registro:", [
            "ENTREGA VOLUNTARIA: Soporte preservado para PDI.",
            "NEGATIVA / ORDEN JUDICIAL: Requiere orden de secuestro.",
            "MANIFESTACIÓN TÉCNICA: No graba o está dañado.",
            "SOLICITUD DE PERITOS: Desconoce manejo técnico.",
            "RE-FILMACIÓN DE URGENCIA: Captación digital por riesgo de pérdida."
        ])
    st.warning("🖋️ FIRMA DEL RESPONSABLE (Táctil)")
    canvas_result = st_canvas(fill_color="rgba(255, 255, 255, 0)", stroke_width=3, stroke_color="#000", background_color="#fff", height=150, width=400, key="canvas_firma")
    if canvas_result.image_data is not None:
        firma_b64 = canvas_result.image_data

def generar_pdf_bytes():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "POLICIA DE LA PROVINCIA DE SANTA FE", ln=True, align="C")
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "ACTA DE INSPECCION OCULAR", ln=True, align="C")
    pdf.ln(5)
    pdf.set_font("Arial", "B", 10)
    pdf.cell(0, 8, f"CAUSA: {causa} | FECHA: {fecha.strftime('%d/%m/%Y')}", ln=True)
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(0, 6, f"LUGAR: {lugar}\nHECHO: {hecho}\nACTANTE: {grade} {name_actante} (Legajo: {legajo})")
    pdf.ln(5)
    
    # 1. INSPECCIÓN
    pdf.set_font("Arial", "B", 10)
    pdf.cell(0, 8, "1. INFORME TECNICO DE INSPECCION:", ln=True)
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(0, 6, resultado_ia)
    
    # 2. PERÍMETRO
    pdf.ln(3)
    pdf.set_font("Arial", "B", 10)
    pdf.cell(0, 8, "2. PRESERVACION DEL LUGAR DEL HECHO:", ln=True)
    pdf.set_font("Arial", "", 10)
    txt_peri = "Se procedió a la correcta delimitación del área mediante encintado perimetral." if perimetro == "SÍ" else "No se realizó encintado perimetral por razones de urgencia operativa."
    pdf.multi_cell(0, 6, txt_peri)

    # 3. CÁMARAS
    if hay_camaras:
        pdf.ln(3)
        pdf.set_font("Arial", "B", 10)
        pdf.cell(0, 8, "3. RELEVAMIENTO DE CAMARAS Y COMPROMISO DE RESGUARDO:", ln=True)
        pdf.set_font("Arial", "", 10)
        texto = f"Responsable: {datos_civil['nombre']}, DNI: {datos_civil['dni']}, Contacto: {datos_civil['celular']}. Situacion: {datos_civil['estado']}."
        pdf.multi_cell(0, 6, texto)
        if firma_b64 is not None:
            img_firma = Image.fromarray(firma_b64.astype('uint8'), 'RGBA')
            img_buffer = BytesIO()
            img_firma.save(img_buffer, format="PNG")
            img_buffer.seek(0)
            pdf.image(img_buffer, x=10, y=pdf.get_y()+5, w=50)
            pdf.ln(25)

    pdf.ln(20)
    pdf.cell(0, 10, "__________________________", ln=True, align="R")
    pdf.cell(0, 5, f"Firma {grade} {name_actante}", ln=True, align="R")
    return bytes(pdf.output())

st.divider()
if st.button("🏁 VALIDAR Y GENERAR"):
    if not resultado_ia:
        st.error("Falta el informe de inspección.")
    else:
        st.markdown(f'<div class="acta-previa"><div class="titulo-pdf">ACTA DE INSPECCIÓN OCULAR</div><p><b>CAUSA:</b> {causa} | <b>ACTANTE:</b> {grade} {name_actante}</p><p>{resultado_ia}</p></div>', unsafe_allow_html=True)
        st.subheader("⬇️ DESCARGAS OFICIALES")
        c_pdf, c_json = st.columns(2)
        try:
            pdf_data = generar_pdf_bytes()
            c_pdf.download_button(label="📄 Descargar Acta PDF", data=pdf_data, file_name=f"Acta_{causa}.pdf", mime="application/pdf")
            json_data = json.dumps({"oficial": name_actante, "causa": causa, "perimetro": perimetro, "inspeccion": resultado_ia, "camaras": datos_civil if hay_camaras else "N/A"}, indent=4)
            c_json.download_button(label="💾 Descargar JSON", data=json_data, file_name=f"Data_{causa}.json", mime="application/json")
        except Exception as e:
            st.error(f"Error: {e}")
