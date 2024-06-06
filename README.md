# Análise de dados voltado ao Futebol

Este projeto utiliza Streamlit e Pandas para analisar o desempenho recente de times de futebol com base nos resultados das partidas. Usuários podem carregar dados de partidas, explorar estatísticas de goleadas e verificar os resultados recentes dos times em diferentes condições de jogo: casa, fora, e global, ou seja, descondirenda mando de campo.

### Pré-requisitos

Antes de iniciar, você precisará instalar Python e as bibliotecas necessárias:

- Python 3.8+
- Pandas
- Streamlit

### Aplicação Do projeto

Para carregar a aplicação, basta digitar streamlit run nome_da_aplicacao.py, que nesse
caso coloquei o nome como Premier_League_Aplicacao


### Erros e correções durante o  código

Problema: A value is trying to be set on a copy of a slice from a DataFrame.
Try using .loc[row_indexer,col_indexer] = value instead

Solução: tive que usar o .loc para que o pandas entendesse que eu devia atualizar o DataFrame original e não apenas a visão atual, utilizei isso em empates.ipynb

Solução alternativa (mais simples): dados_2023 = dados_2023.copy(), só copiei os dados



### Reflxões Estudadas 

Existem padrões de variações, em geral quanto mais um time varia seus gols no HT em relação de uma rodada
para a seguinte, maior é a probabildiade de na próxima rodada ter essa variação de gols no HT, ou seja, pouco
provável de repetir mesma quantidade de gols no HT
