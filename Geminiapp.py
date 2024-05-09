import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import timedelta
import numpy as np
import matplotlib.pyplot as plt
import requests
from textblob import TextBlob

# Função para importar dados CSV
@st.cache_data
def importar_dados():
    df = pd.read_csv('dadosdf_cripto.csv')
    df['tempo'] = pd.to_datetime(df['tempo'])
    return df

# Carregar dados
df = importar_dados()

# Funções para calcular indicadores técnicos
def calculate_moving_averages(df):
    df['SMA'] = df['fechamento'].rolling(window=20).mean()
    return df

def calculate_rsi(df):
    df['delta'] = df['fechamento'].diff(1)
    df['up'] = df['delta'].where(df['delta'] > 0, 0)
    df['down'] = -df['delta'].where(df['delta'] < 0, 0)
    df['avg_up'] = df['up'].rolling(window=14).mean()
    df['avg_down'] = df['down'].rolling(window=14).mean()
    df['RSI'] = 100 - (100 / (1 + df['avg_down'] / df['avg_up']))
    return df

def calculate_macd(df):
    df['EMA_short'] = df['fechamento'].ewm(span=12, min_periods=12).mean()
    df['EMA_long'] = df['fechamento'].ewm(span=26, min_periods=26).mean()
    df['MACD'] = df['EMA_short'] - df['EMA_long']
    df['MACD_signal'] = df['MACD'].ewm(span=9, min_periods=9).mean()
    df['MACD_line'] = df['MACD'] - df['MACD_signal']
    return df

# Configurar título e subtítulo da dashboard
st.title('Dashboard Avançada de Análise de Criptomoedas')
st.subheader('Sua Jornada Personalizada para Insights e Descobertas')

# Criar menu lateral com opções de navegação
opcoes = ['Home', 'Visualização', 'Análise', 'Sobre']
escolha = st.sidebar.selectbox("Escolha uma opção", opcoes)

# Página Home
if escolha == 'Home':
    st.write("""
        Bem-vindo à Dashboard Avançada de Análise de Criptomoedas!
        Aqui você encontrará ferramentas poderosas para explorar e entender o mercado de criptomoedas de forma personalizada.
        """)
    # Adicione um link de imagem online ou carregue a imagem no código
    st.image("link_para_imagem_online.jpg", use_column_width=True)

# Página Visualização
if escolha == 'Visualização':
    criptomoedas = df['moeda'].unique()
    moeda_selecionada = st.selectbox('Selecione uma Moeda para Visualização:', criptomoedas)

    if st.button(f'Visualizar Gráfico para {moeda_selecionada}'):
        df_moeda = df[df['moeda'] == moeda_selecionada]
        fig = px.line(df_moeda, x='tempo', y='fechamento', title=f'Preço de Fechamento ao Longo do Tempo para {moeda_selecionada}')
        st.plotly_chart(fig)

