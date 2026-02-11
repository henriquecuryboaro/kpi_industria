import pandas as pd
import streamlit as st
from pathlib import Path
from datetime import datetime, date
import plotly.express as px
import plotly.graph_objects as go

## Título da página,layout
st.set_page_config(page_title="Dashb",layout="wide")

#Import dataset
COMPLETE_PATH = Path(__file__).resolve().parent / 'chemical_industry_kpis_complete_expanded_consistent.csv'

@st.cache_data
def load_data(path_df):
    return pd.read_csv(path_df)

data = load_data(COMPLETE_PATH)

#Separar variáveis por tipo (Categórico ou numérico)
def SeparaTipo(data):
    num_cols = data.select_dtypes(include = ['int64', 'float64']).columns
    cat_cols = data.select_dtypes(exclude = ['int64', 'float64']).columns
    var_numericas, var_categoricas = [column for column in num_cols], [column for column in cat_cols]
    return num_cols, cat_cols, var_numericas, var_categoricas

num_cols, cat_cols, var_numericas, var_categoricas = SeparaTipo(data)

#listas de empreendimentos e de métricas quantitativas utilizáveis como KPIs
facilities_list = data['facility_name'].unique().tolist()
kpi_lista = var_numericas
indicadores_para_somatorios = ['downtime_hours','production_volume_tons','gross_profit','net_income']

#converter data em formato string para 'datetime'
# definir formato
format_string = "%Y-%m-%d"

# converter
for i in range(len(data)):
    data.iloc[i,2] = datetime.strptime(data.iloc[i,2], format_string)

@st.cache_data
def variavel_agreg_periodo(empresa,variavel,inicio,fim):
    inicio = pd.to_datetime(inicio)
    fim = pd.to_datetime(fim)
    filtro_temporal = data[(data['facility_name'] == empresa) & (data['year_month'] >= inicio) & (data['year_month'] <= fim)]
    filtro_temporal = filtro_temporal[variavel]

    return round(filtro_temporal.sum(skipna=True),2)

def main():

    st.write('# Painel de indicadores operacionais de indústrias químicas')
    st.sidebar.title('Menu de navegação')
    inicio = st.sidebar.date_input('### Início da série', min_value=date(2010, 1, 1), max_value=None)
    fim = st.sidebar.date_input('### Fim da série', min_value=date(2026, 12, 31), max_value=None)
    facility_escolhida = st.sidebar.selectbox('Escolha a planta',sorted(facilities_list), index=None, placeholder='Plantas', key=f'planta')

    col1,col2 = st.columns(2)
    con1 = col1.container(key='comp_1')
    con2 = col2.container(key='comp_2')

    with con1:
        kpi_escolhida = st.selectbox('Escolha o KPI',sorted(kpi_lista), index=None, placeholder='Indicadores', key=f'indicador')

        try:
            data_facility = data[data['facility_name'] == facility_escolhida]
            fig = px.scatter(
                data_facility,
                x=f'{kpi_escolhida}',
                y='ebitda',
                trendline="ols",
                title=f'Relação: {kpi_escolhida} x EBITDA',
            )

            st.plotly_chart(fig)
        except:
            pass

    with con2:
        variavel_somar = st.selectbox('Esolha indicador',sorted(indicadores_para_somatorios),index=None,placeholder='Indicadores',key='indicador_soma')
        
        try:
            soma_obtida = variavel_agreg_periodo(facility_escolhida,variavel_somar,inicio,fim)
            st.metric(label=f'Somatório de {variavel_somar}', value=soma_obtida, border=True)
        except:
            pass

if __name__ == "__main__":
    main()