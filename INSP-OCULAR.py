import streamlit as st
import json
from datetime import datetime
from streamlit_drawable_canvas import st_canvas
from fpdf import FPDF
from io import BytesIO
from PIL import Image

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="S.I.V. Bloque 6 - INSPECCIÓN OCULAR", layout="wide")

# --- ESTILOS CSS JUDICIALES ---
st.markdown("""
    <style>
    .acta-previa { 
        background-color: white; 
        color: black; 
        padding: 45px; 
        border: 2px solid #000; 
        font-family: 'Times New Roman', serif; 
        line-height: 1.5;
        box-shadow: 5px 5px 15px rgba(0,0,0,0.1);
    }
    .titulo-pdf { text-align: center; font-weight: bold; text-decoration: underline; font-size: 20px; margin-bottom: 25px; text-transform: uppercase; }
    .watermark { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%) rotate(-45deg); opacity: 0.1; font-size: 80px; pointer-events: none; }
    </style>
    """, unsafe_allow_html=True)

# --- PANEL LATERAL ---
st.sidebar.title("S.I.V. SISTEMA DE VALIDACIÓN")
st.sidebar.write("**Módulo:** Inspección Ocular")
st.sidebar.write("**Autoría:** Sub Comisario CASTAÑEDA Juan")
st.sidebar.divider()

st.title("🛡️ INSPECCIÓN OCULAR")

# --- SECCIÓN 1: PERSONAL ACTUANTE ---
with st.expander("👤 PERSONAL ACTUANTE", expanded=True):
    c1, c2, c3 = st.columns(3)
    with c1: grade = st.selectbox("Grado:", ["Sub Comisario", "Principal", "Inspector", "Sub Inspector", "Oficial"])
    with c2: name_actuante = st.text_input("Apellido y Nombre:", "CASTAÑEDA Juan")
    with c3: legajo = st.text_input("Legajo / NI:", "123.456")

