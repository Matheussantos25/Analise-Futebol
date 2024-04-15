import streamlit as st
import pandas as pd

#Função para calcular os resultados recentes do time
def resultados_recentes(df, team_name, num_games, venue='all'):
    if venue == 'home':
        df_team = df[df['HomeTeam'] == team_name][-num_games:]
    elif venue == 'away':
        df_team = df[df['AwayTeam'] == team_name][-num_games:]
    else:
        df_team = df[(df['HomeTeam'] == team_name) | (df['AwayTeam'] == team_name)][-num_games:]
    
    resultados = {'Vitória': 0, 'Empate': 0, 'Derrota': 0}
    for _, row in df_team.iterrows():
        if (row['HomeTeam'] == team_name and row['FTHG'] > row['FTAG']) or (row['AwayTeam'] == team_name and row['FTAG'] > row['FTHG']):
            resultados['Vitória'] += 1
        elif row['FTHG'] == row['FTAG']:
            resultados['Empate'] += 1
        else:
            resultados['Derrota'] += 1
    return resultados


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

     # Exibir resultados recentes para diferentes condições
    for num_games in [3, 5]:
        st.subheader(f'Últimos {num_games} jogos do {team_name} (em todas as condições):')
        resultados_recentes_dict = resultados_recentes(df, team_name, num_games)
        st.write(f"Vitórias: {resultados_recentes_dict['Vitória']}, Empates: {resultados_recentes_dict['Empate']}, Derrotas: {resultados_recentes_dict['Derrota']}")

        st.subheader(f'Últimos {num_games} jogos do {team_name} como mandante:')
        resultados_recentes_dict = resultados_recentes(df, team_name, num_games, 'home')
        st.write(f"Vitórias: {resultados_recentes_dict['Vitória']}, Empates: {resultados_recentes_dict['Empate']}, Derrotas: {resultados_recentes_dict['Derrota']}")

        st.subheader(f'Últimos {num_games} jogos do {team_name} como visitante:')
        resultados_recentes_dict = resultados_recentes(df, team_name, num_games, 'away')
        st.write(f"Vitórias: {resultados_recentes_dict['Vitória']}, Empates: {resultados_recentes_dict['Empate']}, Derrotas: {resultados_recentes_dict['Derrota']}")


    # Exibindo as informações
    st.write(f"Total de partidas na liga: {total_matches}")
    st.write(f"Total de goleadas na liga: {total_goleadas}")
    st.write(f"Proporção de goleadas na liga: {proportion_goleadas:.2%}")
    st.write(f"Total de partidas jogadas pelo {team_name}: {total_matches_by_team}")
    st.write(f"Total de goleadas feitas pelo {team_name}: {total_goleadas_by_team}")
    st.write(f"Proporção de goleadas pelo {team_name}: {proportion_goleadas_by_team:.2%}")
    st.write("Detalhes das goleadas:")
    st.dataframe(goleadas_team_info[['Data', 'Time Mandante', 'Time Visitante', 'Gols do Mandante', 'Gols do Visitante']])
