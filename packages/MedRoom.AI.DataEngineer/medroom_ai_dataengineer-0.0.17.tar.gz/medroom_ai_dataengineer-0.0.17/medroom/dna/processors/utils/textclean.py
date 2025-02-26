import re  # Importa o módulo de expressões regulares
import string  # Importa módulo com constantes e operações de strings
import spacy  # Importa a biblioteca spaCy para processamento de linguagem natural
from nltk.corpus import stopwords  # Importa lista de stopwords do nltk
from nltk.stem import RSLPStemmer  # Importa o algoritmo RSLP para stemização em português
from nltk.tokenize import word_tokenize  # Importa função de tokenização de palavras do nltk
from unidecode import unidecode  # Importa função para remover acentos de strings

class TextPreprocessor:
    RE_PUNCTUATION = re.compile(rf"[{string.punctuation}]")  # Regex para identificar pontuações
    RE_DIGITS = re.compile(r"\d+")  # Regex para identificar dígitos
    STOP_WORDS = set(stopwords.words("portuguese"))  # Define conjunto de stopwords em português

    def __init__(
        self, remove_accents=True, remove_digits=True, use_lemmatization=True, use_stemming=False, remove_stopwords=True
    ):
        # Inicializa as configurações de preprocessamento
        self.remove_accents = remove_accents
        self.remove_digits = remove_digits
        self.use_lemmatization = use_lemmatization
        self.use_stemming = use_stemming
        self.remove_stopwords = remove_stopwords
        self.stemmer = RSLPStemmer() if use_stemming else None # Carrega stemmer se necessário
        self.nlp = spacy.load("pt_core_news_sm") if use_lemmatization else None  # Carrega modelo spaCy se necessário

    @staticmethod
    def remove_consecutive_duplicates(tokens):
        # Remove duplicatas consecutivas de uma lista de tokens
        return [t for i, t in enumerate(tokens) if i == 0 or t != tokens[i - 1]]

    def preprocess_text(self, text):
        # Processa texto de acordo com as configurações de preprocessamento
        text = text.lower() # Converte texto para minúsculas
        text = self.RE_PUNCTUATION.sub(" ", text) # Substitui pontuações por espaço
        if self.remove_digits:
            text = self.RE_DIGITS.sub("", text) # Remove dígitos

        tokens = word_tokenize(text) # Tokeniza o texto

        result_tokens = []
        for word in tokens:
            if self.remove_stopwords and word in self.STOP_WORDS:
                continue
            if self.use_lemmatization:
                doc = self.nlp(word)
                word = doc[0].lemma_ if doc else word # Aplica lematização
            if self.use_stemming:
                word = self.stemmer.stem(word) # Aplica stemização
            if self.remove_accents:
                word = unidecode(word)
            result_tokens.append(word) # Remove acentos

        result_tokens = self.remove_consecutive_duplicates(result_tokens) # Remove duplicatas consecutivas
        return " ".join(result_tokens)  # Junta os tokens em uma string e retorna