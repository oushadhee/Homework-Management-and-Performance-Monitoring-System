"""
Question Generator - Uses LLaMA 3.2 for generating homework questions
Fine-tuned Small Language Model for question generation
"""

import torch
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    BitsAndBytesConfig,
    pipeline
)
from peft import PeftModel, PeftConfig
from typing import List, Dict, Optional
from loguru import logger
import json
import re


class QuestionGenerator:
    """
    Generates structured questions from lesson content using LLaMA 3.2
    Supports MCQ, Short Answer, and Descriptive questions
    """
    
    def __init__(
        self,
        model_name: str = "meta-llama/Llama-3.2-3B",
        device: str = "cuda",
        use_4bit: bool = True,
        adapter_path: Optional[str] = None
    ):
        """
        Initialize the question generator
        
        Args:
            model_name: HuggingFace model name
            device: Device to run model on ('cuda' or 'cpu')
            use_4bit: Use 4-bit quantization for memory efficiency
            adapter_path: Path to fine-tuned LoRA adapter (if available)
        """
        self.device = device
        self.model_name = model_name
        
        logger.info(f"Loading model: {model_name}")
        
        # Configure quantization for memory efficiency
        if use_4bit and device == "cuda":
            bnb_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.float16,
                bnb_4bit_use_double_quant=True,
            )
        else:
            bnb_config = None
        
        # Load tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            trust_remote_code=True
        )
        self.tokenizer.pad_token = self.tokenizer.eos_token
        
        # Load base model
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            quantization_config=bnb_config,
            device_map="auto" if device == "cuda" else None,
            trust_remote_code=True,
            torch_dtype=torch.float16 if device == "cuda" else torch.float32
        )
        
        # Load fine-tuned adapter if available
        if adapter_path:
            logger.info(f"Loading fine-tuned adapter from: {adapter_path}")
            self.model = PeftModel.from_pretrained(self.model, adapter_path)
        
        self.model.eval()
        
        logger.info("Model loaded successfully")
    
    def generate_questions(
        self,
        lesson_content: str,
        keywords: List[str],
        num_mcq: int = 3,
        num_short: int = 2,
        num_descriptive: int = 1,
        difficulty: str = "intermediate"
    ) -> Dict[str, List[Dict]]:
        """
        Generate multiple types of questions from lesson content
        
        Args:
            lesson_content: The lesson text
            keywords: Important keywords from the lesson
            num_mcq: Number of MCQ questions to generate
            num_short: Number of short answer questions
            num_descriptive: Number of descriptive questions
            difficulty: Difficulty level (beginner, intermediate, advanced)
            
        Returns:
            Dictionary with question types as keys and lists of questions as values
        """
        questions = {
            "mcq": [],
            "short_answer": [],
            "descriptive": []
        }
        
        # Generate MCQs
        if num_mcq > 0:
            questions["mcq"] = self._generate_mcq(
                lesson_content, keywords, num_mcq, difficulty
            )
        
        # Generate Short Answer questions
        if num_short > 0:
            questions["short_answer"] = self._generate_short_answer(
                lesson_content, keywords, num_short, difficulty
            )
        
        # Generate Descriptive questions
        if num_descriptive > 0:
            questions["descriptive"] = self._generate_descriptive(
                lesson_content, keywords, num_descriptive, difficulty
            )
        
        return questions
    
    def _generate_mcq(
        self,
        lesson_content: str,
        keywords: List[str],
        num_questions: int,
        difficulty: str
    ) -> List[Dict]:
        """Generate Multiple Choice Questions"""
        
        prompt = self._create_mcq_prompt(lesson_content, keywords, difficulty)
        
        generated_text = self._generate_text(prompt, max_length=1500)
        
        # Parse the generated questions
        mcqs = self._parse_mcq_response(generated_text, num_questions)
        
        return mcqs
    
    def _generate_short_answer(
        self,
        lesson_content: str,
        keywords: List[str],
        num_questions: int,
        difficulty: str
    ) -> List[Dict]:
        """Generate Short Answer Questions"""

        prompt = self._create_short_answer_prompt(lesson_content, keywords, difficulty)

        generated_text = self._generate_text(prompt, max_length=1000)

        # Parse the generated questions
        questions = self._parse_short_answer_response(generated_text, num_questions)

        return questions

    def _generate_descriptive(
        self,
        lesson_content: str,
        keywords: List[str],
        num_questions: int,
        difficulty: str
    ) -> List[Dict]:
        """Generate Descriptive Questions"""

        prompt = self._create_descriptive_prompt(lesson_content, keywords, difficulty)

        generated_text = self._generate_text(prompt, max_length=800)

        # Parse the generated questions
        questions = self._parse_descriptive_response(generated_text, num_questions)

        return questions

    def _generate_text(self, prompt: str, max_length: int = 1024) -> str:
        """Generate text using the model"""

        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=2048
        ).to(self.device)

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_length,
                temperature=0.7,
                top_p=0.9,
                top_k=50,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )

        generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Remove the prompt from the output
        generated_text = generated_text[len(prompt):].strip()

        return generated_text

    def _create_mcq_prompt(self, lesson: str, keywords: List[str], difficulty: str) -> str:
        """Create prompt for MCQ generation"""

        keywords_str = ", ".join(keywords[:10])

        prompt = f"""You are an expert educator creating multiple-choice questions.

Lesson Content:
{lesson[:1000]}

Keywords: {keywords_str}
Difficulty: {difficulty}

Generate 3 multiple-choice questions based on the lesson. For each question:
1. Write a clear question
2. Provide 4 options (A, B, C, D)
3. Indicate the correct answer
4. Provide a brief explanation

Format:
Question 1: [question text]
A) [option A]
B) [option B]
C) [option C]
D) [option D]
Correct Answer: [A/B/C/D]
Explanation: [explanation]

Generate the questions:
"""
        return prompt

    def _create_short_answer_prompt(self, lesson: str, keywords: List[str], difficulty: str) -> str:
        """Create prompt for short answer generation"""

        keywords_str = ", ".join(keywords[:10])

        prompt = f"""You are an expert educator creating short answer questions.

Lesson Content:
{lesson[:1000]}

Keywords: {keywords_str}
Difficulty: {difficulty}

Generate 2 short answer questions that require 2-3 sentence responses. For each question:
1. Write a clear question
2. Provide the expected answer (2-3 sentences)

Format:
Question 1: [question text]
Answer: [expected answer]

Generate the questions:
"""
        return prompt

    def _create_descriptive_prompt(self, lesson: str, keywords: List[str], difficulty: str) -> str:
        """Create prompt for descriptive question generation"""

        keywords_str = ", ".join(keywords[:10])

        prompt = f"""You are an expert educator creating descriptive questions.

Lesson Content:
{lesson[:1000]}

Keywords: {keywords_str}
Difficulty: {difficulty}

Generate 1 descriptive question that requires a detailed paragraph response. Include:
1. A thought-provoking question
2. Key points that should be covered in the answer

Format:
Question: [question text]
Key Points: [bullet points of what should be covered]

Generate the question:
"""
        return prompt

    def _parse_mcq_response(self, text: str, num_questions: int) -> List[Dict]:
        """Parse MCQ questions from generated text"""

        questions = []
        # Simple parsing logic - in production, use more robust parsing
        question_blocks = re.split(r'Question \d+:', text)[1:]

        for block in question_blocks[:num_questions]:
            try:
                # Extract question text
                question_match = re.search(r'^(.+?)\n[A-D]\)', block, re.DOTALL)
                if not question_match:
                    continue

                question_text = question_match.group(1).strip()

                # Extract options
                options = re.findall(r'([A-D])\)\s*(.+?)(?=\n[A-D]\)|Correct Answer:|$)', block, re.DOTALL)

                # Extract correct answer
                correct_match = re.search(r'Correct Answer:\s*([A-D])', block)
                correct_answer = correct_match.group(1) if correct_match else 'A'

                # Extract explanation
                explanation_match = re.search(r'Explanation:\s*(.+?)(?=Question \d+:|$)', block, re.DOTALL)
                explanation = explanation_match.group(1).strip() if explanation_match else ""

                questions.append({
                    "question_text": question_text,
                    "options": [{"letter": opt[0], "text": opt[1].strip()} for opt in options],
                    "correct_answer": correct_answer,
                    "explanation": explanation
                })
            except Exception as e:
                logger.error(f"Error parsing MCQ: {e}")
                continue

        return questions

    def _parse_short_answer_response(self, text: str, num_questions: int) -> List[Dict]:
        """Parse short answer questions from generated text"""

        questions = []
        question_blocks = re.split(r'Question \d+:', text)[1:]

        for block in question_blocks[:num_questions]:
            try:
                parts = block.split('Answer:', 1)
                if len(parts) == 2:
                    questions.append({
                        "question_text": parts[0].strip(),
                        "expected_answer": parts[1].strip()
                    })
            except Exception as e:
                logger.error(f"Error parsing short answer: {e}")
                continue

        return questions

    def _parse_descriptive_response(self, text: str, num_questions: int) -> List[Dict]:
        """Parse descriptive questions from generated text"""

        questions = []

        try:
            question_match = re.search(r'Question:\s*(.+?)(?=Key Points:|$)', text, re.DOTALL)
            key_points_match = re.search(r'Key Points:\s*(.+?)$', text, re.DOTALL)

            if question_match:
                questions.append({
                    "question_text": question_match.group(1).strip(),
                    "key_points": key_points_match.group(1).strip() if key_points_match else ""
                })
        except Exception as e:
            logger.error(f"Error parsing descriptive question: {e}")

        return questions

