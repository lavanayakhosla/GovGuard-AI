import pdfplumber
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def analyze(paths):
    texts = []
    for p in paths:
        with pdfplumber.open(p) as pdf:
            text = "".join(page.extract_text() or "" for page in pdf.pages)
            texts.append(text)

    tfidf = TfidfVectorizer(stop_words="english")
    mat = tfidf.fit_transform(texts)
    return cosine_similarity(mat).tolist()
