import streamlit as st
import pandas as pd

# Upload do arquivo
uploaded_file = st.file_uploader("Faça upload do arquivo CSV:")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Calculando a diferença de gols
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

    # Calcular o total de jogos jogados pelo time
    total_matches_by_team = len(df[(df['HomeTeam'] == team_name) | (df['AwayTeam'] == team_name)])
    
    # Calcular a proporção de goleadas feitas pelo time em relação ao total de jogos do time
    proportion_goleadas_by_team = total_goleadas_by_team / total_matches_by_team

    goleadas_team = pd.concat([goleadas_home, goleadas_away])

    # Renomeando colunas para termos mais amigáveis
    goleadas_team_info = goleadas_team.rename(columns={
        'Date': 'Data',
        'HomeTeam': 'Time Mandante',
        'AwayTeam': 'Time Visitante',
        'FTHG': 'Gols do Mandante',
        'FTAG': 'Gols do Visitante'
    })

    # Exibindo as informações
    st.write(f"Total de partidas na liga: {total_matches}")
    st.write(f"Total de goleadas na liga: {total_goleadas}")
    st.write(f"Proporção de goleadas na liga: {proportion_goleadas:.2%}")
    st.write(f"Total de partidas jogadas pelo {team_name}: {total_matches_by_team}")
    st.write(f"Total de goleadas feitas pelo {team_name}: {total_goleadas_by_team}")
    st.write(f"Proporção de goleadas pelo {team_name}: {proportion_goleadas_by_team:.2%}")
    st.write("Detalhes das goleadas:")
    st.dataframe(goleadas_team_info[['Data', 'Time Mandante', 'Time Visitante', 'Gols do Mandante', 'Gols do Visitante']])
