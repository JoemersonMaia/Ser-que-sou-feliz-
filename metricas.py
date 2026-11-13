# %% 
import pandas as pd

df = pd.read_csv("Dados Comunidade (respostas) - dados.csv")
df

# %%

df= df.replace({"Sim":1,
                "Não":0})

df.head()

# %%
num_vars = [
    "Curte games?",
    "Curte futebol?",
    "Curte livros?",
    "Curte jogos de tabuleiro?",
    "Curte jogos de fórmula 1?",
    "Curte jogos de MMA?",
    "Idade",
]
dummy_vars =[
"Como conheceu o Téo Me Why?",
"Quantos cursos acompanhou do Téo Me Why?",
"Estado que mora atualmente",
"Área de Formação",
"Tempo que atua na área de dados",
"Posição da cadeira (senioridade)",
]

df_analise = pd.get_dummies(df[dummy_vars]).astype(int)
df_analise[num_vars] = df[num_vars].copy()
df_analise["pessoa feliz"] = df["Você se considera uma pessoa feliz?"].copy()
df_analise

# %%

from sklearn import tree
from sklearn import naive_bayes
from sklearn import linear_model

freatures =  df_analise.columns[:-1].to_list()
X= df_analise[freatures]
y = df_analise["pessoa feliz"]

arvore = tree.DecisionTreeClassifier(random_state=42,
                                     min_samples_leaf=6,
                                     )

arvore.fit(X, y)

naive = naive_bayes.GaussianNB()
naive.fit(X, y)

reg = linear_model.LogisticRegression(penalty=None, fit_intercept=True)
reg.fit(X,y)

# %%
arvore_predict = arvore.predict(X)

df_predict = df_analise[["pessoa feliz"]].copy()

df_predict["proba_reg"] = reg.predict_proba(X)[:,1]
df_predict["predict_reg"] = reg.predict(X)

# %%

from sklearn import metrics

acc_reg = metrics.accuracy_score(df_predict["pessoa feliz"],df_predict["predict_reg"] )
precisao_reg = metrics.precision_score(df_predict["pessoa feliz"],df_predict["predict_reg"] )
recall_reg = metrics.recall_score(df_predict["pessoa feliz"],df_predict["predict_reg"] )
roc_reg = metrics.roc_curve(df_predict["pessoa feliz"],df_predict["proba_reg"] )
auc_reg = metrics.roc_auc_score(df_predict["pessoa feliz"],df_predict["proba_reg"] )


# %%%

import matplotlib.pyplot as plt


plt.plot(roc_reg[0], roc_reg[1], "o-")
plt.grid(True)
plt.title("ROC Curve")
plt.xlabel("1 = especificidade")
plt.ylabel("recall")

plt.legend([f"naive: {auc_reg:.2f}"])

# %%

pd.Series({"model":reg, "features":freatures}).to_pickle("model_feliz.pke")

# %%
