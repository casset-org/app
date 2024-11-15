# coding: utf-8

"""graficos_neon_fundo_preto_reformulado.py"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from google.colab import drive
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

# Constantes e configurações
DRIVE_MOUNT_PATH = "/content/drive"
GRAPHPATH = "/content/drive/MyDrive/graficos"
SUMMARYPATH = "/content/drive/MyDrive/sumarios"
CSV_URL = "https://docs.google.com/spreadsheets/d/1PfVcZ2QYo9BAbwvU5Em7tCsAL9dVs_9f6TEWAYAlXlw/export?format=csv&gid=879458484"
NEON_PALETTE = ['#39FF14', '#FF073A', '#FFD700', '#00FFFF', '#FF69B4']
FIGSIZE = (10, 6)

# Estilo neon com fundo preto
sns.set(style="whitegrid")
plt.rcParams.update({
    'figure.facecolor': 'black',
    'axes.facecolor': 'black',
    'axes.edgecolor': 'white',
    'xtick.color': 'white',
    'ytick.color': 'white',
    'text.color': 'white',
    'legend.facecolor': 'black',
    'axes.labelcolor': 'white',
    'grid.color': 'gray'
})

# Função para carregar os dados
def load_data(url):
    try:
        df = pd.read_csv(url, delimiter=',', encoding='utf-8')
        df['Oxygen_Saturation'] = df['Oxygen_Saturation'].str.replace(',', '.').astype(float)
        return df
    except Exception as e:
        print(f"Erro ao carregar os dados: {e}")
        return None

# Função para salvar gráficos
def save_fig(filename):
    plt.savefig(os.path.join(GRAPHPATH, filename), dpi=300, bbox_inches='tight')
    plt.close()

# Função para criar figura
def create_figure():
    return plt.figure(figsize=FIGSIZE)

# Gráficos de violino
def generate_violinplot(df, x, y, hue, title, filename, split=False):
    create_figure()
    sns.violinplot(x=x, y=y, hue=hue, data=df, split=split, palette=NEON_PALETTE)
    plt.title(title)
    save_fig(filename)

# Histogramas
def generate_histplot(df, x, hue, title, filename, bins=20):
    create_figure()
    sns.histplot(data=df, x=x, hue=hue, bins=bins, palette=NEON_PALETTE)
    plt.title(title)
    save_fig(filename)

# KDEs
def generate_kdeplot(df, x, hue, title, filename):
    create_figure()
    sns.kdeplot(data=df, x=x, hue=hue, palette=NEON_PALETTE, fill=True)
    plt.title(title)
    save_fig(filename)

# Regressões não lineares de grau 3
def generate_nonlinear_regression_degree3(df, x, y, title, filename):
    create_figure()
    X = df[[x]]
    y = df[y]

    poly = PolynomialFeatures(degree=3)
    X_poly = poly.fit_transform(X)

    model = LinearRegression()
    model.fit(X_poly, y)

    X_range = np.linspace(X.min(), X.max(), 100).reshape(-1, 1)
    X_range_poly = poly.transform(X_range)

    plt.scatter(X, y, color='white', label='Dados Reais')
    plt.plot(X_range, model.predict(X_range_poly), color=NEON_PALETTE[0], label='Regressão Não Linear (Grau 3)', linewidth=2)
    plt.title(title)
    plt.legend()
    save_fig(filename)

# Sumário estatístico detalhado no estilo SPSS
def generate_statistical_summary_spss(df, col):
    try:
        summary = pd.DataFrame({
            'N': [df[col].count()],
            'Média': [df[col].mean()],
            'Desvio Padrão': [df[col].std()],
            'Variância': [df[col].var()],
            'Mínimo': [df[col].min()],
            'Máximo': [df[col].max()],
            'Assimetria': [df[col].skew()],
            'Curtose': [df[col].kurt()]
        })
        print(f"Sumário estatístico (estilo SPSS) para {col}:\n{summary}")
        summary.to_csv(os.path.join(SUMMARYPATH, f'summary_{col}_spss.csv'))
    except Exception as e:
        print(f"Erro ao gerar o sumário estatístico: {e}")

# Gráficos adicionais
def generate_boxplot(df, x, y, hue, title, filename):
    create_figure()
    sns.boxplot(x=x, y=y, hue=hue, data=df, palette=NEON_PALETTE)
    plt.title(title)
    save_fig(filename)

def generate_barplot(df, x, y, hue, title, filename):
    create_figure()
    sns.barplot(x=x, y=y, hue=hue, data=df, palette=NEON_PALETTE)
    plt.title(title)
    save_fig(filename)

# Main
if __name__ == "__main__":
    drive.mount(DRIVE_MOUNT_PATH, force_remount=True)
    os.makedirs(GRAPHPATH, exist_ok=True)
    os.makedirs(SUMMARYPATH, exist_ok=True)

    df = load_data(CSV_URL)

    if df is not None:
        if 'Causes_Respiratory_Imbalance' in df.columns:
            generate_violinplot(df, 'Causes_Respiratory_Imbalance', 'Heart_Rate', None, 'Violin: Frequência Cardíaca por Causa', 'violin_frequencia_causa.png', split=False)
            generate_violinplot(df, 'Causes_Respiratory_Imbalance', 'Oxygen_Saturation', None, 'Violin: Saturação de Oxigênio por Causa', 'violin_saturacao_causa.png', split=False)

        generate_kdeplot(df, 'Heart_Rate', 'Causes_Respiratory_Imbalance', 'KDE: Frequência Cardíaca por Causa', 'kde_frequencia_causa.png')
        generate_kdeplot(df, 'Oxygen_Saturation', 'Causes_Respiratory_Imbalance', 'KDE: Saturação de Oxigênio por Causa', 'kde_saturacao_causa.png')

        generate_nonlinear_regression_degree3(df, 'Heart_Rate', 'BPSYS', 'Regressão Não Linear: Pressão Sistólica por Frequência Cardíaca (Grau 3)', 'regressao_pressao_frequencia_grau3.png')
        generate_nonlinear_regression_degree3(df, 'Heart_Rate', 'Oxygen_Saturation', 'Regressão Não Linear: Saturação de Oxigênio por Frequência Cardíaca (Grau 3)', 'regressao_saturacao_frequencia_grau3.png')

        generate_boxplot(df, 'Causes_Respiratory_Imbalance', 'BPSYS', None, 'Boxplot: Pressão Sistólica por Causa', 'boxplot_pressao_causa.png')
        generate_boxplot(df, 'Causes_Respiratory_Imbalance', 'Heart_Rate', None, 'Boxplot: Frequência Cardíaca por Causa', 'boxplot_frequencia_causa.png')

        generate_statistical_summary_spss(df, 'Heart_Rate')
        generate_statistical_summary_spss(df, 'Oxygen_Saturation')