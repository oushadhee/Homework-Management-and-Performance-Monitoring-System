"""
Lesson Processor - NLP-based lesson understanding and keyword extraction
Uses spaCy and NLTK for text processing and analysis
"""

import spacy
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from typing import List, Dict, Tuple, Optional
import re
from collections import Counter
from loguru import logger


class LessonProcessor:
    """
    Processes lesson content to extract topics, keywords, and key concepts
    using NLP techniques
    """
    
    def __init__(self, language: str = "en"):
        """
        Initialize the lesson processor
        
        Args:
            language: Language code (default: 'en' for English)
        """
        self.language = language
        
        # Load spaCy model
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            logger.warning("spaCy model not found. Downloading...")
            import subprocess
            subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
            self.nlp = spacy.load("en_core_web_sm")
        
        # Download required NLTK data
        try:
            self.stop_words = set(stopwords.words('english'))
        except LookupError:
            nltk.download('stopwords')
            nltk.download('punkt')
            nltk.download('averaged_perceptron_tagger')
            self.stop_words = set(stopwords.words('english'))
    
    def process_lesson(self, lesson_text: str) -> Dict:
        """
        Process lesson text and extract structured information
        
        Args:
            lesson_text: Raw lesson content
            
        Returns:
            Dictionary containing extracted information
        """
        # Clean text
        cleaned_text = self._clean_text(lesson_text)
        
        # Process with spaCy
        doc = self.nlp(cleaned_text)
        
        # Extract information
        topics = self._extract_topics(doc)
        keywords = self._extract_keywords(doc)
        key_concepts = self._extract_key_concepts(doc)
        entities = self._extract_entities(doc)
        difficulty = self._estimate_difficulty(doc)
        
        return {
            "topics": topics,
            "keywords": keywords,
            "key_concepts": key_concepts,
            "entities": entities,
            "difficulty_level": difficulty,
            "sentence_count": len(list(doc.sents)),
            "word_count": len([token for token in doc if not token.is_punct])
        }
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep punctuation
        text = re.sub(r'[^\w\s.,!?;:\-\']', '', text)
        return text.strip()
    
    def _extract_topics(self, doc) -> List[str]:
        """Extract main topics from the document"""
        # Use noun chunks as potential topics
        topics = []
        for chunk in doc.noun_chunks:
            if len(chunk.text.split()) >= 2:  # Multi-word topics
                topics.append(chunk.text.lower())
        
        # Get most common topics
        topic_counts = Counter(topics)
        return [topic for topic, _ in topic_counts.most_common(10)]
    
    def _extract_keywords(self, doc) -> List[Dict]:
        """Extract important keywords with scores"""
        keywords = []
        
        for token in doc:
            # Filter: nouns, proper nouns, adjectives
            if token.pos_ in ['NOUN', 'PROPN', 'ADJ'] and not token.is_stop:
                keywords.append({
                    "keyword": token.text.lower(),
                    "pos": token.pos_,
                    "lemma": token.lemma_.lower()
                })
        
        # Count frequency
        keyword_counts = Counter([kw['keyword'] for kw in keywords])
        
        # Return top keywords with importance scores
        result = []
        max_count = max(keyword_counts.values()) if keyword_counts else 1
        
        for keyword, count in keyword_counts.most_common(20):
            result.append({
                "keyword": keyword,
                "importance_score": round(count / max_count, 2),
                "frequency": count
            })
        
        return result
    
    def _extract_key_concepts(self, doc) -> List[str]:
        """Extract key concepts (important noun phrases)"""
        concepts = []
        
        for chunk in doc.noun_chunks:
            # Filter out short or common phrases
            if (len(chunk.text.split()) >= 2 and 
                not all(token.is_stop for token in chunk)):
                concepts.append(chunk.text.lower())
        
        # Get unique concepts
        concept_counts = Counter(concepts)
        return [concept for concept, _ in concept_counts.most_common(15)]
    
    def _extract_entities(self, doc) -> List[Dict]:
        """Extract named entities"""
        entities = []
        for ent in doc.ents:
            entities.append({
                "text": ent.text,
                "label": ent.label_,
                "description": spacy.explain(ent.label_)
            })
        return entities
    
    def _estimate_difficulty(self, doc) -> str:
        """
        Estimate difficulty level based on text complexity
        
        Returns:
            'beginner', 'intermediate', or 'advanced'
        """
        # Calculate average word length
        words = [token.text for token in doc if token.is_alpha]
        avg_word_length = sum(len(word) for word in words) / len(words) if words else 0
        
        # Calculate average sentence length
        sentences = list(doc.sents)
        avg_sent_length = len(words) / len(sentences) if sentences else 0
        
        # Simple heuristic
        if avg_word_length < 5 and avg_sent_length < 15:
            return "beginner"
        elif avg_word_length < 7 and avg_sent_length < 25:
            return "intermediate"
        else:
            return "advanced"

