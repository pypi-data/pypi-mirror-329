import os
import json
import pandas as pd
import re
from nltk.tokenize import word_tokenize
import nltk
from PIL import Image, ImageTk
import tkinter as tk

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
        # Tentukan base path relatif terhadap file ini
        base_path = os.path.dirname(os.path.abspath(__file__))

        # Path untuk file data
        self.stopwords_path = os.path.join(base_path, "data", "stopwords.txt")
        self.normalization_path = os.path.join(base_path, "data", "kamuskatabaku.xlsx")
        self.news_dictionary_path = os.path.join(base_path, "data", "news_dictionary.txt")
        self.profile_path = os.path.join(base_path, "data", "profile.json")

        # Memastikan semua file yang diperlukan ada
        self.ensure_files_exist([self.stopwords_path, self.normalization_path, self.news_dictionary_path, self.profile_path])

        # Load stopwords
        with open(self.stopwords_path, "r", encoding="utf-8") as f:
            self.stopwords = set(f.read().splitlines())

        # Load kamus kata baku
        self.normalization_dict = pd.read_excel(self.normalization_path, header=None)
        self.normalization_dict = dict(zip(self.normalization_dict[0], self.normalization_dict[1]))

        # Load news media dictionary
        with open(self.news_dictionary_path, "r", encoding="utf-8") as f:
            self.news_media = set(normalize_media_name(line.strip()) for line in f.readlines())

        # Load user profile
        with open(self.profile_path, 'r') as file:
            self.profile_data = json.load(file)

    @staticmethod
    def ensure_files_exist(files):
        """Ensure all required files exist."""
        for file in files:
            if not os.path.exists(file):
                raise FileNotFoundError(f"Required file not found: {file}")

    @staticmethod
    def clean_text(text):
        """Clean text by removing URLs, numbers, special characters, and usernames."""
        return re.sub(r"([@#][A-Za-z0-9]+)|(\w+:\/\/\S+)|\d+|[^\w\s]|_", " ", text).strip()

    @staticmethod
    def tokenize_text(text):
        """Tokenize text using NLTK's word_tokenize."""
        return word_tokenize(text)

    def remove_stopwords(self, tokens):
        """Remove stopwords from the list of tokens."""
        return [token for token in tokens if token not in self.stopwords and token.isalpha()]

    def normalize_text(self, tokens):
        """Normalize text by replacing words with their base forms according to the normalization dictionary."""
        return [self.normalization_dict.get(token, token) for token in tokens]

    def detect_media_source(self, tokens, channel_title):
        """Detect if the channel title or any tokens are in the set of known media sources."""
        normalized_title = normalize_media_name(channel_title)
        tokens_lower = [token.lower() for token in tokens]
        return any(token in self.news_media for token in tokens_lower) or (normalized_title in self.news_media)

    def preprocess(self, input_path, text_column="comment", channel_title_column="channel_title", output_path="output.xlsx"):
        """Preprocess the dataset by cleaning, tokenizing, and normalizing the text."""
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

    def display_user_profile(self):
        """Display the user profile information in a simple window using tkinter, including photo."""
        window = tk.Tk()
        window.title("User Profile")

        # Load and display the photo
        image_path = self.profile_data['photo']
        img = Image.open(image_path)
        photo = ImageTk.PhotoImage(img)
        label_photo = tk.Label(window, image=photo)
        label_photo.image = photo  # keep a reference!
        label_photo.pack()

        label_name = tk.Label(window, text=f"Name: {self.profile_data['name']}")
        label_name.pack()

        label_title = tk.Label(window, text=f"Title: {self.profile_data['title']}")
        label_title.pack()

        label_address = tk.Label(window, text=f"Address: {self.profile_data['address']}")
        label_address.pack()

        window.mainloop()

# Example usage
if __name__ == "__main__":
    app = AsroPreprocessing()
    app.display_user_profile()
