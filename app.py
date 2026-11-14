
import streamlit as st
import pandas as pd
import numpy as np

# Configuração da página
st.set_page_config(
    page_title="Descubra a Felicidade",
    page_icon="😊",
    layout="wide"
)

# Carregamento do modelo
@st.cache_resource
def carregar_modelo():
    return pd.read_pickle("model_feliz.pke")

try:
    model = carregar_modelo()
except ModuleNotFoundError as erro:
    st.error(f"Biblioteca necessária não encontrada: {erro.name}")
    st.info("Verifique o arquivo requirements.txt e as dependências do modelo.")
    st.stop()
except FileNotFoundError:
    st.error("Arquivo model_feliz.pke não encontrado no repositório.")
    st.stop()
except Exception as erro:
    st.error(f"Não foi possível carregar o modelo: {erro}")
    st.stop()

# Título
st.markdown("# Descubra a Felicidade")

# Opções dos formulários
cursos_opt = ['0', '2', '1', '3', 'Mais que 3']
cursos = st.selectbox(
    "Quantos cursos acompanhou do Téo Me Why?",
    cursos_opt
)

redes_opt = [
    'LinkedIn', 'Twitch', 'YouTube', 'Instagram',
    'Amigos', 'Twitter / X', 'Outra rede social'
]

redes = st.selectbox(
    "Como conheceu o Téo Me Why?",
    options=redes_opt
)

col1, col2, col3 = st.columns(3)

with col1:
    video_game = st.radio("Curte Video Game?", ["Sim", "Não"])
    futebol = st.radio("Curte Futebol?", ["Sim", "Não"])

    idade = st.number_input(
        "Sua idade",
        min_value=18,
        max_value=100,
        value=18
    )

    areas_formacao = ['Biológicas', 'Exatas', 'Humanas']

    tempos = [
        'De 0 a 6 meses',
        'De 1 ano a 2 anos',
        'De 6 meses a 1 ano',
        'Mais de 4 anos',
        'Não atuo',
        'de 2 anos a 4 anos'
    ]

    tempo = st.selectbox(
        "Tempo que atua na área de dados",
        options=tempos
    )

with col2:
    livros = st.radio("Curte livros?", ["Sim", "Não"])
    tabuleiro = st.radio("Curte jogos de tabuleiro?", ["Sim", "Não"])

    ufs = [
        'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA',
        'MG', 'MT', 'PA', 'PB', 'PE', 'PR', 'RJ',
        'RN', 'RS', 'SC', 'SP'
    ]

    uf = st.selectbox(
        "Estado que mora atualmente",
        options=ufs
    )

    niveis = [
        'Iniciante', 'Júnior', 'Pleno', 'Sênior',
        'Especialista', 'Coordenação', 'Gerência',
        'Diretoria', 'C-Level'
    ]

    cadeira = st.selectbox(
        "Posição da cadeira (senioridade)",
        options=niveis
    )

with col3:
    f1 = st.radio("Curte jogos de Fórmula 1?", ["Sim", "Não"])
    mma = st.radio("Curte jogos de MMA?", ["Sim", "Não"])

    formacao = st.selectbox(
        "Área de Formação",
        options=areas_formacao
    )

# Preparação dos dados
data = {
    'Como conheceu o Téo Me Why?': redes,
    'Quantos cursos acompanhou do Téo Me Why?': cursos,
    'Curte games?': video_game,
    'Curte futebol?': futebol,
    'Curte livros?': livros,
    'Curte jogos de tabuleiro?': tabuleiro,
    'Curte jogos de fórmula 1?': f1,
    'Curte jogos de MMA?': mma,
    'Idade': idade,
    'Estado que mora atualmente': uf,
    'Área de Formação': formacao,
    'Tempo que atua na área de dados': tempo,
    'Posição da cadeira (senioridade)': cadeira,
}

df = pd.DataFrame([data]).replace({
    "Sim": 1,
    "Não": 0
})

