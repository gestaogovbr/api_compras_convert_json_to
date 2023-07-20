# Bibliotecas
import json
import requests
import pandas as pd
import streamlit as st

# Criar função para ler um JSON
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
        st.dataframe(df.head(10))
    else:
        st.warning("Nenhum dado disponível para visualização.")

# Função para exportar o DataFrame para Excel
def export_to_excel(data):
    if 'resultado' in data:
        df = pd.DataFrame(data['resultado'])
        with pd.ExcelWriter("temp.xlsx") as writer:
            df.to_excel(writer, index=False)
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
st.title("JSON para Excel")

# Campo de pesquisa
url = st.text_input("Qual é a url da API?")
st.text("Exemplo de URL: 'https://api-comprasv2.dth.nuvem.gov.br/modulo-pesquisa-preco/1_consultarMaterial?pagina=1&codigoItemCatalogo=267203'")
st.text("https://api-comprasv2.dth.nuvem.gov.br/modulo-pesquisa-preco/1_consultarMaterial?pagina=1&codigoItemCatalogo=267203")

# Variável de controle para exibir o botão de download após a exportação
exported_excel = False
exported_csv = False

# Botão de pesquisa
if st.button("Visualizar", key="visualizar_button"):
    if url:
        try:
            st.text("Carregando dados...")
            data = read_json(url)
            visualize_dataframe(data)
        except Exception as e:
            st.error("Ocorreu um erro ao recuperar os dados da API.")
            st.error(e)

# Botão de exportação para Excel
if st.button("Exportar para Excel", key="exportar_excel_button"):
    if url:
        try:
            st.text("Exportando para Excel...")
            with st.spinner("Exportando... Aguarde o download do arquivo."):
                data = read_json(url)
                if export_to_excel(data):
                    exported_excel = True
                    st.success("Dados exportados com sucesso! Clique abaixo para baixar o arquivo Excel.")
        except Exception as e:
            st.error("Ocorreu um erro ao exportar os dados para Excel.")
            st.error(e)

# Botão de exportação para CSV
if st.button("Exportar para CSV", key="exportar_csv_button"):
    if url:
        try:
            st.text("Exportando para CSV...")
            with st.spinner("Exportando... Aguarde o download do arquivo."):
                data = read_json(url)
                if export_to_csv(data):
                    exported_csv = True
                    st.success("Dados exportados com sucesso! Clique abaixo para baixar o arquivo CSV.")
        except Exception as e:
            st.error("Ocorreu um erro ao exportar os dados para CSV.")
            st.error(e)

# Botões de download condicional
if exported_excel:
    st.download_button(
        label="Clique aqui para baixar o arquivo Excel",
        data=open("temp.xlsx", "rb"),
        file_name="dataframe_exportado.xlsx",
    )

if exported_csv:
    st.download_button(
        label="Clique aqui para baixar o arquivo CSV",
        data=open("temp.csv", "rb"),
        file_name="dataframe_exportado.csv",
    )
