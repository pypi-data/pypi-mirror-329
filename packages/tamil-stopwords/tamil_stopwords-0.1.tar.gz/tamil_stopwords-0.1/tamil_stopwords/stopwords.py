import os

def get_tamil_stopwords():
    """Returns a set of Tamil stopwords."""
    with open(os.path.join(os.path.dirname(__file__), "tamil_stopwords_cleaned.txt"), "r", encoding="utf-8") as f:
        return set(f.read().splitlines())
