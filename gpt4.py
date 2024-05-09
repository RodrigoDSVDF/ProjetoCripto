import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import timedelta
import base64
from io import BytesIO

# Importar módulo com funções de cálculo dos indicadores
from modulocripto import calculate_moving_averages, calculate_rsi, calculate_macd

# Função de caching para carregar dados
@st.cache_data
def importar_dados():
    df = pd.read_csv('dadosdf_cripto.csv')
    df['tempo'] = pd.to_datetime(df['tempo'])
    return df

df = importar_dados()

# Função para exportar DataFrame para Excel
def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False)
    writer.save()
    processed_data = output.getvalue()
    return processed_data

def get_table_download_link(df):
    val = to_excel(df)
    b64 = base64.b64encode(val)  # B64 encoded
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="extract.xlsx">Download Excel file</a>'

# Sistema de Alertas
if 'alertas' not in st.session_state:
    st.session_state['alertas'] = []

st.sidebar.header("Configurar Alertas")
tipo_alerta = st.sidebar.selectbox("Tipo de Alerta", ["Preço acima", "Preço abaixo", "Mudança percentual"])
valor_alerta = st.sidebar.number_input("Definir Valor", step=0.01)
moeda_alerta = st.sidebar.selectbox("Selecione a Moeda", df['moeda'].unique())
if st.sidebar.button("Adicionar Alerta"):
    st.session_state['alertas'].append((tipo_alerta, valor_alerta, moeda_alerta))
    st.sidebar.success("Alerta adicionado!")

st.sidebar.subheader("Alertas Ativos")
for alerta in st.session_state['alertas']:
    st.sidebar.text(f"{alerta[0]} {alerta[1]} - {alerta[2]}")

# Título da Aplicação
st.title('Análises de Cripto Moedas')
st.sidebar.header('Menu')

opcoes = ['Home', 'Visualização', 'Análise', 'Sobre']
escolha = st.sidebar.selectbox("Escolha uma opção", opcoes)

if escolha == 'Home':
    st.subheader('Bem-vindo à Dashboard de Análise de Criptomoedas')
    st.write("Aqui você pode encontrar informações valiosas e análises detalhadas que podem ajudar a orientar suas decisões de investimento em criptomoedas.")

elif escolha == 'Visualização':
    st.subheader('Visualização de Dados')
    criptomoedas = df['moeda'].unique()
    moeda_selecionada = st.selectbox('Selecione uma Moeda para Visualização:', criptomoedas)

    if st.button(f'Visualizar Gráfico para {moeda_selecionada}'):
        df_moeda = df[df['moeda'] == moeda_selecionada]
        fig = px.line(df_moeda, x='tempo', y='fechamento', title=f'Preço de Fechamento ao Longo do Tempo para {moeda_selecionada}')
        st.plotly_chart(fig)
        st.markdown(get_table_download_link(df_moeda), unsafe_allow_html=True)

elif escolha == 'Análise':
    st.subheader('Análise de Correlação e Indicadores de Mercado')
    criptomoedas = df['moeda'].unique()
    moeda_selecionada = st.selectbox('Selecione uma Moeda para Análise Detalhada:', criptomoedas)
    df_moeda = df[df['moeda'] == moeda_selecionada]

    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["Correlação Geral", "Médias Móveis", "RSI", "MACD", "Volume de Negociação", "Preço de Fechamento (Últimos 20 Dias)", "Volatilidade Percentual"])
    
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

    with tab7:
        st.subheader('Volatilidade Percentual')
        volatilidade = []
        for moeda in criptomoedas:
            df_moeda = df[df['moeda'] == moeda]
            volatilidade.append((moeda, (df_moeda['fechamento'].max() - df_moeda['fechamento'].min()) / df_moeda['fechamento'].min() * 100))
        df_volatilidade = pd.DataFrame(volatilidade, columns=['Moeda', 'Volatilidade Percentual'])
        df_volatilidade['Volatilidade Percentual'] = df_volatilidade['Volatilidade Percentual'].apply(lambda x: '{:.2f}%'.format(x))
        fig = px.bar(df_volatilidade, x='Moeda', y='Volatilidade Percentual', title='Volatilidade Percentual para Todas as Moedas')
        st.plotly_chart(fig)

elif escolha == 'Sobre':
    st.write("""
    ## Sobre a Dashboard de Análise de Criptomoedas
    Esta dashboard foi criada para auxiliar entusiastas de criptomoedas e investidores na análise de dados e identificação de oportunidades no mercado.
    """)


