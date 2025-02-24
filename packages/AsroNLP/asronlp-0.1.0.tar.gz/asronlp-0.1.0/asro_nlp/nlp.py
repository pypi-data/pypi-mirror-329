import pandas as pd
import re
from nltk.tokenize import word_tokenize
import os
import nltk
import time

# Ensure NLTK tokenizer is available
nltk.download('punkt')

def normalize_media_name(name):
    """Normalize media names by removing spaces and special characters except '.', and converting to lowercase."""
    name = re.sub(r"[^\w\d\s.]", '', name)
    name = re.sub(r"\s+", '', name)
    return name.lower()

class AsroNLP:
    def __init__(self, base_path=None):
        """Initialize paths for data files and lexicons."""
        if base_path is None:
            base_path = os.path.dirname(os.path.abspath(__file__))

        self.stopwords_path = os.path.join(base_path, "data/stopwords.txt")
        self.normalization_path = os.path.join(base_path, "data/kamuskatabaku.xlsx")
        self.news_dictionary_path = os.path.join(base_path, "data/news_dictionary.txt")
        self.root_words_path = os.path.join(base_path, "data/kata-dasar.txt")
        self.lexicon_positive_path = os.path.join(base_path, "data/kamus_positive.xlsx")
        self.lexicon_negative_path = os.path.join(base_path, "data/kamus_negative.xlsx")

        self.load_resources()

    def load_resources(self):
        """Load necessary resources from files."""
        self.ensure_files_exist([
            self.stopwords_path,
            self.normalization_path,
            self.news_dictionary_path,
            self.root_words_path,
            self.lexicon_positive_path,
            self.lexicon_negative_path
        ])

        with open(self.stopwords_path, "r", encoding="utf-8") as f:
            self.stopwords = set(f.read().splitlines())

        self.normalization_dict = pd.read_excel(self.normalization_path, header=None)
        self.normalization_dict = dict(zip(self.normalization_dict[0], self.normalization_dict[1]))

        with open(self.news_dictionary_path, "r", encoding="utf-8") as f:
            self.news_media = set(normalize_media_name(line.strip()) for line in f.readlines())

        self.lexicon_positive = pd.read_excel(self.lexicon_positive_path)
        self.lexicon_positive_dict = {row[0].lower(): row[1] for index, row in self.lexicon_positive.iterrows()}

        self.lexicon_negative = pd.read_excel(self.lexicon_negative_path)
        self.lexicon_negative_dict = {row[0].lower(): row[1] for index, row in self.lexicon_negative.iterrows()}

    def preprocess_and_optionally_stem_and_analyze(self, input_path, text_column="comment", channel_title_column="channel_title", output_path="output.xlsx"):
        df = pd.read_excel(input_path)
        df["Case_Folding"] = df[text_column].str.lower()
        df["Cleaned_Text"] = df["Case_Folding"].apply(self.clean_text)
        df["Text_Tokenizing"] = df["Cleaned_Text"].apply(self.tokenize_text)
        df["Filtered_Text"] = df["Text_Tokenizing"].apply(self.remove_stopwords)
        df["Normalized_Text"] = df["Filtered_Text"].apply(self.normalize_text)
        df["Is_Media"] = df.apply(lambda x: self.detect_media_source(x["Filtered_Text"], x[channel_title_column]), axis=1)

        if input("Do you want to proceed with stemming? (yes/no): ").lower() == 'yes':
            df['Stemmed_Text'] = df['Normalized_Text'].apply(lambda tokens: [self.custom_stemmer(token) for token in tokens])
            text_for_analysis = 'Stemmed_Text'
        else:
            text_for_analysis = 'Normalized_Text'

        # Sentiment analysis
        if input("Do you want to perform sentiment analysis? (yes/no): ").lower() == 'yes':
            df['PolarityScore'], df['Sentiment'] = zip(*df[text_for_analysis].apply(self.sentiment_analysis_lexicon_indonesia))
            output_filename = output_path.replace('.xlsx', '_sentiment.xlsx')
            df.to_excel(output_filename, index=False)
            print(f"Processed data with sentiment analysis saved to {output_filename}")

        return df

    def sentiment_analysis_lexicon_indonesia(self, tokens):
        """Perform sentiment analysis based on tokens."""
        score = 0
        for word in tokens:
            word = word.lower()
            if word in self.lexicon_positive_dict:
                score += self.lexicon_positive_dict[word]
            if word in self.lexicon_negative_dict:
                score -= self.lexicon_negative_dict[word]
        return score, 'Positive' if score > 0 else 'Negative' if score < 0 else 'Neutral'

    def custom_stemmer(self, token):
        """Placeholder for a custom stemming logic."""
        return token  # Replace with actual stemming logic if necessary

    def detect_media_source(self, tokens, channel_title):
        """Check if text mentions any predefined media names."""
        normalized_channel_title = normalize_media_name(channel_title)
        token_set = set(normalize_media_name(token) for token in tokens)
        return any(media in token_set or normalized_channel_title == media for media in self.news_media)

if __name__ == "__main__":
    # Example usage can be added here for direct execution
    pass
