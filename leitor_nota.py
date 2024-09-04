import streamlit as st
import requests
import base64


st.set_page_config(page_title="Xml - DANFE", layout="centered")


with open("styles.css") as f:
    css = f.read()

st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)


st.markdown('<div class="my-texto_app">XML para DANFe/DACTe</div>', unsafe_allow_html=True)
st.markdown('<div class="my-sub_app">Converta o xml da NFe para DANFe ou o xml do CTe para DACTe</div>', unsafe_allow_html=True)


st.image("Imgs/seo.png", caption="", width=300)  


def selecionar_arquivo():
    uploaded_file = st.file_uploader("Escolha um arquivo XML", type="xml")
    return uploaded_file

def enviar_requisicao(xml_nfe):
    if xml_nfe:
       
        api_url = "https://ws.meudanfe.com/api/v1/get/nfe/xmltodanfepdf/API"

        headers = {
            'Content-Type': 'text/plain',
        }

        response = requests.post(api_url, headers=headers, data=xml_nfe)

        if response.status_code == 200:
            base64_response = response.text.strip('data:application/pdf;base64,').strip('"')

            pdf_data = base64.b64decode(base64_response)

          
            st.download_button(
                label="Download do PDF DANFE",
                data=pdf_data,
                file_name="danfe.pdf",
                mime="application/pdf"
            )

            st.success("PDF do DANFE salvo com sucesso.")
        else:
            st.error(f"Falha ao gerar PDF do DANFE! Confira o seu XML. Código de status HTTP: {response.status_code}")
    else:
        st.warning("Selecione um arquivo XML antes de enviar a requisição.")



xml_nfe = None


uploaded_file = selecionar_arquivo()

if uploaded_file:
    xml_nfe = uploaded_file.read()


if st.button("Gerar DANFE"):
    enviar_requisicao(xml_nfe)
