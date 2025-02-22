import pandas as pd
import re
from nltk.tokenize import word_tokenize
import os

class AsroPreprocessing:
    def __init__(self):
        base_path = os.path.dirname(__file__)

        # Load stopwords dari file bawaan library
        stopwords_path = os.path.join(base_path, "data/stopwords.txt")
        with open(stopwords_path, "r", encoding="utf-8") as f:
            self.stopwords = set(f.read().splitlines())

        # Load kamus kata baku dari file bawaan library
        normalization_path = os.path.join(base_path, "data/kamuskatabaku.xlsx")
        self.normalization_dict = pd.read_excel(normalization_path, header=None)
        self.normalization_dict = dict(zip(self.normalization_dict[0], self.normalization_dict[1]))

        # Load news media dictionary
        news_dictionary_path = os.path.join(base_path, "data/news_dictionary.txt")
        with open(news_dictionary_path, "r", encoding="utf-8") as f:
            self.news_media = set(f.read().splitlines())

    @staticmethod
    def clean_text(text):
        text = re.sub(r"([@#][A-Za-z0-9]+)|(\w+:\/\/\S+)|\d+|[^\w\s]|_", " ", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    @staticmethod
    def tokenize_text(text):
        return word_tokenize(text)

    def remove_stopwords(self, tokens):
        return [token for token in tokens if token not in self.stopwords and token.isalpha()]

    def normalize_text(self, tokens):
        return [self.normalization_dict.get(token, token) for token in tokens]

    def detect_media_source(self, tokens, channel_title):
        # Detect if tokens contain any news media names or the channel title is a known media source
        return any(token in self.news_media for token in tokens) or (channel_title in self.news_media)

    def preprocess(self, input_path, text_column="comment", channel_title_column="channel_title", output_path="output.xlsx"):
        df = pd.read_excel(input_path)
        if text_column not in df.columns or channel_title_column not in df.columns:
            raise ValueError(f"Kolom '{text_column}' atau '{channel_title_column}' tidak ditemukan dalam DataFrame.")

        df["Case_Folding"] = df[text_column].str.lower()
        df["Cleaned_Text"] = df["Case_Folding"].apply(self.clean_text)
        df = df.drop_duplicates(subset="Cleaned_Text", keep="first").reset_index(drop=True)
        df["Text_Tokenizing"] = df["Cleaned_Text"].apply(self.tokenize_text)
        df["Filtered_Text"] = df["Text_Tokenizing"].apply(self.remove_stopwords)
        df["Normalized_Text"] = df["Filtered_Text"].apply(self.normalize_text)
        df["Is_Media"] = df.apply(lambda x: self.detect_media_source(x["Filtered_Text"], x[channel_title_column]), axis=1)

        df.to_excel(output_path, index=False)
        return df
