import streamlit as st

def modulo_croquis_inteligente():
    st.header("📐 TRANSFORMACIÓN DE INSPECCIÓN A PLANO")
    
    # 1. EL "ALMA" DEL ACTA: El texto de la inspección
    st.subheader("1. Redacción de la Inspección Ocular")
    relato = st.text_area("Describa lo observado (Este texto será el marco legal del croquis):", 
                          placeholder="Ej: Se observa sobre el plano de apoyo un arma de fuego...",
                          height=150)

    # 2. LA "PRUEBA": La foto del croquis o la escena
    st.subheader("2. Sustento Visual")
    img_evidencia = st.file_uploader("Suba la foto del croquis o relevamiento:", type=['jpg', 'png'])

    if img_evidencia and relato:
        st.success("✅ Sistema listo para fusionar relato y visión.")
        
        # 3. EL RESULTADO (Lo que viste en el otro chat)
        with st.container(border=True):
            st.markdown("### VISTA PREVIA DEL ACTA INTEGRADA")
            st.write(f"**RELATO:** {relato}")
            st.image(img_evidencia, caption="CROQUIS/RELEVAMIENTO FOTOGRÁFICO ADJUNTO")
            
        # Botón para mandarlo al PDF final del S.I.V.
        if st.button("INTEGRAR AL SUMARIO FINAL"):
            st.session_state['acta_inspeccion_lista'] = True
            st.balloons()
