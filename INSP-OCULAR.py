import streamlit as st
import json
from datetime import datetime, date

# Configuración de página
st.set_page_config(page_title="SVI - Bloque 6 Inspección Ocular", layout="wide")

# =========================
# CABECERA Y AUTORÍA (CORREGIDO)
# =========================
st.title("🗺️ BLOQUE 6 - INSPECCIÓN OCULAR")
st.markdown("### Sistema de Validación de Identidad (S.I.V.)")
st.sidebar.markdown("### Autoría:\n**Sub Comisario CASTAÑEDA Juan**")

# =========================
# ESTADO DE SESIÓN
# =========================
if "ocular" not in st.session_state:
    st.session_state.ocular = {
        "ubicacion": "",
        "escenario": "VÍA PÚBLICA",
        "iluminacion": "ALUMBRADO PÚBLICO (BUENO)",
        "clima": "DESPEJADO",
        "norte": "", "sur": "", "este": "", "oeste": "",
        "croquis_data": ""
    }

# =========================
# 1. DATOS DEL ENTORNO
# =========================
with st.expander("🌍 CONDICIONES DEL LUGAR", expanded=True):
    a1, a2 = st.columns(2)
    st.session_state.ocular["ubicacion"] = a1.text_input("Ubicación Exacta (Calle/Altura/Intersección):", st.session_state.ocular["ubicacion"])
    st.session_state.ocular["escenario"] = a2.selectbox("Tipo de Escenario:", ["VÍA PÚBLICA", "DOMICILIO PARTICULAR", "LOCAL COMERCIAL", "BALDÍO/CAMPO"])
    
    b1, b2 = st.columns(2)
    st.session_state.ocular["iluminacion"] = b1.selectbox("Iluminación:", ["LUZ SOLAR", "ALUMBRADO PÚBLICO (BUENO)", "ALUMBRADO PÚBLICO (DEFICIENTE)", "OSCURIDAD TOTAL"])
    st.session_state.ocular["clima"] = b2.selectbox("Condiciones Climáticas:", ["DESPEJADO", "LLUVIA", "NIEBLA", "VIENTOS FUERTES"])

# =========================
# 2. REGISTRO POR CARDINALES (INFORME IA)
# =========================
st.subheader("📸 Descripciones Técnicas (Fotos)")
st.info("💡 Pegue aquí las descripciones generadas por Gemini a partir de las fotos panorámicas.")

c1, c2 = st.columns(2)
st.session_state.ocular["norte"] = c1.text_area("📷 CARDINAL NORTE:", value=st.session_state.ocular["norte"], placeholder="Ej: Calzada asfáltica, sentido doble de circulación...")
st.session_state.ocular["sur"] = c2.text_area("📷 CARDINAL SUR:", value=st.session_state.ocular["sur"])

c3, c4 = st.columns(2)
st.session_state.ocular["este"] = c3.text_area("📷 CARDINAL ESTE:", value=st.session_state.ocular["este"])
st.session_state.ocular["oeste"] = c4.text_area("📷 CARDINAL OESTE:", value=st.session_state.ocular["oeste"])

# =========================
# 3. GENERADOR DE INFORME Y CROQUIS
# =========================
st.divider()

if st.button("🚀 GENERAR INFORME Y CROQUIS PARA EL ACTANTE"):
    # REDACCIÓN AUTOMÁTICA DEL INFORME
    informe_final = (
        f"INSPECCIÓN OCULAR: En el lugar del hecho ({st.session_state.ocular['ubicacion']}), "
        f"se observa un escenario de {st.session_state.ocular['escenario']}, bajo condiciones de {st.session_state.ocular['iluminacion']} "
        f"y clima {st.session_state.ocular['clima']}. SE CONSTATÓ: "
        f"Al NORTE: {st.session_state.ocular['norte']}; "
        f"al SUR: {st.session_state.ocular['sur']}; "
        f"al ESTE: {st.session_state.ocular['este']}; "
        f"y al OESTE: {st.session_state.ocular['oeste']}. "
        f"Se realizaron tomas fotográficas que se agregan a foja siguiente."
    )
    
    st.subheader("📄 Texto para el Acta (Copiar/Pegar)")
    st.code(informe_final, language="")

    # BOSQUEJO DEL CROQUIS (VISUALIZACIÓN ESQUEMÁTICA)
    st.subheader("🗺️ Bosquejo Planimétrico (Orientado al Norte)")
    
    croquis = f"""
    +-----------------------------------------------------------+
    |         BOSQUEJO DE INSPECCIÓN OCULAR - CARDINAL NORTE ▲  |
    +-----------------------------------------------------------+
    |                                                           |
    |      [ NORTE ]                                            |
    |      {st.session_state.ocular['norte'][:40]}...            |
    |                                                           |
    |  [ OESTE ]                      [ ESTE ]                  |
    |  {st.session_state.ocular['oeste'][:20]}...    +     {st.session_state.ocular['este'][:20]}...   |
    |                                 |                         |
    |                                [D] Punto Aprehensión      |
    |                                [S] Objeto Secuestrado     |
    |                                                           |
    |      [ SUR ]                                              |
    |      {st.session_state.ocular['sur'][:40]}...              |
    |                                                           |
    +-----------------------------------------------------------+
    |  REFERENCIAS: [D] Detenido | [S] Secuestro | [=] L.E.     |
    +-----------------------------------------------------------+
    """
    st.code(croquis, language="")

# =========================
# EXPORTACIÓN
# =========================
data_export = {
    "modulo": "BLOQUE_6_OCULAR",
    "autor": "SUB COMISARIO CASTAÑEDA JUAN",
    "datos": st.session_state.ocular,
    "timestamp": str(datetime.now())
}

st.download_button(
    "💾 EXPORTAR DATOS OCULAR",
    json.dumps(data_export, indent=4, ensure_ascii=False),
    file_name=f"SVI_B6_OCULAR_{date.today()}.json"
)
