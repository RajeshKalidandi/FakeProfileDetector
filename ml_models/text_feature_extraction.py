import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.sentiment import SentimentIntensityAnalyzer
from gensim import corpora
from gensim.models import LdaMulticore
from gensim.parsing.preprocessing import STOPWORDS
from gensim.utils import simple_preprocess
import nltk
from textblob import TextBlob
import language_tool_python

# Initialize LanguageTool for grammar checking
language_tool = language_tool_python.LanguageTool('en-US')

def preprocess(text):
    result = []
    for token in simple_preprocess(text):
        if token not in STOPWORDS and len(token) > 3:
            result.append(token)
    return result

def extract_text_features(bio, posts):
    features = {}
    
    # Combine bio and posts
    all_text = bio + ' ' + ' '.join(posts)
    
    # TF-IDF Vectorization
    tfidf = TfidfVectorizer(max_features=100)
    tfidf_features = tfidf.fit_transform([all_text]).toarray()[0]
    for i, value in enumerate(tfidf_features):
        features[f'tfidf_{i}'] = value
    
    # Sentiment Analysis
    sia = SentimentIntensityAnalyzer()
    sentiment_scores = sia.polarity_scores(all_text)
    features.update(sentiment_scores)
    
    # Topic Modeling
    processed_posts = [preprocess(post) for post in posts]
    dictionary = corpora.Dictionary(processed_posts)
    corpus = [dictionary.doc2bow(text) for text in processed_posts]
    
    lda_model = LdaMulticore(corpus=corpus, id2word=dictionary, num_topics=5)
    topics = lda_model.get_document_topics(corpus)
    for i in range(5):
        features[f'topic_{i}'] = max([topic[1] for topic in topics if topic[0] == i], default=0)
    
    # Named Entity Recognition
    tokens = nltk.word_tokenize(all_text)
    pos_tags = nltk.pos_tag(tokens)
    named_entities = nltk.ne_chunk(pos_tags)
    ner_counts = {}
    for chunk in named_entities:
        if hasattr(chunk, 'label'):
            ner_counts[chunk.label()] = ner_counts.get(chunk.label(), 0) + 1
    features.update(ner_counts)
    
    # Spelling and Grammar Check
    blob = TextBlob(all_text)
    features['spelling_errors'] = len(blob.correct().split()) - len(blob.split())
    
    grammar_errors = language_tool.check(all_text)
    features['grammar_errors'] = len(grammar_errors)
    
    return features

def extract_profile_features(profile_data):
    bio = profile_data.get('bio', '')
    posts = profile_data.get('posts', [])
    
    text_features = extract_text_features(bio, posts)
    
    # Add other profile features
    additional_features = {
        'followers_count': profile_data.get('followers_count', 0),
        'following_count': profile_data.get('following_count', 0),
        'posts_count': len(posts),
        'account_age_days': profile_data.get('account_age_days', 0),
    }
    
    return {**text_features, **additional_features}
