import pandas as pd
import streamlit as st
import requests
import time

#Criando função para converter o DF em um .csv (para poder fazer o download)
    #para armazenar caso o DF n seja filtrado, n preecisando fazer a conversao novamente 
@st.cache_data
    #função:
def converte_csv(df):
    return df.t_csv(index=False).encode('utf-8')

#Criando função de mensagem de sucesso do download
def mensagem_sucesso():
    sucesso = st.success('Arquivo baixado com sucesso!', icon = "✅")
    time.sleep(5)
    sucesso.empty()


st.title('DADOS BRUTOS')

url = 'https://labdados.com/produtos'
dados = pd.DataFrame.from_dict(response.json())
dados['Data da Compra'] = pd.to_datetime(dados['Data da Compra'], format = '%d%m%Y')



#selecionando as colunas que quero que apareçam
    ## Selecionando as colunas
with st.expander('Colunas'):
    colunas = st.multiselect('Selecione as colunas', list(dados.columns), list(dados.columns))
st.sidebar.title('Filtros')

    ## Selecionando os nomes dos produtos
with st.sidebar.expander('Nome do produto'):
    produtos = st.multiselect('Selecione os produtos', list(dados['Produto'].unique()), dados['Produto'].unique())

    ## Selecionando a categoria do produto
with st.sidebar.expander('Categoria do produto'):
    categoria = st.multiselect('Selecione a categoria', dados['Categoria do Produto'].unique(), dados['Categoria do Produto'].unique())

    ## Selecionando o preço do produto
with st.sidebar.expander('Preço do produto'):
    preco = st.slider('Selecione o preço', 0, 5000,(0,5000))

    ##Selecionando o frete
with st.sidebar.expander('Frete da venda'):
    frete = st.slider('Frete', 0,250, (0,250))

    ##Selecionando data da compra
with st.sidebar.expander('Data da compra'):
    data_compra = st.date_input('Selecione a data', (dados['Data da Compra'].min(), dados['Data da Compra'].max()))

    ##Selecionando os vendedores
with st.sidebar.expander('Vendedor'):
    vendedores = st.multiselect('Selecione os vendedores',(dados['Vendedor'].unique(), dados['Vendedor'].unique()))

    ##Selecionando o local da compra
with st.sidebar.expander('Local da compra'):
    st.multiselect('Selecione o local da compra', dados['Local da compra'].unique(), dados['Local da compra'].unique())

    ##Selecionando a avaliação da compra
with st.sidebar.expander('Avaliação da compra'):
    avaliacao = st.slider('Selecione a avaliaçao da compra',1,5, value = (1,5))

    ##Selecionando o tipo de pagamento
with st.sidebar.expander('Tipo de pagamento'):
    tipo_pagamento = st.multiselect('Selecione o tipo de pagamento', dados['Tipo de pagamento'].unique(), dados['Tipo de pagamento'].unique())

    ##Selecionando a uantidade de parcelras
with st.sidebar.expander('Quantidade de parcelas'):
    qtd_parcelas = st.slider('Selecione a quantidade de parcelas', 1, 24, (1,24))


#Fazendo a filtragem das colunas
query = '''
Produto in @produtos and \
@preco[0] <= Preço <= @preco[1] and \
@frete[0] <= Frete <= @frete[1] and \
@data_compra[0] <= `Data de Compra` <= @data_compra[1] and \
Vendedor in @vendedores and \
`Local da compra` in @local_compra and \
@avaliacao[0] <= `Avaliação da compra` < @avaliacao[1] and \
`Tipo de pagamento` in @tipo_pagamento and \
@qtd_parcelas[0] <= `Quantidade de parcelas` <= @qtd_parcelas[1]
'''

dados_filtrados = dados.query(query)
dados_filtrados = dados_filtrados[colunas]

st.dataframe(dados_filtrados)

st.markdown(f'A tabela possui :blue[{dados_filtrados.shape[0]}] linhas e :blue[{dados_filtrados.shape[1]} colunas]')

st.markdown('Escreva um nome para o arquivo')
coluna1, coluna2 = st.columns(2)
with coluna1:
    nome_arquivo = st.text_input('', label_visibility = 'collapsed', value = 'dados')
    nome_arquivo += '.csv'
with coluna2:
    st.download_button('Fazer o download da tabela em csv', data = converte_csv(dados_filtrados), file_name = nome_arquivo, mime = 'text/csv', on_click = mensagem_sucesso)