# --- SECCIÓN 2: REFERENCIA ADMINISTRATIVA ---
with st.expander("📝 REFERENCIA DEL PROCEDIMIENTO", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        acta_nro = st.text_input("REFERENTE ACTA N°:", placeholder="Ej: 123/26")
        lugar = st.text_input("Lugar del Hecho (Intersección/Domicilio):")
    with col2:
        hecho = st.text_input("Carátula Policial:", "ROBO CALIFICADO")
        fecha = st.date_input("Fecha de la Inspección:")

# --- SECCIÓN 3: CUERPO TÉCNICO ---
st.header("🔍 Informe de Inspección")
resultado_ia = st.text_area("Descripción técnica (Cardinal Norte, Sur, Este, Oeste):", height=200, help="Pegue aquí el texto procesado por la IA.")

st.header("🛡️ Preservación de la Escena")
perimetro = st.radio("¿Se procedió al encintado perimetral?", ["SÍ", "NO"], horizontal=True, help="Define la cláusula de seguridad en el acta.")

# --- SECCIÓN 4: VIDEOVIGILANCIA ---
st.header("📹 Relevamiento de Cámaras")
c_pub, c_priv = st.columns(2)
with c_pub: hay_publicas = st.checkbox("Cámaras Públicas (911 / Central de Monitoreo)")
with c_priv: hay_privadas = st.checkbox("Cámaras Privadas (Particulares / Comercios)")

id_domos = ""
datos_civil = {}
firma_b64 = None

if hay_publicas:
    id_domos = st.text_input("ID de Domos detectados:", placeholder="Ej: Domo 102, 44, 21")

if hay_privadas:
    st.subheader("🖋️ Compromiso de Resguardo (Privado)")
    cx1, cx2 = st.columns(2)
    with cx1:
        datos_civil['nombre'] = st.text_input("Nombre y Apellido del Responsable:")
        datos_civil['dni'] = st.text_input("DNI:")
        datos_civil['vinculo'] = st.selectbox("Vínculo:", ["Propietario", "Empleado", "Inquilino", "Encargado"])
    with cx2:
        datos_civil['celular'] = st.text_input("Celular:")
        datos_civil['estado'] = st.selectbox("Situación del Soporte:", [
            "ENTREGA VOLUNTARIA: Soporte preservado para PDI.",
            "NEGATIVA / ORDEN JUDICIAL: Se requiere orden de secuestro.",
            "MANIFESTACIÓN TÉCNICA: El equipo no graba.",
            "RE-FILMACIÓN DE URGENCIA: Captación digital por riesgo de pérdida."
        ])
    
    st.info("El civil debe firmar en el recuadro blanco para validar el compromiso.")
    canvas_result = st_canvas(fill_color="rgba(255, 255, 255, 0)", stroke_width=3, stroke_color="#000", background_color="#fff", height=150, width=450, key="canvas_firma")
    if canvas_result.image_data is not None:
        firma_b64 = canvas_result.image_data

# --- MOTOR DE GENERACIÓN PDF (BLINDADO) ---
def generar_pdf_blindado():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Encabezado
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "POLICIA DE LA PROVINCIA DE SANTA FE", ln=True, align="C")
    pdf.set_font("Arial", "BU", 12)
    pdf.cell(0, 10, "ACTA DE INSPECCION OCULAR", ln=True, align="C")
    pdf.ln(5)
    
    # Datos Referenciales
    pdf.set_font("Arial", "B", 10)
    pdf.cell(0, 7, f"REFERENTE ACTA Nro: {acta_nro} | FECHA: {fecha.strftime('%d/%m/%Y')}", ln=True)
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(0, 6, f"LUGAR: {lugar}\nHECHO: {hecho}\nPERSONAL ACTUANTE: {grade} {name_actuante} (NI: {legajo})")
    pdf.ln(5)
    
    # 1. Inspección
    pdf.set_font("Arial", "B", 10)
    pdf.cell(0, 8, "1. INFORME TECNICO DE INSPECCION OCULAR:", ln=True)
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(0, 6, resultado_ia)
    
    # 2. Perímetro
    pdf.ln(3)
    pdf.set_font("Arial", "B", 10)
    pdf.cell(0, 8, "2. PRESERVACION DEL LUGAR DEL HECHO:", ln=True)
    pdf.set_font("Arial", "", 10)
    txt_peri = ("Se hace constar que el Personal Actuante procedió a la correcta delimitación del área mediante el uso de cinta de peligro y vallado perimetral, garantizando la intangibilidad de la escena." if perimetro == "SÍ" else 
                "Se deja constancia que no se realizó el encintado perimetral debido a la urgencia operativa, manteniendo la custodia visual ininterrumpida del lugar.")
    pdf.multi_cell(0, 6, txt_peri)

    # 3. Cámaras
    if hay_publicas or hay_privadas:
        pdf.ln(3)
        pdf.set_font("Arial", "B", 10)
        pdf.cell(0, 8, "3. RELEVAMIENTO DE VIDEOVIGILANCIA:", ln=True)
        pdf.set_font("Arial", "", 10)
        if hay_publicas:
            pdf.multi_cell(0, 6, f"- PUBLICA: Se detectaron dispositivos oficiales ID: {id_domos}.")
        if hay_privadas:
            txt_priv = f"- PRIVADA: Responsable {datos_civil['nombre']}, DNI {datos_civil['dni']}. Situación: {datos_civil['estado']}. El mismo asume el compromiso de resguardo de las imágenes."
            pdf.multi_cell(0, 6, txt_priv)
            if firma_b64 is not None:
                img_firma = Image.fromarray(firma_b64.astype('uint8'), 'RGBA')
                buf = BytesIO()
                img_firma.save(buf, format="PNG")
                buf.seek(0)
                pdf.image(buf, x=20, y=pdf.get_y()+2, w=45)
                pdf.ln(22)
                pdf.set_font("Arial", "I", 8)
                pdf.cell(0, 5, f"Firma Responsable: {datos_civil['nombre']}", ln=True)

    # Pie de Firma
    pdf.ln(25)
    pdf.set_font("Arial", "B", 10)
    pdf.cell(0, 5, "__________________________", ln=True, align="R")
    pdf.cell(0, 5, f"Firma {grade} {name_actuante}", ln=True, align="R")
    pdf.cell(0, 5, f"NI: {legajo}", ln=True, align="R")
    
    return bytes(pdf.output())

# --- CIERRE Y DESCARGAS ---
st.divider()
if st.button("🏁 VALIDAR Y FINALIZAR ACTA"):
    if not resultado_ia or not acta_nro:
        st.error("Error: Debe completar el N° de Acta y el Informe Técnico.")
    else:
        st.markdown(f'<div class="acta-previa"><div class="titulo-pdf">ACTA DE INSPECCIÓN OCULAR</div><p><b>ACTA N°:</b> {acta_nro} | <b>FECHA:</b> {fecha}</p><p>{resultado_ia}</p></div>', unsafe_allow_html=True)
        
        st.subheader("📦 Exportación de Documentación")
        c_pdf, c_json = st.columns(2)
        try:
            pdf_out = generar_pdf_blindado()
            c_pdf.download_button("📄 Descargar ACTA DE INSPECCIÓN OCULAR (PDF)", data=pdf_out, file_name=f"Acta_Inspeccion_{acta_nro.replace('/','-')}.pdf", mime="application/pdf")
            
            js_out = json.dumps({"acta": acta_nro, "oficial": name_actuante, "inspeccion": resultado_ia, "camaras_priv": datos_civil if hay_privadas else "N/A"}, indent=4)
            c_json.download_button("💾 Descargar JSON de Respaldo", data=js_out, file_name=f"Data_B6_{acta_nro.replace('/','-')}.json", mime="application/json")
            st.success("Validación completada. Los archivos están listos para su resguardo.")
        except Exception as e:
            st.error(f"Error en la generación: {e}")
