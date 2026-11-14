# 😄 Será que sou feliz?

> Responda 13 perguntinhas e deixe uma Regressão Logística palpitar sobre a sua felicidade.

<p align="left">
  <img src="https://img.shields.io/badge/PYTHON-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/STREAMLIT-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit" />
  <img src="https://img.shields.io/badge/SCIKIT--LEARN-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white" alt="scikit-learn" />
  <img src="https://img.shields.io/badge/PANDAS-150458?style=for-the-badge&logo=pandas&logoColor=white" alt="Pandas" />
  <img src="https://img.shields.io/badge/MATPLOTLIB-11557C?style=for-the-badge" alt="Matplotlib" />
</p>

---

## 📑 Sumário

- [Sobre o projeto](#-sobre-o-projeto)
- [Demonstração](#-demonstração)
- [Funcionalidades](#-funcionalidades)
- [Estrutura do projeto](#-estrutura-do-projeto)
- [Como funciona o modelo](#-como-funciona-o-modelo)
- [Instalação e execução](#-instalação-e-execução)
- [Dicionário de dados](#-dicionário-de-dados)
- [Limitações e avisos](#-limitações-e-avisos)
- [Melhorias futuras](#-melhorias-futuras)
- [Como contribuir](#-como-contribuir)
- [Licença](#-licença)
- [Autor e contato](#-autor-e-contato)
- [Agradecimentos](#-agradecimentos)

---

## 💡 Sobre o projeto

**Será que sou feliz?** é um app web feito com **Streamlit** que estima a probabilidade de uma pessoa se considerar feliz a partir das respostas dela a um questionário.

Por trás da brincadeira há um fluxo completo de ciência de dados: uma pesquisa real com a comunidade do **Téo Me Why** (canal de dados e tecnologia), tratamento da base, comparação de algoritmos de classificação, treino de um modelo final (**Regressão Logística**) e uma interface para colocar esse modelo para conversar com o usuário.

---

## 🎬 Demonstração

<p align="center">
  <img src="docs/img/app.png" alt="Tela do app Será que sou feliz?, com o questionário e o resultado da avaliação" width="800" />
</p>

---

## ✨ Funcionalidades

- Questionário interativo com **13 perguntas**, usando `selectbox`, `radio` e `number_input`, organizadas em 3 colunas.
- Conversão das respostas "Sim/Não" em 1/0 e codificação *one-hot* das variáveis categóricas.
- Alinhamento das respostas a um template com todas as colunas esperadas pelo modelo.
- Cálculo da **probabilidade de "feliz"** com `predict_proba`.
- Resultado exibido em `st.success` ou `st.error`, conforme a faixa de probabilidade (acima de 70%, de 40% a 70% e abaixo de 40%).
- Script de treino (`metricas.py`) que trata os dados, compara três algoritmos e salva o modelo final.

---

## 🗂️ Estrutura do projeto

```text
Ser-que-sou-feliz-/
├── .vscode/
│   └── settings.json                         # ambiente conda como padrão no VS Code
├── Dados Comunidade (respostas) - dados.csv  # base da pesquisa (182 respostas)
├── app.py                                    # interface Streamlit
├── metricas.py                               # tratamento, treino e métricas (células "# %%")
└── model_feliz.pke                           # modelo serializado com pickle
```

| Arquivo | Função |
|---------|--------|
| `app.py` | Carrega o modelo, coleta as respostas, aplica *one-hot encoding* e mostra a probabilidade de felicidade. |
| `metricas.py` | Script em células `# %%` (estilo notebook no VS Code). Treina Árvore de Decisão, Naive Bayes e Regressão Logística, calcula acurácia, precisão, recall, curva ROC e AUC e salva o modelo final. |
| `model_feliz.pke` | `pd.Series` serializada com duas chaves: `model` (a `LogisticRegression`) e `features` (a lista de colunas). |
| `Dados Comunidade (respostas) - dados.csv` | Respostas da pesquisa, coletadas entre 12/06/2025 e 14/06/2025. |

---

## 🧠 Como funciona o modelo

### Pipeline dos dados até a previsão

```text
CSV da pesquisa
      ↓
Sim/Não → 1/0
      ↓
One-hot encoding das variáveis categóricas (get_dummies)
      ↓
Treino dos modelos (Árvore, Naive Bayes, Regressão Logística)
      ↓
Modelo final salvo em model_feliz.pke
      ↓
app.py: respostas → one-hot → template de colunas → predict_proba
      ↓
Probabilidade de "feliz"
```

### Variáveis usadas

- **Numéricas (7):** os seis "Curte…?" (games, futebol, livros, jogos de tabuleiro, Fórmula 1 e MMA, já convertidos para 1/0) e a idade.
- **Categóricas (6), com *one-hot encoding*:** como conheceu o Téo Me Why, quantos cursos acompanhou, estado, área de formação, tempo de atuação em dados e senioridade. Isso gera 48 colunas.
- **Alvo:** "Você se considera uma pessoa feliz?" (Sim/Não).

### Algoritmos

O `metricas.py` treina três classificadores com os mesmos dados:

| Algoritmo | Configuração no código |
|-----------|------------------------|
| Árvore de Decisão | `DecisionTreeClassifier(random_state=42, min_samples_leaf=6)` |
| Naive Bayes | `GaussianNB()` |
| **Regressão Logística** (modelo final) | `LogisticRegression(penalty=None, fit_intercept=True)` |

Apenas a **Regressão Logística** tem as métricas (acurácia, precisão, recall, curva ROC e AUC) calculadas no script e é ela que é salva em `model_feliz.pke` e usada pelo app.

### Faixas de resultado no app

| Probabilidade | Componente exibido |
|---------------|--------------------|
| Acima de 70% | `st.success` |
| De 40% a 70% | `st.success` |
| Abaixo de 40% | `st.error` |

---

## 🚀 Instalação e execução

**1. Clonar o repositório**

```bash
git clone https://github.com/JoemersonMaia/Ser-que-sou-feliz-.git
cd Ser-que-sou-feliz-
```

**2. Criar o ambiente** (escolha uma das opções)

```bash
# Opção A: venv
python -m venv .venv
source .venv/bin/activate          # Linux/macOS
.venv\Scripts\Activate.ps1         # Windows (PowerShell)

# Opção B: conda
conda create -n feliz python=3
conda activate feliz
```

**3. Instalar as dependências**

```bash
pip install streamlit pandas scikit-learn matplotlib
```

**4. Rodar o app**

```bash
streamlit run app.py
```

O Streamlit abre o app no navegador (normalmente em `http://localhost:8501`). Execute o comando **na raiz do projeto**, porque o app lê `model_feliz.pke` por caminho relativo.

### Retreinar o modelo

O `metricas.py` foi escrito em células `# %%`. O jeito mais confortável de usá-lo é abri-lo no VS Code e executar célula por célula.

Também é possível rodar tudo de uma vez, na raiz do projeto:

```bash
python metricas.py
```

Isso treina os modelos e **sobrescreve** o `model_feliz.pke`. Rodando como script comum, o gráfico da curva ROC não é exibido (o código não chama `plt.show()`) e as métricas ficam apenas em variáveis, sem serem impressas.

---

## 📖 Dicionário de dados

A base tem **182 respostas** e 15 colunas.

| Coluna | Tipo | Valores possíveis |
|--------|------|-------------------|
| `Carimbo de data/hora` | Data e hora | Momento do envio da resposta (não é usada no modelo) |
| `Como conheceu o Téo Me Why?` | Categórica | Amigos, Instagram, LinkedIn, Outra rede social, Twitch, Twitter / X, YouTube |
| `Quantos cursos acompanhou do Téo Me Why?` | Categórica | 0, 1, 2, 3, Mais que 3 |
| `Curte games?` | Binária | Sim, Não |
| `Curte futebol?` | Binária | Sim, Não |
| `Curte livros?` | Binária | Sim, Não |
| `Curte jogos de tabuleiro?` | Binária | Sim, Não |
| `Curte jogos de fórmula 1?` | Binária | Sim, Não |
| `Curte jogos de MMA?` | Binária | Sim, Não |
| `Idade` | Numérica (inteiro) | De 18 a 64 na base; o app aceita de 18 a 100 |
| `Estado que mora atualmente` | Categórica (UF) | AM, BA, CE, DF, ES, GO, MA, MG, MT, PA, PB, PE, PR, RJ, RN, RS, SC, SP |
| `Área de Formação` | Categórica | Biológicas, Exatas, Humanas |
| `Tempo que atua na área de dados` | Categórica | Não atuo, De 0 a 6 meses, De 6 meses a 1 ano, De 1 ano a 2 anos, de 2 anos a 4 anos, Mais de 4 anos |
| `Posição da cadeira (senioridade)` | Categórica | Iniciante, Júnior, Pleno, Sênior, Especialista, Coordenação, Gerência, Diretoria, C-Level |
| `Você se considera uma pessoa feliz?` | Binária (alvo) | Sim, Não |

---

## 🔭 Melhorias futuras

> Nenhum dos itens abaixo está implementado.

- Corrigir a etapa de pré-processamento do `app.py` para que as variáveis numéricas cheguem ao modelo.
- Separar os dados em treino e teste.
- Usar validação cruzada para comparar os algoritmos de forma justa.
- Calcular métricas também para Árvore de Decisão e Naive Bayes.
- Adicionar um `requirements.txt`.
- Fazer o deploy no Streamlit Community Cloud.
- Escrever testes automatizados.
- Incluir mais variáveis na pesquisa.
- Corrigir os textos da interface.

---

## 🤝 Como contribuir

1. Faça um *fork* do repositório.
2. Crie uma branch para a sua alteração: `git checkout -b minha-melhoria`.
3. Faça os commits com mensagens claras.
4. Envie a branch: `git push origin minha-melhoria`.
5. Abra um *Pull Request* descrevendo o que mudou e por quê.

Sugestões e *issues* também são muito bem-vindas.

---

## 👤 Autor e contato

**Joemerson Maia**

- GitHub: [@JoemersonMaia](https://github.com/JoemersonMaia)
- LinkedIn: https://www.linkedin.com/in/joemerson-maia-198b39365/

---

## 🙏 Agradecimentos

- Ao **Téo Me Why**, pelo conteúdo e pela inspiração.
- À **comunidade** que respondeu à pesquisa e tornou este projeto possível.
