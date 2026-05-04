import streamlit as st
import json
from datetime import datetime
from streamlit_drawable_canvas import st_canvas
from fpdf import FPDF
from io import BytesIO
from PIL import Image

st.set_page_config(page_title="S.I.V. Bloque 6 - Inspección y Registro", layout="wide")

# ESTILOS
st.markdown("""
    <style>
    .acta-previa { background-color: white; color: black; padding: 45px; border: 1px solid #000; font-family: 'Arial', sans-serif; }
    .titulo-pdf { text-align: center; font-weight: bold; text-decoration: underline; font-size: 18px; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.sidebar.title("S.I.V. Bloque 6")
st.sidebar.write("**Autoría:** Sub Comisario CASTAÑEDA Juan")

# --- BLOQUE 1: IDENTIFICACIÓN DEL PERSONAL ---
st.header("👤 Identificación del Personal Actuante")
c1, c2, c3 = st.columns(3)
with c1: grade = st.selectbox("Grado:", ["Sub Comisario", "Principal", "Inspector", "Sub Inspector", "Oficial"])
with c2: name_actuante = st.text_input("Apellido y Nombre:", "CASTAÑEDA Juan")
with c3: legajo = st.text_input("Legajo / NI:", "123.456")

# --- BLOQUE 2: REFERENCIA ---
st.header("📝 Referencia Administrativa")
col1, col2 = st.columns(2)
with col1:
    acta_nro = st.text_input("REFERENTE ACTA N° (Bloque 1):", "123/26")
    lugar = st.text_input("Lugar del Hecho:", "Mendoza y Martín Rodríguez")
with col2:
    hecho = st.text_input("Carátula:", "ROBO CALIFICADO")
    fecha = st.date_input("Fecha del Procedimiento:")

st.header("🔍 Inspección Técnica (Descripción IA)")
resultado_ia = st.text_area("Informe descriptivo consolidado:", height=150)

st.header("🛡️ Preservación del Lugar")
perimetro = st.radio("¿Se procedió al encintado perimetral?", ["SÍ", "NO"], horizontal=True)

# --- BLOQUE CAMARAS ---
st.header("📹 Relevamiento de Cámaras de Seguridad")
col_pub, col_priv = st.columns(2)
with col_pub: hay_publicas = st.checkbox("Cámaras Públicas / Domos (911)")
with col_priv: hay_privadas = st.checkbox("Cámaras Privadas / Particulares")

id_domos = ""
datos_civil = {}
firma_b64 = None

if hay_publicas:
    id_domos = st.text_input("Identificación de Domos/Cámaras Públicas (ID):", placeholder="Ej: Domo 452, Cámara 12...")

if hay_privadas:
    with st.expander("Datos del Responsable Privado y Firma", expanded=True):
        cx1, cx2 = st.columns(2)
        with cx1:
            datos_civil['nombre'] = st.text_input("Nombre y Apellido (Civil):")
            datos_civil['dni'] = st.text_input("DNI:")
            datos_civil['vinculo'] = st.selectbox("Vínculo:", ["Propietario", "Empleado", "Inquilino", "Otro"])
        with cx2:
            datos_civil['celular'] = st.text_input("Celular de contacto:")
            datos_civil['email'] = st.text_input("E-mail:")
            datos_civil['estado'] = st.selectbox("Situación del Registro:", [
                "ENTREGA VOLUNTARIA: Soporte preservado para PDI.",
                "NEGATIVA / ORDEN JUDICIAL: Requiere orden de secuestro.",
                "MANIFESTACIÓN TÉCNICA: No graba o está dañado.",
                "SOLICITUD DE PERITOS: Desconoce manejo técnico.",
                "RE-FILMACIÓN DE URGENCIA: Captación digital por riesgo de pérdida."
            ])
        st.warning("🖋️ FIRMA DEL RESPONSABLE PRIVADO")
        canvas_result = st_canvas(fill_color="rgba(255, 255, 255, 0)", stroke_width=3, stroke_color="#000", background_color="#fff", height=150, width=400, key="canvas_firma")
        if canvas_result.image_data is not None:
            firma_b64 = canvas_result.image_data

def generar_pdf_bytes():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "POLICIA DE LA PROVINCIA DE SANTA FE", ln=True, align="C")
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "ACTA DE INSPECCION OCULAR Y REGISTRO", ln=True, align="C")
    pdf.ln(5)
    
    pdf.set_font("Arial", "B", 10)
    pdf.cell(0, 8, f"REFERENTE ACTA Nro: {acta_nro} | FECHA: {fecha.strftime('%d/%m/%Y')}", ln=True)
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(0, 6, f"LUGAR: {lugar}\nHECHO: {hecho}\nPERSONAL ACTUANTE: {grade} {name_actuante} (Legajo: {legajo})")
    pdf.ln(5)
    
    # 1. INSPECCIÓN
    pdf.set_font("Arial", "B", 10)
    pdf.cell(0, 8, "1. INFORME TECNICO DE INSPECCION OCULAR:", ln=True)
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(0, 6, resultado_ia)
    
    # 2. PERÍMETRO AMPLIADO
    pdf.ln(3)
    pdf.set_font("Arial", "B", 10)
    pdf.cell(0, 8, "2. PRESERVACION DEL LUGAR DEL HECHO:", ln=True)
    pdf.set_font("Arial", "", 10)
    if perimetro == "SÍ":
        txt_peri = "Se hace constar que el Personal Actuante procedió a la correcta delimitación del área mediante el uso de cinta de peligro y vallado perimetral, garantizando la intangibilidad de la escena y preservando los rastros, huellas e indicios de interés para la presente investigación."
    else:
        txt_peri = "Se deja constancia que no se realizó el encintado perimetral debido a la premura del caso y la necesidad de priorizar la asistencia/seguridad, manteniendo no obstante la custodia visual ininterrumpida del lugar."
    pdf.multi_cell(0, 6, txt_peri)

    # 3. CÁMARAS PÚBLICAS
    if hay_publicas:
        pdf.ln(3)
        pdf.set_font("Arial", "B", 10)
        pdf.cell(0, 8, "3. RELEVAMIENTO DE VIDEOVIGILANCIA PUBLICA (911):", ln=True)
        pdf.set_font("Arial", "", 10)
        pdf.multi_cell(0, 6, f"Se detectaron dispositivos oficiales identificados como: {id_domos}. Se informa vía radial a la central operativa para el resguardo de las imágenes.")

    # 4. CÁMARAS PRIVADAS
    if hay_privadas:
        pdf.ln(3)
        pdf.set_font("Arial", "B", 10)
        pdf.cell(0, 8, "4. RELEVAMIENTO DE CAMARAS PRIVADAS Y COMPROMISO:", ln=True)
        pdf.set_font("Arial", "", 10)
        texto = f"Responsable: {datos_civil['nombre']}, DNI: {datos_civil['dni']}, Vinculo: {datos_civil['vinculo']}. Contacto: {datos_civil['celular']}. Situacion: {datos_civil['estado']}. El mismo se compromete al resguardo de las imagenes."
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
    pdf.cell(0, 5, f"Firma {grade} {name_actuante}", ln=True, align="R")
    return bytes(pdf.output())

st.divider()
if st.button("🏁 VALIDAR Y GENERAR"):
    if not resultado_ia:
        st.error("Falta el informe de inspección.")
    else:
        st.markdown(f'<div class="acta-previa"><div class="titulo-pdf">ACTA DE INSPECCIÓN OCULAR</div><p><b>ACTA N°:</b> {acta_nro} | <b>ACTUANTE:</b> {grade} {name_actuante}</p><p>{resultado_ia}</p></div>', unsafe_allow_html=True)
        st.subheader("⬇️ DESCARGAS OFICIALES")
        c_pdf, c_json = st.columns(2)
        try:
            pdf_data = generar_pdf_bytes()
            c_pdf.download_button(label="📄 Descargar Acta PDF", data=pdf_data, file_name=f"Acta_{acta_nro}.pdf", mime="application/pdf")
            json_data = json.dumps({"personal": name_actuante, "acta_nro": acta_nro, "perimetro": perimetro, "publicas": id_domos, "privadas": datos_civil if hay_privadas else "N/A"}, indent=4)
            c_json.download_button(label="💾 Descargar JSON", data=json_data, file_name=f"Data_{acta_nro}.json", mime="application/json")
        except Exception as e:
            st.error(f"Error: {e}")
