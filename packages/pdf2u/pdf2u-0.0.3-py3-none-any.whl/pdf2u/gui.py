import tempfile

import streamlit as st
from streamlit_pdf_viewer import pdf_viewer


def show_config_popover():
    with st.popover("⚙️ Settings"):
        col1, col2 = st.columns(2)

        with col1:
            service = st.selectbox(
                "Service 🔄",
                options=["google", "openai", "bing"],
                key="service_select",
                help="select translation service",
            )

            source_lang = st.selectbox(
                "Origin 📖",
                options=["en", "zh", "ja", "ko", "fr", "de"],
                key="source_lang_select",
            )

        with col2:
            if service == "openai":
                api_key = st.text_input(
                    "OpenAI API Key 🔑",
                    type="password",
                    key="openai_key_input",
                    help="get your API key from OpenAI",
                )

            target_lang = st.selectbox(
                "Target 📝",
                options=["zh", "en", "ja", "ko", "fr", "de"],
                key="target_lang_select",
            )

        st.divider()

        col3, col4 = st.columns(2)
        with col3:
            qps = st.number_input(
                "QPS limit ⚡",
                min_value=1,
                value=4,
                key="qps_input",
                help="queries per second limit",
            )
            ignore_cache = st.toggle(
                "No Cache 🚫",
                key="ignore_cache_check",
                help="ignore cache and re-translate",
            )
        with col4:
            no_dual = st.toggle(
                "Disable Dual PDF 📄",
                key="no_dual_check",
                help="do not generate dual language PDF",
            )
            no_mono = st.toggle(
                "Disable Mono PDF 📄",
                key="no_mono_check",
                help="do not generate monolingual PDF",
            )

        st.divider()

        col5, col6 = st.columns([1, 3])
        with col5:
            if st.button(
                "Save", type="primary", key="save_config_btn", use_container_width=True
            ):
                st.session_state.config = {
                    "service": service,
                    "source_lang": source_lang,
                    "target_lang": target_lang,
                    "openai_key": api_key if service == "openai" else None,
                    "qps": qps,
                    "ignore_cache": ignore_cache,
                    "no_dual": no_dual,
                    "no_mono": no_mono,
                }
                st.toast("Settings saved! 🎉")


def main():
    st.set_page_config(
        layout="wide", page_title="PDF Translator", initial_sidebar_state="collapsed"
    )

    if "config" not in st.session_state:
        st.session_state.config = {
            "service": "google",
            "source_lang": "en",
            "target_lang": "zh",
            "qps": 4,
            "ignore_cache": False,
            "no_dual": False,
            "no_mono": False,
        }

    # with st.container():
    col1, col2, col3 = st.columns([4, 1, 1])
    with col2:
        if st.button(
            "🚀 Start", type="primary", key="translate_btn", use_container_width=True
        ):
            st.toast("Translation started! 🎉")
    with col3:
        show_config_popover()

    with st.container():
        uploaded_file = st.file_uploader(" ", type="pdf", key="pdf_uploader")

    if uploaded_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            pdf_path = tmp_file.name

        st.divider()
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 📄 Origin")
            pdf_viewer(pdf_path, width="100%", height=800, key="original_pdf")

        with col2:
            st.markdown("#### 📝 Translated")
            pdf_viewer(
                pdf_path,  # dummy
                width="100%",
                height=800,
                key="translated_pdf",
            )
    else:
        # 美化空状态提示
        st.markdown(
            """
            <div style='text-align: center; margin-top: 50px;'>
                <h3>👆 Please Upload PDF<h3>
            </div>
            """,
            unsafe_allow_html=True,
        )


if __name__ == "__main__":
    main()
