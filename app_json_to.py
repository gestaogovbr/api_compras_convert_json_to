# Bibliotecas
import json
import requests
import pandas as pd
import streamlit as st

# Criar função para ler um JSON
@st.cache_data  # Adicionando cache à função
def read_json(url):
    response = requests.get(url)
    if response.status_code == 200:
        return json.loads(response.content)
    else:
        raise Exception("Erro ao recuperar os dados da API")

# Função para visualizar o DataFrame
def visualize_dataframe(data):
    if 'resultado' in data:
        df = pd.DataFrame(data['resultado'])
        st.session_state.dataframe = df
    else:
        st.warning("Nenhum dado disponível para visualização.")

# Função para exportar o DataFrame para Excel
def export_to_excel(data):
    if 'resultado' in data:
        df = pd.DataFrame(data['resultado'])
        df.to_excel("temp.xlsx", index=False)
        return True
    else:
        st.warning("Nenhum dado disponível para exportar.")
        return False

# Função para exportar o DataFrame para CSV
def export_to_csv(data):
    if 'resultado' in data:
        df = pd.DataFrame(data['resultado'])
        df.to_csv("temp.csv", index=False)
        return True
    else:
        st.warning("Nenhum dado disponível para exportar para CSV.")
        return False

# Layout Streamlit
st.title("JSON para Excel ou CSV")

# Nota de descrição
st.markdown("Esta aplicação permite a visualização e exportação de dados da "
            "[API Compras Governamentais](https://api-comprasv2.dth.nuvem.gov.br/swagger-ui/index.html#/) "
            "do governo brasileiro para formatos Excel e CSV, facilitando a análise subsequente desses dados.")


# Campo de pesquisa
url = st.text_input("Qual é a url da API?")
st.text("Exemplo de URL: ")
st.text("https://api-comprasv2.dth.nuvem.gov.br/modulo-pesquisa-preco/1_consultarMaterial?pagina=1&codigoItemCatalogo=267203")

st.divider()

# Initialising the session_state variables for excel and csv
if "exported_excel" not in st.session_state:
    st.session_state.exported_excel = False
if "exported_csv" not in st.session_state:
    st.session_state.exported_csv = False
if "dataframe" not in st.session_state:
    st.session_state.dataframe = pd.DataFrame()

# Botão de pesquisa
if st.button(" :sunglasses: Visualizar Prévia ", key="visualizar_button"):
    if url:
        try:
            # Use st.empty() para criar um espaço vazio no app
            message = st.text("Carregando dados...")

            data = read_json(url)
            visualize_dataframe(data)

            # Exportando dados para Excel e CSV
            st.session_state.exported_excel = export_to_excel(data)
            st.session_state.exported_csv = export_to_csv(data)

            # Remova a mensagem "Carregando dados..." usando a função empty()
            message.empty()

        except Exception as e:
            st.error("Ocorreu um erro ao recuperar os dados da API.")
            st.error(e)
    else:
        st.warning("Por favor, informe uma URL.")  # Adicionando aviso quando a URL estiver vazia

# Display the dataframe if it exists
if not st.session_state.dataframe.empty:
    st.dataframe(st.session_state.dataframe.head(6))

# Botões de download condicional
if st.session_state.exported_excel:
    st.download_button(
        label="Exportar para Excel",
        data=open("temp.xlsx", "rb"),
        file_name="dataframe_exportado.xlsx",
    )

if st.session_state.exported_csv:
    st.download_button(
        label="Exportar para CSV",
        data=open("temp.csv", "rb"),
        file_name="dataframe_exportado.csv",
    )
