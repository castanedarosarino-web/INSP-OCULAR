import streamlit as st


def modulo_croquis_inteligente():
    st.header("📐 TRANSFORMACIÓN DE INSPECCIÓN A PLANO")

    st.subheader("1. Redacción de la Inspección Ocular")

    relato = st.text_area(
        "Describa lo observado (este texto será el marco legal del croquis):",
        placeholder="Ej: Se observa en el lugar una abertura violentada, elementos removidos y desorden generalizado...",
        height=150
    )

    st.subheader("2. Sustento Visual")

    img_evidencia = st.file_uploader(
        "Suba la foto del croquis o relevamiento:",
        type=['jpg', 'png', 'jpeg']
    )

    if img_evidencia and relato:
        st.success("✅ Sistema listo para fusionar relato y visión.")

        with st.container(border=True):
            st.markdown("### VISTA PREVIA DEL ACTA INTEGRADA")
            st.write(f"**RELATO:** {relato}")
            st.image(
                img_evidencia,
                caption="CROQUIS / RELEVAMIENTO FOTOGRÁFICO ADJUNTO",
                use_container_width=True
            )

        if st.button("INTEGRAR AL SUMARIO FINAL"):
            st.session_state['acta_inspeccion_lista'] = True
            st.session_state['relato_inspeccion'] = relato
            st.success("✅ Inspección integrada al sumario final")
            st.balloons()


st.title("S.I.V. - Módulo Croquis Inteligente")

modulo_croquis_inteligente()
