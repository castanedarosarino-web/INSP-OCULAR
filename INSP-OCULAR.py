import streamlit as st
import json
from datetime import datetime

# CONFIGURACIÓN Y ESTILO PROFESIONAL
st.set_page_config(page_title="SIV - Inspección Ocular Integrada", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f5f5f5; }
    .stTextArea textarea { font-size: 14px !important; }
    .croquis-final { 
        border: 3px solid #000; 
        padding: 30px; 
        background-color: white; 
        font-family: 'Arial', sans-serif;
        color: black;
    }
    .header-table { width: 100%; border-bottom: 2px solid black; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# AUTORÍA
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/b/b5/Escudo_de_la_Polic%C3%ADa_de_Santa_Fe.png", width=100)
st.sidebar.markdown(f"### Autoría:\n**Sub Comisario CASTAÑEDA Juan**")

# SIMULACIÓN DE INTEGRACIÓN DE BLOQUES (Aquí el SIV toma datos de B2 y B5)
# En un futuro, estos datos vendrán del st.session_state global
st.sidebar.header("📥 Datos Integrados")
nombre_detenido = st.sidebar.text_input("Dato de Bloque 2 (Aprehendido):", value="GOMEZ, Ramón")
objeto_secuestro = st.sidebar.text_input("Dato de Bloque 5 (Secuestro):", value="Revólver Cal. 38")

st.title("🛡️ S.I.V. - Módulo de Inspección y Planimetría")

# 1. ENTRADA DE DATOS TÉCNICOS
with st.container():
    col_a, col_b = st.columns([1, 1])
    with col_a:
        st.subheader("📍 Ubicación y Escenario")
        lugar = st.text_input("Lugar exacto del hecho:", value="Mendoza y Martín Rodríguez")
        clima = st.selectbox("Estado Climático:", ["Despejado", "Lluvia", "Niebla", "Nublado"])
        luz = st.selectbox("Iluminación Artificial:", ["Excelente", "Regular", "Nula", "Luz Solar"])
    
    with col_b:
        st.subheader("🧭 Descripciones por Cardinal (IA)")
        norte = st.text_input("NORTE:", placeholder="Descripción de la calzada...")
        sur = st.text_input("SUR:", placeholder="Descripción de la intersección...")
        este = st.text_input("ESTE:", placeholder="Descripción de la acera...")
        oeste = st.text_input("OESTE:", placeholder="Descripción de los locales...")

# 2. CONFIGURACIÓN DEL CROQUIS (REFERENCIAS DINÁMICAS)
st.divider()
st.subheader("🔢 Configuración de Referencias")
c1, c2, c3 = st.columns(3)
ref_1 = c1.text_input("Ref ①:", value=f"Aprehendido ({nombre_detenido})")
ref_2 = c2.text_input("Ref ②:", value=f"Secuestro ({objeto_secuestro})")
ref_3 = c3.text_input("Ref ③:", value="Unidad Móvil Policial")

# 3. EJECUCIÓN: INSPECCIÓN OCULAR + CROQUIS
if st.button("🏁 GENERAR INSPECCIÓN OCULAR Y CROQUIS DEMOSTRATIVO"):
    
    # --- PARTE A: REDACCIÓN PARA EL ACTANTE ---
    st.success("✅ Informe generado para el Actante")
    texto_acta = f"""INSPECCIÓN OCULAR: En la fecha y hora señalada, se constituye personal policial en {lugar}. 
    Se observa un escenario con visibilidad {luz} y condiciones climáticas {clima}. 
    Se procede al registro fotográfico constatando: Al NORTE {norte}; al SUR {sur}; al ESTE {este} y al OESTE {oeste}. 
    Se hace constar que la Referencia ① corresponde a la ubicación de {ref_1} y la Referencia ② al hallazgo de {ref_2}."""
    st.code(texto_acta, language="")

    # --- PARTE B: CROQUIS DEMOSTRATIVO (EL RESULTADO VISUAL) ---
    st.markdown('<div class="croquis-final">', unsafe_allow_html=True)
    
    # Encabezado Formulario
    st.markdown(f"""
    <table class="header-table">
        <tr>
            <td style="text-align:left;"><b>POLICÍA DE SANTA FE</b><br>U.R. II - ROSARIO</td>
            <td style="text-align:center;"><b>CROQUIS DEMOSTRATIVO</b><br>INSPECCIÓN OCULAR</td>
            <td style="text-align:right;"><b>FECHA:</b> {datetime.now().strftime('%d/%m/%Y')}</td>
        </tr>
    </table>
    <p><b>LUGAR:</b> {lugar} | <b>VISIBILIDAD:</b> {luz}</p>
    """, unsafe_allow_html=True)

    # Cuerpo del Croquis
    col_ref, col_dibujo = st.columns([1, 2])
    with col_ref:
        st.markdown(f"""
        **REFERENCIAS:**<br>
        ① {ref_1}<br>
        ② {ref_2}<br>
        ③ {ref_3}<br><br>
        **OBSERVACIONES:**<br>
        Se orienta el presente hacia el<br>
        Cardinal Norte. No se realiza<br>
        a escala técnica, solo demostrativa.
        """, unsafe_allow_html=True)

    with col_dibujo:
        # Representación gráfica mejorada
        st.markdown(f"""
        <div style="border: 2px solid #333; padding: 20px; text-align: center; background: #fafafa;">
            <b>NORTE (▲)</b><br>
            <div style="font-family: monospace; line-height: 1.2;">
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[ CALLE MENDOZA ]<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|<br>
            -----(L.C.)-----+-----(L.C.)-----<br>
            M. RODRÍGUEZ (E)&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp; (O) M. RODRÍGUEZ<br>
            -----(L.C.)-----+-----(L.C.)-----<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;<b>① ②</b><br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>③</b>&nbsp;&nbsp;&nbsp;|<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[ CALLE MENDOZA ]<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|<br>
            </div>
            <b>SUR</b>
        </div>
        """, unsafe_allow_html=True)

    # Pie de firmas
    st.markdown("<br><br>", unsafe_allow_html=True)
    f1, f2, f3 = st.columns(3)
    f1.markdown("<hr>Firma Oficial Actante", unsafe_allow_html=True)
    f2.markdown("<hr>Firma Testigo 1", unsafe_allow_html=True)
    f3.markdown("<hr>Firma Testigo 2", unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# BOTÓN DE DESCARGA DE DATOS PARA EL SUMARIO
st.sidebar.download_button("💾 Exportar para SUMARIO SVI", json.dumps({"informe": "texto_acta", "lugar": lugar}))
