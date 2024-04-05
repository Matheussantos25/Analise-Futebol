import streamlit as st
import pandas as pd

uploaded_file = st.file_uploader("C:\\Users\\msdof\\OneDrive\\Imagens\\Ligas\\E0 (1).csv")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    df['GoalDifference'] = abs(df['FTHG'] - df['FTAG'])
    condicoes_goleada = (df['GoalDifference'] >= 3) & ~((df['FTHG'] == 3) & (df['FTAG'] == 0)) & ~((df['FTHG'] == 0) & (df['FTAG'] == 3))
    goleadas = df[condicoes_goleada]

    total_matches = df.shape[0]
    total_goleadas = goleadas.shape[0]
    proportion_goleadas = total_goleadas / total_matches

    # Selecionar um time
    team_list = df['HomeTeam'].unique()
    team_name = st.selectbox('Selecione um time:', team_list)

    goleadas_home = goleadas[goleadas['HomeTeam'] == team_name]
    goleadas_away = goleadas[goleadas['AwayTeam'] == team_name]
    total_goleadas_by_team = len(goleadas_home) + len(goleadas_away)

    goleadas_chelsea = pd.concat([goleadas_home, goleadas_away])
    goleadas_chelsea_info = goleadas_chelsea[['Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG']]

    st.write(f"Total de partidas: {total_matches}")
    st.write(f"Total de goleadas: {total_goleadas}")
    st.write(f"Proporção de goleadas: {proportion_goleadas:.2%}")
    st.write(f"Total de goleadas feitas pelo {team_name}: {total_goleadas_by_team}")
    st.write("Detalhes das goleadas:", goleadas_chelsea_info)
