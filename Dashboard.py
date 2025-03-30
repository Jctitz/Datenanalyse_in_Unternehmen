"""
Streamlit Dashboard zur Fondsanalyse
- Das Dashboard stellt eine interaktive Visualisierung der berechneten Fondskennzahlen dar
- Es können einzelne Fonds ausgewählt und im Zeitverlauf analysiert werden
- Dabei können die Kennzahlen die in Datenbrechnen.py berechnet wurde in unterschiedlichen Charts analysiert werden
"""


import streamlit as st
import pandas as pd
import pickle
import plotly.graph_objs as go

# Datenpfade
daten_ordner = './Ergebnisse'

# Farben
theme_colors = {
    'fonds': '#001F60',
    'bm': '#7F7F7F',
    'up': '#92FC7A',
    'down': '#EE8383',
    'corporate': '#728598'
}

# Daten laden
@st.cache_data
def lade_pickle(path):
    with open(path, 'rb') as f:
        return pickle.load(f)

fonds_meta = lade_pickle(f'{daten_ordner}/fonds_metadata.pkl')
fonds_meta["Label"] = fonds_meta["Fondsname"] + " - " + fonds_meta["ISIN"]

bench_meta = lade_pickle(f'{daten_ordner}/benchmark_metadata.pkl')

basis_kpis = ['Rendite', 'Vola', 'MaxDD', 'WorstMonth', 'Omega', 'Sharpe']
fit_kpis = ['TE', 'Beta', 'R2', 'BmKorr']
zeitfenster = ['12', '24', '36', '60']

fonds_daten = {kpi: lade_pickle(f'{daten_ordner}/{kpi}.pkl') for kpi in basis_kpis}
fonds_fit_daten = {kpi: lade_pickle(f'{daten_ordner}/{kpi}.pkl') for kpi in fit_kpis}
bench_daten = {kpi: lade_pickle(f'{daten_ordner}/Benchmarks_{kpi}.pkl') for kpi in basis_kpis}
percentil_daten = {kpi: lade_pickle(f'{daten_ordner}/Percentil_{kpi}.pkl') for kpi in basis_kpis}
korr = lade_pickle(f'{daten_ordner}/Korrelationen.pkl')

# Auswahl der Parameter in der Sidebar
st.sidebar.title("Parameter")
fonds_label = st.sidebar.selectbox("Fonds", fonds_meta['Label'])
kpi = st.sidebar.selectbox("Kennzahl", basis_kpis)
kpi_fit = st.sidebar.selectbox("Fit Kennzahl", fit_kpis)
window = st.sidebar.selectbox("Zeitraum (Monate)", zeitfenster)

fonds_id = fonds_meta[fonds_meta['Label'] == fonds_label].index[0]
peergroup = fonds_meta.loc[fonds_id, 'Peergroup']
benchmarkname = bench_meta.loc[peergroup, 'Benchmarkname']
benchmark_index = peergroup

# Fondsinfos
st.title("Fondsanalyse Dashboard")
st.markdown(f"### {fonds_meta.loc[fonds_id, 'Fondsname']} ({fonds_meta.loc[fonds_id, 'ISIN']})")
st.markdown(f"**Peergroup:** {peergroup}")
st.markdown(f"**Ranking:** {fonds_meta.loc[fonds_id, 'Ranking']}")
st.markdown(f"**Benchmark:** {benchmarkname}")

# Chart 1: Kennzahl-Zeitreihe gegen Benchmark
st.subheader("Kennzahl rollierend gegen Benchmark")
df_fonds = fonds_daten[kpi][f'{window}M']
df_bm = bench_daten[kpi][f'{window}M']

fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=df_fonds.index, y=df_fonds[fonds_id], mode='lines', name='Fonds', line=dict(color=theme_colors['fonds'])))
fig1.add_trace(go.Scatter(x=df_bm.index, y=df_bm[benchmark_index], mode='lines', name='Benchmark', line=dict(color=theme_colors['bm'])))
fig1.update_layout(title=f"{kpi} ({window}M)", xaxis_title="Datum", yaxis_title=kpi)
st.plotly_chart(fig1, use_container_width=True)

# Chart 2: Percentil-Rang
st.subheader("Percentil-Rang innerhalb Peergroup")
df_percentil = percentil_daten[kpi][f'{window}M']
fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=df_percentil.index, y=df_percentil[fonds_id], mode='lines', name='Perzentil', line=dict(color=theme_colors['corporate'])))
fig2.update_layout(title=f"Perzentil (Peergroup: {peergroup}) – {kpi} ({window}M)", xaxis_title="Datum", yaxis=dict(range=[0, 1], tickformat='.0%', title='Perzentil'))
st.plotly_chart(fig2, use_container_width=True)

# Chart 3: Benchmark-Fit
st.subheader("Benchmark-Fit Kennzahlen")
df_fit = fonds_fit_daten[kpi_fit][f'{window}M']
fig3 = go.Figure()
fig3.add_trace(go.Scatter(x=df_fit.index, y=df_fit[fonds_id], mode='lines', name=kpi_fit))
fig3.update_layout(title=f"Benchmark-Fit vs. {benchmarkname} ({window}M)", xaxis_title="Datum")
st.plotly_chart(fig3, use_container_width=True)

# Chart 4: Korrelationen
st.subheader("Korrelation zu allgemeinen Benchmarks")
labels = korr[f'Korr_{window}M'].index
bar1 = korr[f'Korr_{window}M'][fonds_id]
bar2 = korr[f'UpKorr_{window}M'][fonds_id]
bar3 = korr[f'DownKorr_{window}M'][fonds_id]

fig4 = go.Figure()
fig4.add_trace(go.Bar(name='Korr', x=labels, y=bar1, marker_color=theme_colors['corporate']))
fig4.add_trace(go.Bar(name='Up-Korr', x=labels, y=bar2, marker_color=theme_colors['up']))
fig4.add_trace(go.Bar(name='Down-Korr', x=labels, y=bar3, marker_color=theme_colors['down']))
fig4.update_layout(barmode='group', title=f"Korrelationen ({window}M)", xaxis_title="Benchmark",yaxis=dict(range=[-1, 1]))
st.plotly_chart(fig4, use_container_width=True)
