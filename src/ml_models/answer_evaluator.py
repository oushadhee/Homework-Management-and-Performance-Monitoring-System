"""
Answer Evaluator - Automatic grading and NLP-assisted evaluation
Handles both objective (MCQ) and subjective (text) answer evaluation
"""

import torch
from sentence_transformers import SentenceTransformer, util
from typing import Dict, List, Optional, Tuple
from loguru import logger
import re
import difflib


class AnswerEvaluator:
    """
    Evaluates student answers using various techniques:
    - Exact matching for MCQs
    - Semantic similarity for short answers
    - NLP-based evaluation for descriptive answers
    """
    
    def __init__(
        self,
        similarity_model: str = "all-MiniLM-L6-v2",
        similarity_threshold: float = 0.75,
        device: str = "cuda"
    ):
        """
        Initialize the answer evaluator
        
        Args:
            similarity_model: Sentence transformer model for semantic similarity
            similarity_threshold: Minimum similarity score for correct answers
            device: Device to run model on
        """
        self.similarity_threshold = similarity_threshold
        self.device = device
        
        logger.info(f"Loading similarity model: {similarity_model}")
        self.similarity_model = SentenceTransformer(similarity_model)
        if device == "cuda" and torch.cuda.is_available():
            self.similarity_model = self.similarity_model.to(device)
        
        logger.info("Answer evaluator initialized")
    
    def evaluate_mcq(
        self,
        student_answer: str,
        correct_answer: str
    ) -> Dict:
        """
        Evaluate Multiple Choice Question answer
        
        Args:
            student_answer: Student's selected option (A, B, C, or D)
            correct_answer: Correct option
            
        Returns:
            Evaluation result with score and feedback
        """
        student_answer = student_answer.strip().upper()
        correct_answer = correct_answer.strip().upper()
        
        is_correct = student_answer == correct_answer
        
        return {
            "is_correct": is_correct,
            "score": 1.0 if is_correct else 0.0,
            "max_score": 1.0,
            "feedback": "Correct!" if is_correct else f"Incorrect. The correct answer is {correct_answer}."
        }
    
    def evaluate_short_answer(
        self,
        student_answer: str,
        expected_answer: str,
        keywords: Optional[List[str]] = None
    ) -> Dict:
        """
        Evaluate short answer using semantic similarity and keyword matching
        
        Args:
            student_answer: Student's answer text
            expected_answer: Expected/model answer
            keywords: Important keywords that should be present
            
        Returns:
            Evaluation result with score and feedback
        """
        # Clean answers
        student_answer = self._clean_text(student_answer)
        expected_answer = self._clean_text(expected_answer)
        
        # Calculate semantic similarity
        similarity_score = self._calculate_similarity(student_answer, expected_answer)
        
        # Calculate keyword coverage if keywords provided
        keyword_score = 1.0
        if keywords:
            keyword_score = self._calculate_keyword_coverage(student_answer, keywords)
        
        # Combined score (70% similarity, 30% keywords)
        final_score = (similarity_score * 0.7) + (keyword_score * 0.3)
        
        # Determine if answer is acceptable
        is_correct = final_score >= self.similarity_threshold
        
        # Generate feedback
        feedback = self._generate_short_answer_feedback(
            similarity_score,
            keyword_score,
            is_correct
        )
        
        return {
            "is_correct": is_correct,
            "score": final_score,
            "max_score": 1.0,
            "similarity_score": similarity_score,
            "keyword_score": keyword_score,
            "feedback": feedback,
            "requires_manual_review": 0.6 <= final_score < self.similarity_threshold
        }
    
    def evaluate_descriptive(
        self,
        student_answer: str,
        key_points: List[str],
        expected_length: int = 100
    ) -> Dict:
        """
        Evaluate descriptive answer based on key points coverage and quality
        
        Args:
            student_answer: Student's descriptive answer
            key_points: List of key points that should be covered
            expected_length: Expected minimum word count
            
        Returns:
            Evaluation result with score and detailed feedback
        """
        # Clean answer
        student_answer = self._clean_text(student_answer)
        
        # Check length
        word_count = len(student_answer.split())
        length_score = min(word_count / expected_length, 1.0)
        
        # Calculate coverage of key points
        point_scores = []
        covered_points = []
        
        for point in key_points:
            similarity = self._calculate_similarity(student_answer, point)
            point_scores.append(similarity)
            if similarity >= 0.6:  # Lower threshold for key points
                covered_points.append(point)
        
        # Average key point coverage
        coverage_score = sum(point_scores) / len(point_scores) if point_scores else 0.0
        
        # Final score (40% length, 60% content coverage)
        final_score = (length_score * 0.4) + (coverage_score * 0.6)
        
        # Generate detailed feedback
        feedback = self._generate_descriptive_feedback(
            word_count,
            expected_length,
            len(covered_points),
            len(key_points),
            final_score
        )
        
        return {
            "score": final_score,
            "max_score": 1.0,
            "word_count": word_count,
            "length_score": length_score,
            "coverage_score": coverage_score,
            "covered_points": len(covered_points),
            "total_points": len(key_points),
            "feedback": feedback,
            "requires_manual_review": final_score < 0.7
        }
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate semantic similarity between two texts"""
        
        if not text1 or not text2:
            return 0.0
        
        # Encode texts
        embedding1 = self.similarity_model.encode(text1, convert_to_tensor=True)
        embedding2 = self.similarity_model.encode(text2, convert_to_tensor=True)
        
        # Calculate cosine similarity
        similarity = util.cos_sim(embedding1, embedding2).item()
        
        return max(0.0, min(1.0, similarity))  # Clamp between 0 and 1
    
    def _calculate_keyword_coverage(self, text: str, keywords: List[str]) -> float:
        """Calculate what percentage of keywords are present in text"""
        
        text_lower = text.lower()
        found_keywords = sum(1 for keyword in keywords if keyword.lower() in text_lower)
        
        return found_keywords / len(keywords) if keywords else 1.0
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters
        text = re.sub(r'[^\w\s.,!?;:\-\']', '', text)
        return text.strip()

    def _generate_short_answer_feedback(
        self,
        similarity_score: float,
        keyword_score: float,
        is_correct: bool
    ) -> str:
        """Generate feedback for short answer"""

        if is_correct:
            if similarity_score > 0.9:
                return "Excellent answer! Your response matches the expected answer very well."
            else:
                return "Good answer! Your response covers the main points."
        else:
            feedback_parts = []

            if similarity_score < 0.5:
                feedback_parts.append("Your answer doesn't fully address the question.")

            if keyword_score < 0.5:
                feedback_parts.append("Make sure to include key concepts in your answer.")

            feedback_parts.append("Please review the lesson material and try again.")

            return " ".join(feedback_parts)

    def _generate_descriptive_feedback(
        self,
        word_count: int,
        expected_length: int,
        covered_points: int,
        total_points: int,
        final_score: float
    ) -> str:
        """Generate detailed feedback for descriptive answer"""

        feedback_parts = []

        # Length feedback
        if word_count < expected_length * 0.5:
            feedback_parts.append(f"Your answer is too brief ({word_count} words). Aim for at least {expected_length} words.")
        elif word_count < expected_length:
            feedback_parts.append(f"Your answer could be more detailed ({word_count}/{expected_length} words).")
        else:
            feedback_parts.append(f"Good length ({word_count} words).")

        # Content coverage feedback
        coverage_percentage = (covered_points / total_points * 100) if total_points > 0 else 0

        if coverage_percentage >= 80:
            feedback_parts.append(f"Excellent coverage of key points ({covered_points}/{total_points}).")
        elif coverage_percentage >= 60:
            feedback_parts.append(f"Good coverage, but some key points are missing ({covered_points}/{total_points}).")
        else:
            feedback_parts.append(f"Several important points are missing ({covered_points}/{total_points} covered).")

        # Overall feedback
        if final_score >= 0.85:
            feedback_parts.append("Overall: Excellent work!")
        elif final_score >= 0.7:
            feedback_parts.append("Overall: Good effort!")
        else:
            feedback_parts.append("Overall: Needs improvement. Review the lesson and expand your answer.")

        return " ".join(feedback_parts)

