import pandas as pd
import re
from nltk.tokenize import word_tokenize
import os
import sys
import nltk

# Ensure that the necessary NLTK resources are available
nltk.download('punkt')

def normalize_media_name(name):
    """Normalize media names by removing spaces, special characters except '.', and converting to lowercase."""
    name = re.sub(r"[^\w\d\s.]", '', name)  # Remove special chars except dot
    name = re.sub(r"\s+", '', name)  # Remove spaces
    return name.lower()

class AsroPreprocessing:
    def __init__(self, base_path=None):
        # Set base path to the directory containing this script/module, assuming the data folder is in the same directory
        if base_path is None:
            base_path = os.path.dirname(os.path.abspath(__file__))

        # Paths for data files
        self.stopwords_path = os.path.join(base_path, "data/stopwords.txt")
        self.normalization_path = os.path.join(base_path, "data/kamuskatabaku.xlsx")
        self.news_dictionary_path = os.path.join(base_path, "data/news_dictionary.txt")

        self.load_resources()

    def load_resources(self):
        """Load necessary resources from files."""
        self.ensure_files_exist([self.stopwords_path, self.normalization_path, self.news_dictionary_path])

        with open(self.stopwords_path, "r", encoding="utf-8") as f:
            self.stopwords = set(f.read().splitlines())

        self.normalization_dict = pd.read_excel(self.normalization_path, header=None)
        self.normalization_dict = dict(zip(self.normalization_dict[0], self.normalization_dict[1]))

        with open(self.news_dictionary_path, "r", encoding="utf-8") as f:
            self.news_media = set(normalize_media_name(line.strip()) for line in f.readlines())

    @staticmethod
    def ensure_files_exist(files):
        for file in files:
            if not os.path.exists(file):
                raise FileNotFoundError(f"Required file not found: {file}")

    @staticmethod
    def clean_text(text):
        """Clean text by removing URLs, numbers, special characters, etc."""
        return re.sub(r"([@#][A-Za-z0-9]+)|(\w+:\/\/\S+)|\d+|[^\w\s]|_", " ", text).strip()

    @staticmethod
    def tokenize_text(text):
        """Tokenize text using the NLTK library."""
        return word_tokenize(text)

    def remove_stopwords(self, tokens):
        """Remove stopwords from a list of tokens."""
        return [token for token in tokens if token not in self.stopwords and token.isalpha()]

    def normalize_text(self, tokens):
        """Normalize text using a predefined normalization dictionary."""
        return [self.normalization_dict.get(token, token) for token in tokens]

    def detect_media_source(self, tokens, channel_title):
        """Detect if the tokens or title indicate a media source."""
        normalized_title = normalize_media_name(channel_title)
        tokens_lower = [token.lower() for token in tokens]
        return any(token in self.news_media for token in tokens_lower) or (normalized_title in self.news_media)

    def preprocess(self, input_path, text_column="comment", channel_title_column="channel_title", output_path="output.xlsx"):
        """Process the input Excel file and output a cleaned version."""
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
