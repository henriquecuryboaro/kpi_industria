import pandas as pd
import streamlit as st
from pathlib import Path

#Import dataset
FACILITIES_PATH = Path(__file__).resolve().parent / 'chemical_facilities.csv'
COMPLETE_PATH = Path(__file__).resolve().parent / 'chemical_industry_kpis_complete.csv'
COMPLETE_PATH_EXPANDED = Path(__file__).resolve().parent / 'chemical_industry_kpis_complete_expanded.csv'
MONTHLY_PATH = Path(__file__).resolve().parent / 'chemical_monthly_operations.csv'

@st.cache_data
def load_data(path_df):
    return pd.read_csv(path_df)

data = load_data(COMPLETE_PATH)
expanded_data = load_data(COMPLETE_PATH_EXPANDED)
facilities_df = load_data(FACILITIES_PATH)
monthly_df = load_data(MONTHLY_PATH)

print(expanded_data.describe())
print(data.describe())