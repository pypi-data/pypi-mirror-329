from io import BytesIO  # Importa utilitário para manipulação de streams de bytes

import matplotlib.pyplot as plt  # Importa a biblioteca para criação de gráficos
import numpy as np  # Importa a biblioteca NumPy para operações numéricas
import pandas as pd  # Importa a biblioteca Pandas para manipulação de dados
import seaborn as sns  # Importa a biblioteca Seaborn para gráficos estatísticos
from sklearn.metrics import (  # Importa métricas de avaliação de modelos
    accuracy_score,
    classification_report,
    confusion_matrix,
    roc_auc_score,
)
from sklearn.preprocessing import LabelBinarizer  # Importa utilitário para binarização de labels


class ModelEvaluator:
    @staticmethod
    def accuracy(y_true, y_pred):
        """Calcula e imprime a acurácia do modelo."""
        if len(y_true) == 0 or len(y_pred) == 0:
            raise ValueError("y_true e y_pred não devem estar vazios.")  # Valida se os inputs não estão vazios
        acc = accuracy_score(y_true, y_pred)  # Calcula a acurácia
        print(f"Acurácia do modelo = {acc * 100.0:.2f}%")  # Imprime a acurácia formatada
        return acc

    @staticmethod
    def flatten_classification_report(report, prefix="", suffix=""):
        """Achata o relatório de classificação em um dicionário único com prefixos e sufixos opcionais."""
        flat_report = {}  # Inicializa o dicionário achatado
        for key, value in report.items():  # Itera sobre os itens do relatório
            if isinstance(value, dict):  # Checa se o valor é um dicionário
                for metric, metric_value in value.items():
                    flat_report[f"{prefix} {key} {metric} {suffix}".strip()] = (
                        metric_value  # Adiciona métricas com prefixos/sufixos
                    )
            else:
                flat_report[f"{prefix} {key} {suffix}".strip()] = value
        return flat_report

    @staticmethod
    def _generate_heatmap(data, title, cmap="Greens", square=False, fmt="0.2f"):
        """Função auxiliar para gerar um heatmap a partir dos dados."""
        fig, ax = plt.subplots()  # Cria a figura e o eixo
        sns.heatmap(
            data, cmap=cmap, linewidths=0.5, annot=True, fmt=fmt, cbar=False, square=square, ax=ax
        )  # Desenha o heatmap
        ax.set_title(title)  # Define o título do gráfico
        img = BytesIO()  # Cria um buffer para a imagem
        plt.savefig(img, format="png", bbox_inches="tight")  # Salva a imagem no buffer
        plt.close(fig)  # Fecha a figura para liberar memória
        img.seek(0)  # Reposiciona o cursor do buffer para o início
        return img

    @staticmethod
    def classification_report_img_generator(y_true, y_pred):
        report = classification_report(y_true, y_pred, output_dict=True)  # Gera relatório de classificação
        report_df = pd.DataFrame(report).transpose().drop(columns=["support"])  # Transforma o relatório em DataFrame
        return (
            ModelEvaluator._generate_heatmap(report_df, "Classification Report"),
            report,
        )  # Retorna o heatmap e o relatório

    @staticmethod
    def confusion_matrix_img_generator(y_true, y_pred):
        cnf_matrix = confusion_matrix(y_true, y_pred)  # Gera a matriz de confusão
        report_df = pd.DataFrame(
            classification_report(y_true, y_pred, output_dict=True)
        ).transpose()  # Gera DataFrame do relatório
        cnf_matrix_df = pd.DataFrame(
            cnf_matrix, index=report_df.index[:-3].values, columns=report_df.index[:-3].values
        )  # Formata a matriz de confusão
        cnf_matrix_normalized = (
            cnf_matrix_df / cnf_matrix_df.sum(axis=1).values[:, np.newaxis]
        )  # Normaliza a matriz de confusão
        return (
            ModelEvaluator._generate_heatmap(cnf_matrix_normalized, "Confusion Matrix", square=True, fmt=".0%"),
            cnf_matrix_normalized,
        )  # Retorna o heatmap e a matriz normalizada

    @staticmethod
    def roc_auc(y_true, y_pred):
        lb = LabelBinarizer()  # Inicializa o binarizador de labels
        lb.fit(y_true)  # Ajusta o binarizador aos valores verdadeiros
        y_test = lb.transform(y_true)  # Transforma os valores verdadeiros
        y_pred = lb.transform(y_pred)  # Transforma os valores preditos
        auc_roc = roc_auc_score(y_test, y_pred, average="weighted", multi_class="ovr")  # Calcula o ROC-AUC
        print(f"ROC_AUC do modelo = {auc_roc * 100.0:.2f}%")  # Imprime o ROC-AUC formatado
        return auc_roc
