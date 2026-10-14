"""
Core NLP Processing Pipeline for Text Processing & Analysis.
Integrates spaCy / TextBlob / Textstat / Scikit-Learn / NetworkX.
"""

import os
import sys
import site

# Ensure user site packages on Windows are registered
user_site = site.USER_SITE
if user_site and os.path.exists(user_site) and user_site not in sys.path:
    site.addsitedir(user_site)

import re
import math
from collections import Counter
from typing import Dict, Any, List, Tuple
import pandas as pd
import numpy as np

import textstat
from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
import networkx as nx

# Safe import for spaCy
try:
    import spacy
    try:
        nlp = spacy.load("en_core_web_sm")
    except Exception:
        # Fallback blank English model
        nlp = spacy.blank("en")
        if "sentencizer" not in nlp.pipe_names:
            nlp.add_pipe("sentencizer")
except ImportError:
    nlp = None

def clean_text(text: str) -> str:
    """Normalize whitespace and strip control characters."""
    if not text:
        return ""
    text = re.sub(r'\r\n', '\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def get_sentences(text: str) -> List[str]:
    """Split text into sentences using spaCy or regex fallback."""
    text = clean_text(text)
    if not text:
        return []
    
    if nlp is not None:
        try:
            doc = nlp(text)
            sentences = [sent.text.strip() for sent in doc.sents if sent.text.strip()]
            if sentences:
                return sentences
        except Exception:
            pass
            
    # Regex fallback sentence splitter
    raw_sents = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in raw_sents if s.strip()]

def get_tokens(text: str) -> List[Dict[str, str]]:
    """Perform tokenization, POS tagging, and lemmatization."""
    text = clean_text(text)
    tokens_info = []
    
    if nlp is not None and nlp.has_pipe("tok2tag") if hasattr(nlp, "has_pipe") else False:
        try:
            doc = nlp(text)
            for token in doc:
                if not token.is_space:
                    tokens_info.append({
                        "text": token.text,
                        "lemma": token.lemma_,
                        "pos": token.pos_,
                        "tag": token.tag_,
                        "is_stop": token.is_stop,
                        "is_punct": token.is_punct
                    })
            if tokens_info:
                return tokens_info
        except Exception:
            pass
            
    # TextBlob / Pure Python fallback
    blob = TextBlob(text)
    stop_words = set(["the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by", "is", "it", "this", "that"])
    for word, tag in blob.tags:
        cleaned_word = re.sub(r'[^\w\s]', '', word)
        if cleaned_word:
            pos_label = "NOUN" if tag.startswith("NN") else ("VERB" if tag.startswith("VB") else ("ADJ" if tag.startswith("JJ") else ("ADV" if tag.startswith("RB") else "OTHER")))
            tokens_info.append({
                "text": word,
                "lemma": word.lower(),
                "pos": pos_label,
                "tag": tag,
                "is_stop": word.lower() in stop_words,
                "is_punct": bool(re.match(r'^[^\w\s]+$', word))
            })
            
    return tokens_info

def extract_named_entities(text: str) -> List[Dict[str, str]]:
    """Extract Named Entities (NER) using spaCy or Pattern matching."""
    entities = []
    if nlp is not None:
        try:
            doc = nlp(text)
            for ent in doc.ents:
                entities.append({
                    "text": ent.text,
                    "label": ent.label_,
                    "explanation": spacy.explain(ent.label_) if hasattr(spacy, "explain") else ent.label_
                })
            if entities:
                return entities
        except Exception:
            pass
            
    # Fallback basic capitalised noun phrases / entities
    matches = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
    counts = Counter(matches)
    for ent_text, _ in counts.most_common(15):
        if ent_text.lower() not in ["the", "a", "an", "this", "that"]:
            entities.append({
                "text": ent_text,
                "label": "PROPN",
                "explanation": "Proper Noun / Entity"
            })
    return entities

def compute_readability_metrics(text: str) -> Dict[str, Any]:
    """Calculate comprehensive text metrics & readability indices using textstat & textblob."""
    text = clean_text(text)
    if not text:
        return {
            "flesch_reading_ease": 100.0,
            "flesch_kincaid_grade": 0.0,
            "gunning_fog": 0.0,
            "coleman_liau": 0.0,
            "automated_readability_index": 0.0,
            "word_count": 0,
            "sentence_count": 0,
            "syllable_count": 0,
            "avg_words_per_sentence": 0.0,
            "avg_syllables_per_word": 0.0,
            "reading_time_seconds": 0.0,
            "sentiment_polarity": 0.0,
            "sentiment_subjectivity": 0.0
        }
        
    try:
        fre = textstat.flesch_reading_ease(text)
        fkgl = textstat.flesch_kincaid_grade(text)
        fog = textstat.gunning_fog(text)
        coleman = textstat.coleman_liau_index(text)
        ari = textstat.automated_readability_index(text)
    except Exception:
        fre, fkgl, fog, coleman, ari = 60.0, 8.0, 9.0, 8.0, 8.0
        
    sentences = get_sentences(text)
    sentence_count = max(len(sentences), 1)
    
    words = re.findall(r'\b\w+\b', text)
    word_count = max(len(words), 1)
    
    syllable_count = sum([textstat.syllable_count(w) for w in words]) if hasattr(textstat, "syllable_count") else int(word_count * 1.5)
    
    avg_words_per_sent = round(word_count / sentence_count, 2)
    avg_syllables_per_word = round(syllable_count / word_count, 2)
    
    # Average adult reading speed: 200 words per minute
    reading_time_seconds = round((word_count / 200) * 60, 1)
    
    blob = TextBlob(text)
    polarity = round(blob.sentiment.polarity, 2)
    subjectivity = round(blob.sentiment.subjectivity, 2)
    
    return {
        "flesch_reading_ease": round(fre, 1),
        "flesch_kincaid_grade": round(fkgl, 1),
        "gunning_fog": round(fog, 1),
        "coleman_liau": round(coleman, 1),
        "automated_readability_index": round(ari, 1),
        "word_count": word_count,
        "sentence_count": sentence_count,
        "syllable_count": syllable_count,
        "avg_words_per_sentence": avg_words_per_sent,
        "avg_syllables_per_word": avg_syllables_per_word,
        "reading_time_seconds": reading_time_seconds,
        "sentiment_polarity": polarity,
        "sentiment_subjectivity": subjectivity
    }

