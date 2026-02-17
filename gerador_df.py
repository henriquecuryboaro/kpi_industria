import pandas as pd
import numpy as np
import random

# 1. Carregar estrutura original para mapear colunas e tipos
df_original = pd.read_csv('chemical_industry_kpis_complete.csv')
columns = df_original.columns

# 2. Definir Facilities Reais (para manter a relação 1:1)
facilities = [
    {"id": "B0-FF001", "name": "Refinery Alpha", "loc": "Houston, USA", "type": "Petrochemical"},
    {"id": "B0-FF005", "name": "Zenith Industrial Gases Center", "loc": "Shanghai, China", "type": "Industrial Gases"},
    {"id": "B0-FF009", "name": "Titanium Polymers Plant", "loc": "Frankfurt, Germany", "type": "Polymers"},
    {"id": "B0-FF012", "name": "Amazonas Bio-Chem", "loc": "Manaus, Brazil", "type": "Agro-Chemicals"},
    {"id": "B0-FF015", "name": "Nordic Specialty Acids", "loc": "Oslo, Norway", "type": "Specialty Chemicals"}
]

n_rows = 1500
data = []

for i in range(n_rows):
    f = random.choice(facilities)
    
    # Produção e Eficiência
    prod_vol = np.random.uniform(30000, 80000)
    capacity_util = np.random.uniform(60, 98)
    yield_rate = np.random.uniform(85, 99)
    oee = np.random.uniform(75, 100)
    quality = np.random.uniform(75, 100)
    
    # Financeiro (Garantindo que não sejam zero)
    revenue = prod_vol * np.random.uniform(0.7, 1.2)
    raw_mat_costs = revenue * np.random.uniform(0.4, 0.5)
    labor_costs = np.random.uniform(4000, 6000)
    energy_costs = np.random.uniform(1500, 3000)
    maint_costs = np.random.uniform(800, 1500)
    
    cogs = raw_mat_costs + labor_costs + energy_costs
    gross_profit = revenue - cogs
    op_expenses = np.random.uniform(5000, 8000)
    ebitda = gross_profit - (op_expenses * 0.4)
    depreciation = np.random.uniform(500, 1000)
    ebit = ebitda - depreciation
    net_income = ebit * 0.75 # Simulando desconto de taxas
    
    # Sustentabilidade
    energy_cons = np.random.uniform(1000, 5000)
    water_usage = np.random.uniform(8000, 20000)
    waste = np.random.uniform(50, 200)

    row = {
        "record_id": f"REC-{2024}-{i:04d}",
        "facility_id": f["id"],
        "year_month": f"2024-{random.randint(1,12):02d}",
        "production_volume_tons": round(prod_vol, 2),
        "capacity_utilization_pct": round(capacity_util, 2),
        "yield_rate_pct": round(yield_rate, 2),
        "downtime_hours": round(np.random.uniform(2, 20), 1),
        "quality_defect_rate_pct": round(100 - quality, 2),
        "batch_success_rate_pct": round(np.random.uniform(90, 100), 2),
        "safety_incidents": random.randint(0, 2),
        "environmental_violations": random.choice([0, 0, 0, 1]),
        "energy_consumption_mwh": round(energy_cons, 2),
        "water_usage_cubic_meters": round(water_usage, 2),
        "waste_generated_tons": round(waste, 2),
        "revenue": round(revenue, 2),
        "cost_of_goods_sold": round(cogs, 2),
        "raw_material_costs": round(raw_mat_costs, 2),
        "labor_costs": round(labor_costs, 2),
        "energy_costs": round(energy_costs, 2),
        "maintenance_costs": round(maint_costs, 2),
        "depreciation": round(depreciation, 2),
        "operating_expenses": round(op_expenses, 2),
        "interest_expense": round(np.random.uniform(100, 300), 2),
        "tax_expense": round(ebit * 0.2, 2),
        "facility_name": f["name"],
        "location": f["loc"],
        "facility_type": f["type"],
        "capacity_tons_per_year": 1000000,
        "employees": random.randint(100, 500),
        "gross_profit": round(gross_profit, 2),
        "gross_margin_pct": round((gross_profit / revenue) * 100, 2),
        "ebitda": round(ebitda, 2),
        "ebitda_margin_pct": round((ebitda / revenue) * 100, 2),
        "ebit": round(ebit, 2),
        "ebit_margin_pct": round((ebit / revenue) * 100, 2),
        "net_income": round(net_income, 2),
        "net_margin_pct": round((net_income / revenue) * 100, 2),
        "production_efficiency_score": round(np.random.uniform(70, 95), 2),
        "cost_per_ton": round(cogs / prod_vol, 2),
        "revenue_per_ton": round(revenue / prod_vol, 2),
        "profit_per_ton": round(net_income / prod_vol, 2),
        "energy_per_ton_mwh": round(energy_cons / prod_vol, 4),
        "water_per_ton_m3": round(water_usage / prod_vol, 4),
        "waste_per_ton_produced": round(waste / prod_vol, 4),
        "availability_pct": round(np.random.uniform(85, 99), 2),
        "performance_pct": round(np.random.uniform(85, 99), 2),
        "quality_pct": round(quality, 2),
        "oee_pct": round(oee, 2),
        "safety_score": round(np.random.uniform(80, 100), 2),
        "environmental_score": round(np.random.uniform(80, 100), 2),
        "revenue_per_employee": round(revenue / 300, 2),
        "production_per_employee": round(prod_vol / 300, 2)
    }
    data.append(row)

df_synthetic = pd.DataFrame(data)
# Reordenar para bater com o original
df_synthetic = df_synthetic[columns]
df_synthetic.to_csv('synthetic_chemical_kpis_1500.csv', index=False)