# Página Análise
if escolha == 'Análise':
    criptomoedas = df['moeda'].unique()
    moeda_selecionada = st.sidebar.selectbox('Selecione uma Moeda para Análise Detalhada:', criptomoedas)

    with st.sidebar.header('Tipo de Análise'):
        # Página Análise (continuação)
        tipo_analise = st.selectbox('Escolha o tipo de análise:', ['Correlação', 'Indicadores', 'Volume', 'Preço', 'Volatilidade'])

    # Análise de Correlação
    if tipo_analise == 'Correlação':
        # Matriz de correlação interativa
        fig_matrix = px.scatter_matrix(df, x=df.columns, title='Matriz de Correlação')
        st.plotly_chart(fig_matrix)

        # Análise de correlação detalhada por par
        par_selecionado = st.selectbox('Selecione um Par para Análise Detalhada:', df.columns)
        fig_scatter = px.scatter(df, x=par_selecionado, y='fechamento', trendline="ols",
                                labels={'variable': 'Preço de Fechamento'},
                                title=f'Correlação entre {par_selecionado} e Preço de Fechamento para {moeda_selecionada}')
        st.plotly_chart(fig_scatter)

    # Análise de Indicadores
    elif tipo_analise == 'Indicadores':
        # Médias Móveis (SMA)
        df_moeda = calculate_moving_averages(df.copy())
        fig_ma = px.line(df_moeda, x='tempo', y=['fechamento', 'SMA'], title='Médias Móveis (SMA)')
        st.plotly_chart(fig_ma)

        # Índice de Força Relativa (RSI)
        df_moeda = calculate_rsi(df_moeda.copy())
        fig_rsi = px.line(df_moeda, x='tempo', y='RSI', title='Índice de Força Relativa (RSI)')
        st.plotly_chart(fig_rsi)

        # Divergência de Convergência de Média Móvel (MACD)
        df_moeda = calculate_macd(df_moeda.copy())
        fig_macd = px.line(df_moeda, x='tempo', y=['MACD', 'MACD_signal', 'MACD_line'], title='Divergência de Convergência de Média Móvel (MACD)')
        st.plotly_chart(fig_macd)

        # Indicadores Personalizados
        st.subheader('Indicadores Personalizados')
        formula_indicador = st.text_input('Insira a Fórmula do Indicador (Utilize nomes de colunas do DataFrame):')

        if formula_indicador:
            try:
                novo_indicador = eval(formula_indicador)
                df_moeda['novo_indicador'] = novo_indicador
                st.success('Indicador personalizado criado com sucesso!')
                # Plot do novo indicador
                fig_indicador = px.line(df_moeda, x='tempo', y=['fechamento', 'novo_indicador'], title='Indicador Personalizado')
                st.plotly_chart(fig_indicador)
            except Exception as e:
                st.error(f'Erro ao criar indicador: {e}')

    # Análise de Volume
    elif tipo_analise == 'Volume':
        fig_volume = px.bar(df, x='tempo', y='volume', title='Volume de Negociação ao Longo do Tempo')
        st.plotly_chart(fig_volume)

    # Análise de Preço
    elif tipo_analise == 'Preço':
        st.subheader('Distribuição de Preços')
        fig_hist = px.histogram(df, x='fechamento', title='Distribuição de Preços')
        st.plotly_chart(fig_hist)

    # Análise de Volatilidade
    elif tipo_analise == 'Volatilidade':
        df['mudanca_pct'] = df['fechamento'].pct_change() * 100
        fig_volatilidade = px.line(df, x='tempo', y='mudanca_pct', title='Mudança Percentual Diária')
        st.plotly_chart(fig_volatilidade)

# Página Sobre
if escolha == 'Sobre':
    st.write("""
        ## Sobre a Dashboard Avançada de Análise de Criptomoedas

        Esta dashboard foi criada para auxiliar entusiastas de criptomoedas e investidores na análise de dados e identificação de oportunidades no mercado.

        **Funcionalidades:**

        * Visualização de preços de criptomoedas
        * Cálculo de indicadores técnicos (SMA, RSI, MACD)
        * Análise de correlação entre moedas e indicadores
        * Criação de indicadores personalizados
        * Análise de sentimento de notícias
        * Monitoramento de preços e alertas
        * Interface personalizável e intuitiva

        **Desenvolvimento:**

        A dashboard foi desenvolvida com as seguintes tecnologias:

        * Streamlit: framework para criação de interfaces interativas com Python
        * Pandas: biblioteca para manipulação e análise de dados
        * Plotly Express: biblioteca para criação de gráficos interativos
        * Numpy: biblioteca para operações matemáticas com arrays
        * Matplotlib: biblioteca para criação de gráficos estáticos
        * Requests: biblioteca para realizar requisições HTTP
        * NLTK: biblioteca para processamento de linguagem natural
        * TextBlob: biblioteca para análise de sentimento de texto

        **Contribuições:**

        Esta dashboard é um projeto em constante desenvolvimento. Se você tiver sugestões, feedback ou quiser contribuir com o código, entre em contato.

        **Agradecimentos:**

        Agradecemos a todos que contribuíram para o desenvolvimento desta dashboard.
        """)

# Execução da Dashboard
if __name__ == '__main__':
    st.run()