# Transformação das variáveis categóricas
dummy_vars = [
    "Como conheceu o Téo Me Why?",
    "Quantos cursos acompanhou do Téo Me Why?",
    "Estado que mora atualmente",
    "Área de Formação",
    "Tempo que atua na área de dados",
    "Posição da cadeira (senioridade)",
]

df = pd.get_dummies(df[dummy_vars]).astype(int)

# Estrutura das colunas esperadas pelo modelo
df_template = pd.DataFrame(columns=[
    'Como conheceu o Téo Me Why?_Amigos',
    'Como conheceu o Téo Me Why?_Instagram',
    'Como conheceu o Téo Me Why?_LinkedIn',
    'Como conheceu o Téo Me Why?_Outra rede social',
    'Como conheceu o Téo Me Why?_Twitch',
    'Como conheceu o Téo Me Why?_Twitter / X',
    'Como conheceu o Téo Me Why?_YouTube',
    'Quantos cursos acompanhou do Téo Me Why?_0',
    'Quantos cursos acompanhou do Téo Me Why?_1',
    'Quantos cursos acompanhou do Téo Me Why?_2',
    'Quantos cursos acompanhou do Téo Me Why?_3',
    'Quantos cursos acompanhou do Téo Me Why?_Mais que 3',
    'Estado que mora atualmente_AM',
    'Estado que mora atualmente_BA',
    'Estado que mora atualmente_CE',
    'Estado que mora atualmente_DF',
    'Estado que mora atualmente_ES',
    'Estado que mora atualmente_GO',
    'Estado que mora atualmente_MA',
    'Estado que mora atualmente_MG',
    'Estado que mora atualmente_MT',
    'Estado que mora atualmente_PA',
    'Estado que mora atualmente_PB',
    'Estado que mora atualmente_PE',
    'Estado que mora atualmente_PR',
    'Estado que mora atualmente_RJ',
    'Estado que mora atualmente_RN',
    'Estado que mora atualmente_RS',
    'Estado que mora atualmente_SC',
    'Estado que mora atualmente_SP',
    'Área de Formação_Biológicas',
    'Área de Formação_Exatas',
    'Área de Formação_Humanas',
    'Tempo que atua na área de dados_De 0 a 6 meses',
    'Tempo que atua na área de dados_De 1 ano a 2 anos',
    'Tempo que atua na área de dados_De 6 meses a 1 ano',
    'Tempo que atua na área de dados_Mais de 4 anos',
    'Tempo que atua na área de dados_Não atuo',
    'Tempo que atua na área de dados_de 2 anos a 4 anos',
    'Posição da cadeira (senioridade)_C-Level',
    'Posição da cadeira (senioridade)_Coordenação',
    'Posição da cadeira (senioridade)_Diretoria',
    'Posição da cadeira (senioridade)_Especialista',
    'Posição da cadeira (senioridade)_Gerência',
    'Posição da cadeira (senioridade)_Iniciante',
    'Posição da cadeira (senioridade)_Júnior',
    'Posição da cadeira (senioridade)_Pleno',
    'Posição da cadeira (senioridade)_Sênior',
    'Curte games?',
    'Curte futebol?',
    'Curte livros?',
    'Curte jogos de tabuleiro?',
    'Curte jogos de fórmula 1?',
    'Curte jogos de MMA?',
    'Idade'
])

df = pd.concat([df_template, df], ignore_index=True).fillna(0)

# Organização das colunas para previsão
try:
    features = model['features']

    df = df.reindex(columns=features, fill_value=0)

    proba = model["model"].predict_proba(df)[:, 1][0]

except Exception as erro:
    st.error(f"Erro ao realizar a previsão: {erro}")
    st.stop()

# Resultado
st.markdown("---")
st.subheader("Resultado da sua avaliação")

if proba > 0.7:
    st.success(
        f"Você é uma pessoa feliz! Probabilidade: {100 * proba:.0f}%"
    )

elif proba > 0.4:
    st.warning(
        f"Você apresenta uma probabilidade moderada de felicidade: {100 * proba:.0f}%"
    )

else:
    st.error(
        f"Você apresenta uma baixa probabilidade de felicidade: {100 * proba:.0f}%"
    )
