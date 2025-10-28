from sklearn.feature_extraction.text import TfidfVectorizer

def extract_keywords(text, n=10):
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf = vectorizer.fit_transform([text])
    scores = list(zip(vectorizer.get_feature_names_out(), tfidf.toarray()[0]))
    sorted_keywords = sorted(scores, key=lambda x: x[1], reverse=True)
    return [k for k, v in sorted_keywords[:n]]
