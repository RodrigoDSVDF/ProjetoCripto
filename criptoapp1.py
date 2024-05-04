import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import timedelta
from modulocripto import calculate_moving_averages, calculate_rsi, calculate_macd

# Carregar dados
@st.cache_data
def importar_dados():
    df = pd.read_csv('dadosdf_cripto.csv')
    df['tempo'] = pd.to_datetime(df['tempo'])
    return df

df = importar_dados()


# Interface
st.title('Análises de Cripto Moedas')
st.sidebar.header('Menu')

opcoes = ['Home', 'Visualização', 'Análise', 'Sobre']
escolha = st.sidebar.selectbox("Escolha uma opção", opcoes)

if escolha == 'Visualização':
    st.subheader('Visualização de Dados')
    criptomoedas = df['moeda'].unique()
    moeda_selecionada = st.selectbox('Selecione uma Moeda para Visualização:', criptomoedas)

    if st.button(f'Visualizar Gráfico para {moeda_selecionada}'):
        df_moeda = df[df['moeda'] == moeda_selecionada]
        fig = px.line(df_moeda, x='tempo', y='fechamento', title=f'Preço de Fechamento ao Longo do Tempo para {moeda_selecionada}')
        st.plotly_chart(fig)

if escolha == 'Análise':
    st.subheader('Análise de Correlação e Indicadores de Mercado')
    criptomoedas = df['moeda'].unique()
    moeda_selecionada = st.selectbox('Selecione uma Moeda para Análise Detalhada:', criptomoedas)

    if st.button(f'Analisar {moeda_selecionada}'):
        df_moeda = df[df['moeda'] == moeda_selecionada]
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Correlação Geral", "Médias Móveis", "RSI", "MACD", "Volume de Negociação", "Preço de Fechamento (Últimos 20 Dias)"])

        with tab1:
            fig = px.scatter(df_moeda, x='volume', y='fechamento', trendline="ols",
                             labels={'volume': 'Volume de Negociação', 'fechamento': 'Preço de Fechamento'},
                             title=f'Correlação entre Volume e Preço de Fechamento para {moeda_selecionada}')
            st.plotly_chart(fig)

        with tab2:
            df_moeda = calculate_moving_averages(df_moeda.copy())
            fig = px.line(df_moeda, x='tempo', y=['fechamento', 'SMA'],
                          labels={'value': 'Preço', 'variable': 'Indicadores'},
                          title=f'Médias Móveis para {moeda_selecionada}')
            st.plotly_chart(fig)

        with tab3:
            df_moeda = calculate_rsi(df_moeda.copy())
            fig = px.line(df_moeda, x='tempo', y='RSI', title=f'RSI para {moeda_selecionada}')
            st.plotly_chart(fig)

        with tab4:
            df_moeda = calculate_macd(df_moeda.copy())
            fig = px.line(df_moeda, x='tempo', y=['MACD_line', 'MACD_signal'],
                          labels={'value': 'MACD', 'variable': 'Linhas MACD'},
                          title=f'MACD para {moeda_selecionada}')
            st.plotly_chart(fig)

        with tab5:
            volume_fig = px.bar(df_moeda, x='tempo', y='volume', title='Volume de Negociação ao Longo do Tempo')
            st.plotly_chart(volume_fig)

        with tab6:
            df_recente = df_moeda[df_moeda['tempo'] > (df_moeda['tempo'].max() - timedelta(days=20))]
            close_fig = px.line(df_recente, x='tempo', y='fechamento', title='Preço de Fechamento dos Últimos 20 Dias')
            st.plotly_chart(close_fig)
