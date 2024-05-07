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

if escolha == 'Home':
    st.subheader('Bem-vindo à Dashboard de Análise de Criptomoedas')
    st.write("""
    Aqui você pode encontrar informações valiosas e análises detalhadas que podem ajudar a orientar suas decisões de investimento em criptomoedas.
    """)
    url_da_imagem = 'https://images.unsplash.com/photo-1516245834210-c4c142787335?q=80&w=1469&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'
    st.image(url_da_imagem, use_column_width=True)

elif escolha == 'Visualização':
    st.subheader('Visualização de Dados')
      
    url_da_imagem = 'imagem.jpeg'
    st.image(url_da_imagem, use_column_width=True)
    
    criptomoedas = df['moeda'].unique()
    moeda_selecionada = st.selectbox('Selecione uma Moeda para Visualização:', criptomoedas)
   
    st.write("")  # Separador opcional para melhor layout

    if st.button(f'Visualizar Gráfico para {moeda_selecionada}'):
        df_moeda = df[df['moeda'] == moeda_selecionada]
        fig = px.line(df_moeda, x='tempo', y='fechamento', title=f'Preço de Fechamento ao Longo do Tempo para {moeda_selecionada}')
        st.plotly_chart(fig)

elif escolha == 'Análise':
    st.subheader('Análise de Correlação e Indicadores de Mercado')
    criptomoedas = df['moeda'].unique()
    moeda_selecionada = st.selectbox('Selecione uma Moeda para Análise Detalhada:', criptomoedas)
    if st.button(f'Analisar {moeda_selecionada}'):
        df_moeda = df[df['moeda'] == moeda_selecionada]
        tabs = st.tabs(["Correlação Geral", "Médias Móveis", "RSI", "MACD", "Volume de Negociação", "Preço de Fechamento (Últimos 30 Dias)", "Volatilidade Percentual"])
        
        with tabs[0]:
            fig = px.scatter(df_moeda, x='volume', y='fechamento', trendline="ols")
            st.plotly_chart(fig)
        
        with tabs[1]:
            df_moeda = calculate_moving_averages(df_moeda.copy())
            fig = px.line(df_moeda, x='tempo', y=['fechamento', 'SMA'])
            st.plotly_chart(fig)
        
        with tabs[2]:
            df_moeda = calculate_rsi(df_moeda.copy())
            fig = px.line(df_moeda, x='tempo', y='RSI')
            st.plotly_chart(fig)
        
        with tabs[3]:
            df_moeda = calculate_macd(df_moeda.copy())
            fig = px.line(df_moeda, x='tempo', y=['MACD_line', 'MACD_signal'])
            st.plotly_chart(fig)
        
        with tabs[4]:
            volume_fig = px.bar(df_moeda, x='tempo', y='volume')
            st.plotly_chart(volume_fig)
        
        with tabs[5]:
            df_recente = df_moeda[df_moeda['tempo'] > (df_moeda['tempo'].max() - timedelta(days=30))]
            close_fig = px.line(df_recente, x='tempo', y='fechamento')
            st.plotly_chart(close_fig)
        
        with tabs[6]:
            volatilidade = []
            for moeda in criptomoedas:
                df_moeda_temp = df[df['moeda'] == moeda]
                volatilidade.append((moeda, (df_moeda_temp['fechamento'].max() - df_moeda_temp['fechamento'].min()) / df_moeda_temp['fechamento'].min() * 100))
            df_volatilidade = pd.DataFrame(volatilidade, columns=['Moeda', 'Volatilidade Percentual'])
            fig = px.bar(df_volatilidade, x='Moeda', y='Volatilidade Percentual', title='Volatilidade Percentual para Todas as Moedas')
            st.plotly_chart(fig)