def extract_ngrams(text: str, n: int = 2, top_k: int = 10) -> List[Tuple[str, int]]:
    """Extract top N-grams (unigrams, bigrams, trigrams)."""
    words = [w.lower() for w in re.findall(r'\b[a-zA-Z]{3,}\b', text)]
    stop_words = set(["the", "and", "for", "that", "this", "with", "you", "are", "have", "from", "not", "your", "will", "all"])
    filtered = [w for w in words if w not in stop_words]
    
    if len(filtered) < n:
        return []
        
    ngrams = [" ".join(filtered[i:i+n]) for i in range(len(filtered)-n+1)]
    counts = Counter(ngrams)
    return counts.most_common(top_k)

def extract_keywords_tfidf(text: str, top_k: int = 10) -> List[Tuple[str, float]]:
    """Extract top keywords using TF-IDF vectorizer."""
    sentences = get_sentences(text)
    if not sentences or len(sentences) < 1:
        words = [w.lower() for w in re.findall(r'\b[a-zA-Z]{4,}\b', text)]
        counts = Counter(words)
        return [(w, float(c)) for w, c in counts.most_common(top_k)]
        
    try:
        vectorizer = TfidfVectorizer(stop_words='english', max_features=top_k*2)
        tfidf_matrix = vectorizer.fit_transform(sentences)
        feature_names = vectorizer.get_feature_names_out()
        scores = tfidf_matrix.sum(axis=0).A1
        keyword_scores = list(zip(feature_names, scores))
        keyword_scores.sort(key=lambda x: x[1], reverse=True)
        return [(kw, round(score, 3)) for kw, score in keyword_scores[:top_k]]
    except Exception:
        words = [w.lower() for w in re.findall(r'\b[a-zA-Z]{4,}\b', text)]
        counts = Counter(words)
        return [(w, float(c)) for w, c in counts.most_common(top_k)]

def build_cooccurrence_graph(text: str, top_n_words: int = 15) -> nx.Graph:
    """Build word co-occurrence NetworkX graph for visualization."""
    words = [w.lower() for w in re.findall(r'\b[a-zA-Z]{4,}\b', text)]
    stop_words = set(["this", "that", "with", "from", "have", "they", "will", "your", "were", "been", "their"])
    filtered = [w for w in words if w not in stop_words]
    
    counts = Counter(filtered)
    top_words = set([w for w, _ in counts.most_common(top_n_words)])
    
    G = nx.Graph()
    for word in top_words:
        G.add_node(word, size=counts[word])
        
    window_size = 4
    for i in range(len(filtered) - window_size + 1):
        window = filtered[i:i+window_size]
        for w1 in window:
            for w2 in window:
                if w1 in top_words and w2 in top_words and w1 != w2:
                    if G.has_edge(w1, w2):
                        G[w1][w2]['weight'] += 1
                    else:
                        G.add_edge(w1, w2, weight=1)
    return G

def extract_topics(text: str, num_topics: int = 3) -> List[Dict[str, Any]]:
    """Perform NMF Topic Modeling over document sentences."""
    sentences = get_sentences(text)
    if len(sentences) < 3:
        return [{"topic_id": 1, "words": [w for w, _ in extract_keywords_tfidf(text, 5)]}]
        
    try:
        vectorizer = TfidfVectorizer(stop_words='english', max_features=100)
        tfidf = vectorizer.fit_transform(sentences)
        feature_names = vectorizer.get_feature_names_out()
        
        nmf = NMF(n_components=min(num_topics, len(sentences)), random_state=42)
        nmf.fit(tfidf)
        
        topics = []
        for idx, topic in enumerate(nmf.components_):
            top_features_ind = topic.argsort()[:-6:-1]
            top_words = [feature_names[i] for i in top_features_ind]
            topics.append({
                "topic_id": idx + 1,
                "words": top_words
            })
        return topics
    except Exception:
        return [{"topic_id": 1, "words": [w for w, _ in extract_keywords_tfidf(text, 5)]}]
