import pandas as pd
import streamlit as st
from pathlib import Path
from datetime import datetime, date
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

## Título da página,layout
st.set_page_config(page_title="Painel - KPIs industriais",layout="wide")

#Import dataset
COMPLETE_PATH = Path(__file__).resolve().parent / 'chemical_industry_kpis_complete_expanded_v3.csv'

@st.cache_data
def load_data(path_df):
    return pd.read_csv(path_df)

data = load_data(COMPLETE_PATH)

#remove linhas que apresentavam lucro líquido zero, valor inconsistente
data = data[data['net_income'] != 0]

#Correção de atributos 
data['ebitda_margin_pct'] = 100*(data['ebitda']/data['revenue'])
data['quality_pct'], data['availability_pct'], data['performance_pct']  = 100*(data['quality_pct']/data['quality_pct'].max()), 100*(data['availability_pct']/data['availability_pct'].max()), 100*(data['performance_pct']/data['performance_pct'].max())
data['oee_pct'] = (data['performance_pct']*data['availability_pct']*data['quality_pct'])/10000

#Separar variáveis por tipo (Categórico ou numérico)
def SeparaTipo(data):
    num_cols = data.select_dtypes(include = ['int64', 'float64']).columns
    cat_cols = data.select_dtypes(exclude = ['int64', 'float64']).columns
    var_numericas, var_categoricas = [column for column in num_cols], [column for column in cat_cols]
    return num_cols, cat_cols, var_numericas, var_categoricas

num_cols, cat_cols, var_numericas, var_categoricas = SeparaTipo(data)

#listas de empreendimentos
facilities_list = data['facility_name'].unique().tolist()

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

@st.cache_data
def ebitda_mensal_grafico(empresa,inicio,fim):
    data_facility = data[(data['facility_name'] == empresa) & (data['year_month'] >= (pd.to_datetime(inicio))) & (data['year_month'] <= (pd.to_datetime(fim)))]

    if data_facility.empty:
        st.info("Selecione dados no menu de navegação ao lado para que indicadores sejam exibidos")
        return None

    max_value = max(data_facility['ebitda'])
    fig = px.bar(data_facility, x='year_month',y='ebitda', range_y=[(0.8*max_value),(1.05*max_value)], labels={'year_month':'Período', 'capacity_utilization_pct':'EBITDA mensal'})
    
    fig.update_layout(yaxis=dict(title='EBITDA mensal',tickprefix="US$", tickformat=",.2f"), title_text='Valores mensais de EBITDA')

    return fig

@st.cache_data
def capacidade_mensal_grafico(empresa,inicio,fim):
    data_facility = data[(data['facility_name'] == empresa) & (data['year_month'] >= (pd.to_datetime(inicio))) & (data['year_month'] <= (pd.to_datetime(fim)))]

    if data_facility.empty:
        st.info("Selecione dados no menu de navegação ao lado para que indicadores sejam exibidos")
        return None

    max_value = max(data_facility['capacity_utilization_pct'])
    fig = px.bar(data_facility,x='year_month',y='capacity_utilization_pct',range_y=[(0.8*max_value),(1.05*max_value)], labels={'year_month':'Período', 'capacity_utilization_pct':'Capacidade'})

    fig.update_layout(yaxis=dict(title='Utilização da capacidade por mês',ticksuffix="%", tickformat=",.2f"), title_text='Valores mensais da utilização da capacidade da planta')

    return fig

@st.cache_data
def oee_mensal_grafico(empresa,inicio,fim):
    data_facility = data[(data['facility_name'] == empresa) & (data['year_month'] >= (pd.to_datetime(inicio))) & (data['year_month'] <= (pd.to_datetime(fim)))]

    if data_facility.empty:
        st.info("Selecione dados no menu de navegação ao lado para que indicadores sejam exibidos")
        return None

    max_value = max(data_facility['oee_pct'])
    fig = px.bar(data_facility,x='year_month',y='oee_pct',range_y=[(0.7*max_value),(1.05*max_value)], labels={'year_month':'Período', 'oee_pct':'OEE'})

    fig.update_layout(yaxis=dict(title='OEE (%)',ticksuffix="%", tickformat=",.2f"), title_text='OEE mensal')

    return fig

@st.cache_data
def inatividade_mensal_grafico(empresa,inicio,fim):
    data_facility = data[(data['facility_name'] == empresa) & (data['year_month'] >= (pd.to_datetime(inicio))) & (data['year_month'] <= (pd.to_datetime(fim)))]

    if data_facility.empty:
        st.info("Selecione dados no menu de navegação ao lado para que indicadores sejam exibidos")
        return None

    max_value = max(data_facility['downtime_hours'])
    fig = px.bar(data_facility,x='year_month',y='downtime_hours', range_y=[(0.8*max_value),(1.05*max_value)], labels={'year_month':'Período', 'downtime_hours':'Inatividade'})

    fig.update_layout(yaxis=dict(title='Inatividade (h)', tickformat=",.2f"), title_text='Horas de inatividade por mês')

    return fig

