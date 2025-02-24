import pandas as pd
import re
from nltk.tokenize import word_tokenize
import os
import nltk

# Pastikan semua resource NLTK yang diperlukan tersedia
nltk.download('punkt')

def normalize_media_name(name):
    """ Normalize media names by removing spaces, special characters except '.',
        and converting to lowercase to handle various inconsistencies. """
    name = re.sub(r"[^\w\d\s.]", '', name)  # Remove special chars except dot
    name = re.sub(r"\s+", '', name)  # Remove spaces
    return name.lower()

class AsroPreprocessing:
    def __init__(self):
        base_path = os.getcwd()  # Menggantikan os.path.dirname(__file__)

        # Path untuk file data
        stopwords_path = os.path.join(base_path, "data/stopwords.txt")
        normalization_path = os.path.join(base_path, "data/kamuskatabaku.xlsx")
        news_dictionary_path = os.path.join(base_path, "data/news_dictionary.txt")

        # Memastikan semua file yang diperlukan ada
        self.ensure_files_exist([stopwords_path, normalization_path, news_dictionary_path])

        # Load stopwords
        with open(stopwords_path, "r", encoding="utf-8") as f:
            self.stopwords = set(f.read().splitlines())

        # Load kamus kata baku
        self.normalization_dict = pd.read_excel(normalization_path, header=None)
        self.normalization_dict = dict(zip(self.normalization_dict[0], self.normalization_dict[1]))

        # Load and normalize news media dictionary
        with open(news_dictionary_path, "r", encoding="utf-8") as f:
            self.news_media = set(normalize_media_name(line.strip()) for line in f.readlines())

    @staticmethod
    def ensure_files_exist(files):
        for file in files:
            if not os.path.exists(file):
                raise FileNotFoundError(f"Required file not found: {file}")

    @staticmethod
    def clean_text(text):
        return re.sub(r"([@#][A-Za-z0-9]+)|(\w+:\/\/\S+)|\d+|[^\w\s]|_", " ", text).strip()

    @staticmethod
    def tokenize_text(text):
        return word_tokenize(text)

    def remove_stopwords(self, tokens):
        return [token for token in tokens if token not in self.stopwords and token.isalpha()]

    def normalize_text(self, tokens):
        return [self.normalization_dict.get(token, token) for token in tokens]

    def detect_media_source(self, tokens, channel_title):
        normalized_title = normalize_media_name(channel_title)
        tokens_lower = [token.lower() for token in tokens]
        return any(token in self.news_media for token in tokens_lower) or (normalized_title in self.news_media)

    def preprocess(self, input_path, text_column="comment", channel_title_column="channel_title", output_path="output.xlsx"):
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input file not found at {input_path}")
        
        df = pd.read_excel(input_path)
        if text_column not in df.columns or channel_title_column not in df.columns:
            raise ValueError(f"Column '{text_column}' or '{channel_title_column}' not found in DataFrame.")

        df["Case_Folding"] = df[text_column].str.lower()
        df["Cleaned_Text"] = df["Case_Folding"].apply(self.clean_text)
        df = df.drop_duplicates(subset="Cleaned_Text", keep="first").reset_index(drop=True)
        df["Text_Tokenizing"] = df["Cleaned_Text"].apply(self.tokenize_text)
        df["Filtered_Text"] = df["Text_Tokenizing"].apply(self.remove_stopwords)
        df["Normalized_Text"] = df["Filtered_Text"].apply(self.normalize_text)
        df["Is_Media"] = df.apply(lambda x: self.detect_media_source(x["Filtered_Text"], x[channel_title_column]), axis=1)

        df.to_excel(output_path, index=False)
        return df