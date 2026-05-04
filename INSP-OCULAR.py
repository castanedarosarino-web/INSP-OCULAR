import streamlit as st
import json
from datetime import datetime

# CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="S.I.V. - Bloque 6", layout="wide")

# ESTILO CSS JUDICIAL
st.markdown("""
    <style>
    .acta-judicial {
        background-color: white;
        color: black;
        padding: 45px;
        border: 2px solid #000;
        font-family: 'Arial', sans-serif;
    }
    .header-oficial { text-align: center; border-bottom: 2px solid black; margin-bottom: 20px; padding-bottom: 10px; }
    .titulo-principal { 
        text-align: center; 
        font-weight: bold; 
        text-decoration: underline; 
        font-size: 20px; 
        margin: 20px 0;
        text-transform: uppercase;
    }
    .seccion-label { font-weight: bold; text-decoration: underline; margin-top: 15px; display: block; }
    .croquis-box { border: 2px solid black; padding: 15px; background: #fcfcfc; font-family: monospace; text-align: center; margin-top: 10px; }
    .firmas-grid { margin-top: 60px; display: flex; justify-content: space-between; }
    .bloque-firma { border-top: 1px solid black; width: 30%; text-align: center; font-size: 11px; padding-top: 5px; }
    
    @media print {
        .no-print, .stButton, footer, header, .stSidebar { display: none !important; }
        .acta-judicial { border: none !important; padding: 0 !important; }
    }
    </style>
    """, unsafe_allow_html=True)

# LATERAL
st.sidebar.title("S.I.V. SISTEMA DE VALIDACIÓN")
st.sidebar.write("**Autoría:** Sub Comisario CASTAÑEDA Juan")

# --- CARGA DE DATOS ---
st.title("🛡️ Generador de Acta y Croquis")

with st.expander("📝 DATOS DE CABECERA", expanded=True):
    c1, c2 = st.columns(2)
    with c1:
        causa = st.text_input("Causa / Sumario N°:", "775/26")
        lugar = st.text_input("Lugar del Hecho:", "Mendoza y Martín Rodríguez")
    with c2:
        hecho = st.text_input("Carátula:", "ROBO CALIFICADO")
        fecha_acta = datetime.now().strftime('%d/%m/%Y')

st.subheader("1. Informe de Inspección")
resultado_ia = st.text_area("Pegue aquí el texto técnico de la IA:", height=150)

st.subheader("2. Resguardo y Cámaras")
col_a, col_b = st.columns(2)
with col_a:
    perimetro = st.radio("¿Se preservó el perímetro?", ["SÍ", "NO"], horizontal=True)
with col_b:
    hay_camaras = st.checkbox("¿Se detectaron cámaras de seguridad?")

# Datos de Cámaras (Condicional)
datos_camara = {}
if hay_camaras:
    with st.container():
        st.markdown("---")
        st.write("**Datos del Responsable de Cámara**")
        cx1, cx2, cx3 = st.columns(3)
        with cx1:
            datos_camara['nombre'] = st.text_input("Nombre y Apellido:")
            datos_camara['dni'] = st.text_input("DNI:")
        with cx2:
            datos_camara['celular'] = st.text_input("Celular:")
            datos_camara['email'] = st.text_input("E-mail:")
        with cx3:
            datos_camara['vinculo'] = st.selectbox("Vínculo:", ["Propietario", "Empleado", "Inquilino", "Otro"])
            datos_camara['estado'] = st.selectbox("Situación del Registro:", [
                "ENTREGA VOLUNTARIA: Soporte preservado para PDI.",
                "NEGATIVA / ORDEN JUDICIAL: Se requiere orden de secuestro.",
                "MANIFESTACIÓN TÉCNICA: El equipo no graba o está dañado.",
                "SOLICITUD DE PERITOS: Desconocimiento técnico del propietario.",
                "RE-FILMACIÓN DE URGENCIA: Captación digital por riesgo de pérdida."
            ])

