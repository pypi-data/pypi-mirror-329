# Importando Libs
import json
import os
import pickle
import shutil
import tempfile
from typing import Any, Dict, Optional

import mlflow
from mlflow.entities import Experiment
from mlflow.pyfunc import PythonModel
from PIL import Image
from pydantic import BaseModel, ValidationError
from transformers import pipeline


class TransformersWrapper(PythonModel):
    def __init__(self, model_path):
        self.model_path = model_path
        self.model = None
        self.load_model()

    def load_model(self):
        self.model = pipeline("sentiment-analysis", model=self.model_path)

    def predict(self, model_input):
        return self.model(model_input)


def delete_folder_or_file(path: str) -> Optional[str]:
    if not os.path.exists(path):
        return f"O caminho '{path}' não existe."
    try:
        if os.path.isfile(path) or os.path.islink(path):
            os.unlink(path)  # Remove arquivos ou links
        elif os.path.isdir(path):
            shutil.rmtree(path)  # Remove diretórios e seus conteúdos
    except Exception as e:
        return f"Falha ao deletar {path}. Razão: {e}"
    return None


class ConsolidatedData(BaseModel):
    params: Dict[str, Any]
    metrics: Dict[str, Any]
    artifacts: Dict[str, Any]
    tags: Dict[str, str]


class MLFlowHelper:
    def __init__(self, server_url, experiment_name):
        mlflow.set_tracking_uri(f"{server_url}")  # Define o URI de rastreamento do MLflow
        self.experiment = self.create_or_get_experiment(experiment_name)  # Cria ou recupera um experimento
        self.artifact_handlers = {
            "img": self._process_image_artifact,  # Handler para imagens
            "df_example": self._process_dataframe_artifact,  # Handler para exemplos de DataFrame
            "model_pipeline": self._process_model_pipeline_artifact,  # Handler para pipelines de modelos
        }

    def save_data_pickle(self, dados, nome_arquivo):
        # Validação usando Pydantic
        try:
            validated_data = ConsolidatedData(**dados)
            print("Validação bem-sucedida dos dados.")
        except ValidationError as e:
            print(f"Erro de validação: {e}")
            return  # Não salva o pickle se a validação falhar

        # Salvando os dados em pickle
        with open(nome_arquivo, "wb") as arquivo:
            pickle.dump(dados, arquivo)
        print(f"Dados salvos no arquivo pickle: {nome_arquivo}")

        """
        # Salvando o modelo se necessário
        if save_model and "model_pipeline" in validated_data.artifacts:
            if model_path is None:
                print("Erro: O caminho do modelo não foi fornecido.")
                return
            validated_data.artifacts["model_pipeline"].save_pretrained(model_path)
            print(f"Modelo salvo no diretório: {model_path}")
        """

    def load_data_pickle(self, nome_arquivo):
        with open(nome_arquivo, "rb") as arquivo:
            return pickle.load(arquivo)  # Carrega dados de um arquivo pickle

    def create_or_get_experiment(self, experiment_name: str) -> Experiment:
        experiment = mlflow.get_experiment_by_name(experiment_name)
        if experiment is None:
            experiment_id_created = mlflow.create_experiment(experiment_name)
            print(f"Experimento '{experiment_name}' não existe, criando ele com id {experiment_id_created}.")
            return mlflow.get_experiment_by_name(experiment_name)
        else:
            print(f"Experimento '{experiment_name}' já existe, usando ele com id {experiment.experiment_id}.")
            return experiment

    def log_run(self, consolidated_data, log_model: bool = False):
        try:
            with mlflow.start_run(experiment_id=self.experiment.experiment_id):
                self._log_parameters(consolidated_data["params"])  # Registra os parâmetros do experimento
                self._log_metrics(consolidated_data["metrics"])  # Registra as métricas do experimento
                self._set_tags(consolidated_data["tags"])  # Define tags para o experimento
                self._process_artifacts(consolidated_data["artifacts"])  # Processa e registra os artefatos
                print("Todos os artefatos foram logados com sucesso.")

                # Não logar o modelo no MLFlow se log_model for False
                if log_model and "model_pipeline" in consolidated_data["artifacts"]:
                    self._process_model_pipeline_artifact(
                        "model_pipeline", consolidated_data["artifacts"]["model_pipeline"]
                    )
        except Exception as e:
            print(f"Erro durante a execução do run: {e}")
            raise

    def _log_parameters(self, params):
        try:
            for key, value in params.items():
                print(f"Tentando logar parâmetro: {key}...")
                mlflow.log_param(key, str(value))  # Registra um parâmetro no MLflow
            print("Parâmetros logados com sucesso.")
        except Exception as e:
            print(f"Erro ao logar parâmetros: {e}")
            raise

    def _log_metrics(self, metrics):
        try:
            for key, value in metrics.items():
                print(f"Tentando logar métrica: {key}...")
                mlflow.log_metric(key, value)  # Registra uma métrica no MLflow
            print("Métricas logadas com sucesso.")
        except Exception as e:
            print(f"Erro ao logar métricas: {e}")
            raise

    def _set_tags(self, tags):
        try:
            for key, value in tags.items():
                print(f"Tentando logar tag: {key}...")
                mlflow.set_tag(key, value)  # Define uma tag no MLflow
            print("Tags logadas com sucesso.")
        except Exception as e:
            print(f"Erro ao definir tags: {e}")
            raise

    def _process_artifacts(self, artifacts):
        for key, value in artifacts.items():
            print(f"Tentando processar artefato: {key}...")
            handler = self._get_artifact_handler(key)  # Obtém o manipulador de artefatos adequado
            if handler:
                try:
                    handler(key, value)  # Processa o artefato específico
                except Exception as e:
                    print(f"Erro ao processar o artefato {key}: {e}")
                    raise

    def _get_artifact_handler(self, key):
        for handler_key, handler in self.artifact_handlers.items():
            if handler_key in key:
                return handler  # Retorna o manipulador de artefatos com base na chave
        return None

    def _process_image_artifact(self, key, value):
        try:
            print(f"Tentando processar imagem: {key}...")
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
                value.seek(0)
                img = Image.open(value)
                img.save(tmp.name)
                mlflow.log_artifact(tmp.name, f"images/{key}")  # Registra a imagem no MLflow
                print(f"Imagem '{key}' processada e logada com sucesso.")
        except Exception as e:
            print(f"Erro ao processar imagem {key}: {e}")
            raise

    def _process_dataframe_artifact(self, key, value):
        try:
            print(f"Tentando processar DataFrame: {key}...")
            with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as tmp:
                json.dump(value, tmp)
                tmp.flush()
                mlflow.log_artifact(tmp.name, f"data/{key}")  # Registra o DataFrame no MLflow
                print(f"DataFrame '{key}' processado e logado com sucesso.")
        except Exception as e:
            print(f"Erro ao processar DataFrame {key}: {e}")
            raise

    def _process_model_pipeline_artifact(self, key, value):
        try:
            print(f"Tentando processar modelo: {key}...")
            model_temp_path = "temp_model"
            value.save_pretrained(model_temp_path)
            mlflow.pyfunc.log_model(
                artifact_path="model_pipeline",
                python_model=TransformersWrapper(model_temp_path),
            )  # Registra o modelo no MLflow
            print(f"Modelo '{key}' processado e logado com sucesso.")
            delete_folder_or_file(model_temp_path)
        except Exception as e:
            print(f"Erro ao processar modelo {key}: {e}")
            raise
