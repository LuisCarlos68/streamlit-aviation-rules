import streamlit as st  
import pandas as pd  
import plotly.express as px  
  
# Configuração da página  
st.set_page_config(page_title="Consulta de Regras de Associação", layout="wide")  
  
# Título e descrição  
st.title("📊 Consulta de Regras de Associação - Segurança na Aviação")  
st.markdown("""  
Esta ferramenta permite consultar e analisar regras de associação relacionadas a ocorrências na aviação.  
Selecione o tipo de ocorrência e utilize os filtros para encontrar as regras mais relevantes.  
""")  
  
# Carregar os dados  
@st.cache_data  
def load_data():  
    df_acidente = pd.read_excel('regras_associacao_acidente.xlsx', engine='openpyxl')  
    df_incidente = pd.read_excel('regras_associacao_incidente.xlsx', engine='openpyxl')  
    df_incidente_grave = pd.read_excel('regras_associacao_incidente_grave.xlsx', engine='openpyxl')  
    df_todas = pd.read_excel('regras_associacao_todas_variaveis.xlsx', engine='openpyxl')  
    return df_acidente, df_incidente, df_incidente_grave, df_todas  
  
try:  
    df_acidente, df_incidente, df_incidente_grave, df_todas = load_data()  
      
    # Seletor de tipo de ocorrência  
    tipo_ocorrencia = st.selectbox(  
        "Selecione o tipo de ocorrência",  
        ["Acidente", "Incidente", "Incidente Grave", "Todas as Variáveis"]  
    )  
      
    # Mostrar dados baseado na seleção  
    if tipo_ocorrencia == "Todas as Variáveis":  
        df = df_todas  
    elif tipo_ocorrencia == "Acidente":  
        df = df_acidente  
    elif tipo_ocorrencia == "Incidente Grave":  
        df = df_incidente_grave  
    else:  
        df = df_incidente  
      
    # Adicionar filtros  
    col1, col2, col3 = st.columns(3)  
    with col1:  
        min_support = st.slider("Suporte Mínimo", 0.0, float(df['support'].max()), 0.0)  
    with col2:  
        min_confidence = st.slider("Confiança Mínima", 0.0, float(df['confidence'].max()), 0.0)  
    with col3:  
        min_lift = st.slider("Lift Mínimo", 0.0, float(df['lift'].max()), 0.0)  
      
    # Filtrar dados  
    df_filtered = df[  
        (df['support'] >= min_support) &  
        (df['confidence'] >= min_confidence) &  
        (df['lift'] >= min_lift)  
    ]  
      
    # Mostrar dados filtrados  
    st.dataframe(df_filtered)  
      
    # Visualizações  
    if not df_filtered.empty:  
        st.subheader("📊 Visualizações")  
          
        col1, col2 = st.columns(2)  
          
        with col1:  
            # Histograma do Lift  
            fig_lift = px.histogram(  
                df_filtered,  
                x="lift",  
                title="Distribuição do Lift",  
                labels={"lift": "Valor do Lift", "count": "Frequência"}  
            )  
            st.plotly_chart(fig_lift)  
              
        with col2:  
            # Scatter plot  
            fig_scatter = px.scatter(  
                df_filtered,  
                x="support",  
                y="confidence",  
                size="lift",  
                title="Relação entre Suporte e Confiança",  
                labels={  
                    "support": "Suporte",  
                    "confidence": "Confiança",  
                    "lift": "Lift"  
                }  
            )  
            st.plotly_chart(fig_scatter)  
      
except Exception as e:  
    st.error(f"Erro ao carregar os dados: {str(e)}")  
    st.info("Verifique se todos os arquivos necessários estão presentes no diretório.")  