def main():

    st.write('# Indicadores operacionais e financeiros em plantas industriais')
    st.sidebar.title('Menu de navegação')

    tab1,tab2 = st.tabs(['Natureza operacional','Natureza financeira'])

    inicio = st.sidebar.date_input('### Início da série', min_value=date(2010, 1, 1), max_value=date(2026, 1, 31))
    fim = st.sidebar.date_input('### Fim da série', min_value=date(2010, 1, 1), max_value=date(2026, 1, 31))
    facility_escolhida = st.sidebar.selectbox('Escolha a planta',sorted(facilities_list), index=None, placeholder='Plantas', key=f'planta')

    with tab1:

        st.markdown(
                        """
                        <style>
                        .centered-text {
                            text-align: center;
                            font-size: 28px;
                        }
                        </style>
                        <div class="centered-text">
                            <strong>Indicadores de natureza operacional</strong>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )        
      
        try:
            with st.container(border=True):           
                oee_medio = round(variavel_media(facility_escolhida,'oee_pct',inicio,fim),2)
                qualidade_medio = variavel_media(facility_escolhida,'quality_pct',inicio,fim)
                disponibilidade_medio = variavel_media(facility_escolhida,'availability_pct',inicio,fim)
                performance_medio = variavel_media(facility_escolhida,'performance_pct',inicio,fim)
                fig_oee = go.Figure(go.Indicator(
                        mode = "gauge+number",
                        value = oee_medio,
                        gauge = {"axis": {"range":[0,100]}},
                        title = {'text': "OEE Médio (%)"}))
                
                fig_oee.update_layout(
                                autosize=False,
                                width=540, 
                                height=360, 
                                margin=dict(l=50, r=50, b=100, t=100, pad=4)
                            )
                col1,col2 = st.columns(2)
                col1.plotly_chart(fig_oee, use_container_width=True)
                col2.metric(label=f'Qualidade (valor médio)', value=f'{qualidade_medio}%', border=True)
                col2.metric(label=f'Disponibilidade (valor médio)', value=f'{disponibilidade_medio}%', border=True)
                col2.metric(label=f'Performance (valor médio)', value=f'{performance_medio}%', border=True)
                oee_mensal_plot = oee_mensal_grafico(facility_escolhida,inicio,fim)                  
                st.plotly_chart(oee_mensal_plot)
            
                col1,col2 = st.columns(2)
                con1 = col1.container(key='comp_1',border=True)
                con2 = col2.container(key='comp_2', border=True)
                fig_capacidade = capacidade_mensal_grafico(facility_escolhida,inicio,fim)
                con1.plotly_chart(fig_capacidade)
                fig_inatividade = inatividade_mensal_grafico(facility_escolhida,inicio,fim)
                con2.plotly_chart(fig_inatividade)
                
                col1,col2,col3 = st.columns(3)
                con1 = col1.container(key='comp_pt')
                con2 = col2.container(key='comp_ppe')
                con3 = col3.container(key='comp_ept')
                producao_total = variavel_agreg_periodo(facility_escolhida,'production_volume_tons',inicio,fim)
                con1.metric(label=f'Volume total de produção (toneladas)', value=f'{producao_total}', border=True)
                ppe_media = variavel_media(facility_escolhida,'production_per_employee',inicio,fim)
                con2.metric(label=f'Média de produção por empregado (tonelada/empregado)', value=f'{ppe_media}', border=True)
                ept_media = variavel_media(facility_escolhida,'energy_per_ton_mwh',inicio,fim)
                con3.metric(label=f'Energia consumida por unidade (MWh/tonelada)', value=f'{ept_media}', border=True)

        except:
            pass

    with tab2:
       
        st.markdown(
            """
            <style>
            .centered-text {
                text-align: center;
                font-size: 28px;
            }
            </style>
            <div class="centered-text">
                <strong>Indicadores para análise financeira da operação</strong><br><br>
            </div>
            """,
            unsafe_allow_html=True
        )
    
        try:
            
            somatorio_lucro = variavel_agreg_periodo(facility_escolhida,'gross_profit',inicio,fim)
            somatorio_ebitda = variavel_agreg_periodo(facility_escolhida,'ebitda',inicio,fim)
            somatorio_lucro_liquido = variavel_agreg_periodo(facility_escolhida,'net_income',inicio,fim)
            somatorio_receita = variavel_agreg_periodo(facility_escolhida,'revenue',inicio,fim)
            min_ev = 7*(variavel_agreg_periodo(facility_escolhida,'ebitda','2025-01-01','2025-12-31'))
            max_ev = 10*(variavel_agreg_periodo(facility_escolhida,'ebitda','2025-01-01','2025-12-31'))
            margem_ebitda_media = variavel_media(facility_escolhida,'ebitda_margin_pct',inicio,fim)
        
            with st.container(border=True):
                st.markdown(
                    """
                    <style>
                    .centered-text {
                        text-align: center;
                        font-size: 28px;
                    }
                    </style>
                    <div class="centered-text">
                        Estimativa de valor de mercado da planta baseada em múltiplos de EBITDA (acumulado do ano de 2025)<br>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                st.metric(label=f'Menor estimativa esperada para valor de mercado (em milhares) - Sete múltiplos', value=f'US$ {round(min_ev,2)}', border=True)
                st.metric(label=f'Maior estimativa esperada para valor de mercado (em milhares) - Dez múltiplos', value=f'US$ {round(max_ev,2)}', border=True)
            
            st.write('#### Indicadores financeiros relativos ao período escolhido')
            col1, col2 = st.columns(2)
            fig_ebitda = ebitda_mensal_grafico(facility_escolhida,inicio,fim)
            st.plotly_chart(fig_ebitda)
            col1.metric(label=f'Lucro bruto acumulado (em milhares)', value=f'US$ {somatorio_lucro}', border=True)
            col1.metric(label=f'Receita acumulada (em milhares)', value=f'US$ {somatorio_receita}', border=True)            
            col2.metric(label=f'Lucro líquido acumulado (em milhares)', value=f'US$ {somatorio_lucro_liquido}', border=True)
            col2.metric(label=f'EBITDA acumulado (em milhares)', value=f'US$ {somatorio_ebitda}', border=True)
            st.metric(label=f'Margem EBITDA', value=f'{margem_ebitda_media}%', border=True)

        except:
            pass

if __name__ == "__main__":
    main()