# --- PROCESAMIENTO Y VISTA PREVIA ---
if st.button("🏁 GENERAR DOCUMENTO FINAL"):
    if not resultado_ia:
        st.error("Falta el informe de inspección.")
    else:
        st.markdown('<div class="acta-judicial">', unsafe_allow_html=True)
        
        # CABECERA OFICIAL
        st.markdown(f"""
        <div class="header-oficial">
            <h2 style="margin:0; font-size:18px;">POLICÍA DE LA PROVINCIA DE SANTA FE</h2>
            <p style="margin:5px 0; font-size:14px;">UNIDAD REGIONAL II - ROSARIO | <b>S.I.V. SISTEMA DE VALIDACIÓN</b></p>
        </div>
        <div class="titulo-principal">ACTA DE INSPECCIÓN OCULAR Y CROQUIS DEMOSTRATIVO</div>
        
        <div style="display:flex; justify-content:space-between; font-weight:bold; margin-bottom:15px;">
            <span>CAUSA: {causa}</span>
            <span>FECHA: {fecha_acta}</span>
        </div>
        <p><b>LUGAR:</b> {lugar}<br><b>HECHO:</b> {hecho}<br><b>ACTANTE:</b> S/C CASTAÑEDA Juan</p>
        <hr style="border:1px solid black;">
        """, unsafe_allow_html=True)

        # TEXTO DE LA INSPECCIÓN
        st.markdown('<span class="seccion-label">INFORME TÉCNICO DE INSPECCIÓN:</span>', unsafe_allow_html=True)
        st.markdown(f'<p style="text-align:justify;">{resultado_ia}</p>', unsafe_allow_html=True)

        # TEXTO DE RESGUARDO
        txt_peri = "se procedió a la correcta delimitación y preservación del perímetro" if perimetro == "SÍ" else "no se realizó encintado por razones de urgencia operativa"
        st.markdown('<span class="seccion-label">DILIGENCIAS DE RESGUARDO:</span>', unsafe_allow_html=True)
        st.markdown(f'<p>Se hace constar que, previo al inicio de las tareas, {txt_peri}.</p>', unsafe_allow_html=True)

        # TEXTO DE CÁMARAS
        if hay_camaras:
            st.markdown('<span class="seccion-label">RELEVAMIENTO DE CÁMARAS:</span>', unsafe_allow_html=True)
            st.markdown(f"""
            <p style="text-align:justify;">
            Se identifica como responsable al Sr./Sra. <b>{datos_camara['nombre']}</b>, DNI <b>{datos_camara['dni']}</b>, 
            en carácter de {datos_camara['vinculo']}, contacto <b>{datos_camara['celular']}</b> y correo <b>{datos_camara['email']}</b>. 
            Situación: {datos_camara['estado']}. El responsable se compromete formalmente al resguardo de las imágenes 
            correspondientes a la franja horaria del hecho.
            </p>
            """, unsafe_allow_html=True)

        # CROQUIS
        st.markdown('<div class="croquis-box">', unsafe_allow_html=True)
        st.markdown("<b>CROQUIS DEMOSTRATIVO (NORTE ▲)</b>", unsafe_allow_html=True)
        st.markdown("""
        <pre style="background:none; border:none; margin:10px 0; font-weight:bold; line-height:1.2;">
                  [ CALLE MENDOZA ]
             ----------+----------
             (E)       | ① ②     (O)
             ----------+----------
                       |
                       |
                  [ CALLE MENDOZA ]
        </pre>
        <p style="font-size:10px; margin:0;">① Aprehensión | ② Evidencia | ③ Móvil Policial</p>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # FIRMAS
        st.markdown('<div class="firmas-grid">', unsafe_allow_html=True)
        st.markdown(f'<div class="bloque-firma">S/C CASTAÑEDA Juan<br><b>Oficial Actante</b></div>', unsafe_allow_html=True)
        if hay_camaras:
            st.markdown(f'<div class="bloque-firma">{datos_camara["nombre"]}<br><b>Responsable Cámara</b></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="bloque-firma">Testigo 1<br><b>Firma / Aclaración</b></div>', unsafe_allow_html=True)
        st.markdown('<div class="bloque-firma">Testigo 2 / PDI<br><b>Firma / Aclaración</b></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)
        st.success("✅ Documento listo. Use Ctrl+P para guardar como PDF.")
