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

@st.cache_data
def variavel_media(empresa,variavel,inicio,fim):
    inicio = pd.to_datetime(inicio)
    fim = pd.to_datetime(fim)
    filtro_temporal = data[(data['facility_name'] == empresa) & (data['year_month'] >= inicio) & (data['year_month'] <= fim)]
    filtro_temporal = filtro_temporal[variavel]

    return round(filtro_temporal.mean(skipna=True),2)


def main():

    st.write('# Indicadores operacionais em plantas industriais')
    st.sidebar.title('Menu de navegação')
    inicio = st.sidebar.date_input('### Início da série', min_value=date(2010, 1, 1), max_value=None)
    fim = st.sidebar.date_input('### Fim da série', min_value=date(2010, 1, 1), max_value=None)
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
       
        try:
            col1, col2 = st.columns(2)
            somatorio_lucro = variavel_agreg_periodo(facility_escolhida,'gross_profit',inicio,fim)
            somatorio_ebitda = variavel_agreg_periodo(facility_escolhida,'ebitda',inicio,fim)
            somatorio_lucro_liquido = variavel_agreg_periodo(facility_escolhida,'net_income',inicio,fim)
            somatorio_receita = variavel_agreg_periodo(facility_escolhida,'revenue',inicio,fim)

            oee_medio = variavel_media(facility_escolhida,'oee_pct',inicio,fim)
            margem_ebitda_media = variavel_media(facility_escolhida,'ebitda_margin_pct',inicio,fim)

            fig_oee = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = oee_medio,
                    gauge = {"axis": {"range":[0,100]}},
                    title = {'text': "OEE Médio (%)"}))
            
            fig_margem_ebitda = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = margem_ebitda_media,
                    gauge = {"axis": {"range":[0,100]}},
                    title = {'text': "Margem EBITDA(%)"}))

            col1.metric(label=f'Lucro bruto (em milhares)', value=f'US$ {somatorio_lucro}', border=True)
            col1.metric(label=f'Receita (em milhares)', value=f'USS {somatorio_receita}', border=True)
            col1.plotly_chart(fig_oee, use_container_width=True)
            col2.metric(label=f'Lucro líquido (em milhares', value=f'US$ {somatorio_lucro_liquido}', border=True)
            col2.metric(label=f'EBITDA (em milhares)', value=f'US$ {somatorio_ebitda}', border=True)
            col2.plotly_chart(fig_margem_ebitda, use_container_width=True)

        except:
            pass

if __name__ == "__main__":
    main()