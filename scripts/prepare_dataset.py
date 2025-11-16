"""
Dataset preparation script for the homework management system
Handles data collection, cleaning, and formatting
"""

import json
import os
import re
from pathlib import Path
from typing import List, Dict
import random
from datetime import datetime


class DatasetPreparator:
    """Prepare datasets for model training"""
    
    def __init__(self, base_path: str = "./data"):
        self.base_path = Path(base_path)
        self.raw_path = self.base_path / "raw"
        self.processed_path = self.base_path / "processed"
        
        # Create directories
        self._create_directories()
    
    def _create_directories(self):
        """Create necessary directory structure"""
        subjects = ["mathematics", "science", "english", "history", "health_science"]

        directories = [
            self.raw_path / "responses",
            self.processed_path / "train",
            self.processed_path / "validation",
            self.processed_path / "test",
        ]

        # Add subject-specific directories
        for subject in subjects:
            directories.append(self.raw_path / "lessons" / subject)
            directories.append(self.raw_path / "questions" / subject)

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

        print(f"✓ Created directory structure at {self.base_path}")
    
    def generate_sample_lessons(self, subject: str, count: int = 100):
        """
        Generate sample lesson data for prototyping
        In production, replace with actual data collection
        """
        
        templates = {
            "mathematics": {
                "topics": ["Algebra", "Geometry", "Calculus", "Statistics", "Trigonometry"],
                "keywords": ["equation", "variable", "function", "theorem", "proof", "formula"],
                "content_template": "This lesson covers {topic}. Key concepts include {concepts}. "
                                  "Students will learn about {skill} and how to apply it to solve problems."
            },
            "science": {
                "topics": ["Physics", "Chemistry", "Biology", "Earth Science", "Astronomy"],
                "keywords": ["experiment", "hypothesis", "theory", "observation", "analysis"],
                "content_template": "This lesson explores {topic}. We will study {concepts} and "
                                  "understand the principles of {skill}. Practical applications include..."
            },
            "english": {
                "topics": ["Grammar", "Literature", "Writing", "Reading Comprehension", "Poetry"],
                "keywords": ["analysis", "interpretation", "structure", "theme", "character"],
                "content_template": "This lesson focuses on {topic}. Students will analyze {concepts} "
                                  "and develop skills in {skill}. Key literary elements include..."
            },
            "history": {
                "topics": ["Ancient Civilizations", "World Wars", "American History", "Renaissance", "Industrial Revolution"],
                "keywords": ["timeline", "cause", "effect", "significance", "primary source", "context"],
                "content_template": "This lesson examines {topic}. We will explore {concepts} and "
                                  "understand the historical significance of {skill}. Key events and figures include..."
            },
            "health_science": {
                "topics": ["Nutrition", "Anatomy", "Disease Prevention", "Mental Health", "Exercise Physiology"],
                "keywords": ["wellness", "diagnosis", "treatment", "prevention", "health", "body system"],
                "content_template": "This lesson covers {topic}. Students will learn about {concepts} and "
                                  "understand how to apply {skill} for better health outcomes. Important considerations include..."
            }
        }
        
        if subject not in templates:
            raise ValueError(f"Subject {subject} not supported")
        
        template = templates[subject]
        lessons = []
        
        for i in range(count):
            topic = random.choice(template["topics"])
            keywords = random.sample(template["keywords"], k=3)
            
            lesson = {
                "lesson_id": f"{subject}_{i+1:04d}",
                "subject": subject.capitalize(),
                "grade_level": str(random.randint(6, 12)),
                "title": f"{topic} - Lesson {i+1}",
                "summary": template["content_template"].format(
                    topic=topic,
                    concepts=", ".join(keywords[:2]),
                    skill=keywords[2]
                ),
                "topics": [topic],
                "keywords": keywords,
                "difficulty": random.choice(["beginner", "intermediate", "advanced"]),
                "created_at": datetime.now().isoformat()
            }
            
            lessons.append(lesson)
        
        # Save to file
        output_file = self.raw_path / "lessons" / subject / "lessons.jsonl"
        with open(output_file, 'w', encoding='utf-8') as f:
            for lesson in lessons:
                f.write(json.dumps(lesson) + '\n')
        
        print(f"✓ Generated {count} sample lessons for {subject}")
        return lessons
    
    def generate_sample_questions(self, subject: str, count: int = 200):
        """Generate sample questions for prototyping"""
        
        question_templates = {
            "mcq": {
                "mathematics": [
                    "What is the value of x in the equation {eq}?",
                    "Which of the following is a prime number?",
                    "What is the area of a circle with radius {r}?"
                ],
                "science": [
                    "What is the chemical formula for {compound}?",
                    "Which law states that {law}?",
                    "What is the function of {organ} in the human body?"
                ],
                "english": [
                    "What is the main theme of {text}?",
                    "Which literary device is used in {example}?",
                    "What does the word '{word}' mean in this context?"
                ],
                "history": [
                    "In what year did {event} occur?",
                    "Who was the leader during {period}?",
                    "What was the main cause of {war}?"
                ],
                "health_science": [
                    "Which vitamin is essential for {function}?",
                    "What is the primary function of the {organ}?",
                    "Which of the following is a symptom of {condition}?"
                ]
            },
            "short_answer": {
                "mathematics": [
                    "Explain the Pythagorean theorem.",
                    "Describe the process of solving a quadratic equation.",
                    "What is the difference between mean and median?"
                ],
                "science": [
                    "Explain the process of photosynthesis.",
                    "Describe Newton's first law of motion.",
                    "What is the water cycle?"
                ],
                "english": [
                    "Explain the use of metaphor in poetry.",
                    "Describe the structure of a persuasive essay.",
                    "What is the difference between simile and metaphor?"
                ],
                "history": [
                    "Explain the significance of the Renaissance.",
                    "Describe the causes of World War I.",
                    "What were the effects of the Industrial Revolution?"
                ],
                "health_science": [
                    "Explain the importance of cardiovascular exercise.",
                    "Describe the digestive process.",
                    "What are the key components of a balanced diet?"
                ]
            }
        }
        
        questions = []
        
        for i in range(count):
            q_type = random.choice(["mcq", "short_answer"])
            
            if q_type == "mcq":
                question = self._generate_mcq_sample(subject, i, question_templates)
            else:
                question = self._generate_short_answer_sample(subject, i, question_templates)
            
            questions.append(question)
        
        # Save to file
        output_file = self.raw_path / "questions" / subject / "questions.jsonl"
        with open(output_file, 'w', encoding='utf-8') as f:
            for question in questions:
                f.write(json.dumps(question) + '\n')
        
        print(f"✓ Generated {count} sample questions for {subject}")
        return questions

    def _generate_mcq_sample(self, subject: str, index: int, templates: Dict) -> Dict:
        """Generate a sample MCQ question"""

        template = random.choice(templates["mcq"][subject])

        question = {
            "question_id": f"{subject}_mcq_{index+1:04d}",
            "subject": subject.capitalize(),
            "question_type": "mcq",
            "question_text": template,
            "options": [
                {"letter": "A", "text": f"Option A for question {index+1}"},
                {"letter": "B", "text": f"Option B for question {index+1}"},
                {"letter": "C", "text": f"Option C for question {index+1}"},
                {"letter": "D", "text": f"Option D for question {index+1}"}
            ],
            "correct_answer": random.choice(["A", "B", "C", "D"]),
            "explanation": f"Explanation for question {index+1}",
            "difficulty": random.choice(["easy", "medium", "hard"]),
            "bloom_level": random.choice(["remember", "understand", "apply"]),
            "keywords": [f"keyword{i}" for i in range(3)]
        }

        return question

    def _generate_short_answer_sample(self, subject: str, index: int, templates: Dict) -> Dict:
        """Generate a sample short answer question"""

        template = random.choice(templates["short_answer"][subject])

        question = {
            "question_id": f"{subject}_short_{index+1:04d}",
            "subject": subject.capitalize(),
            "question_type": "short_answer",
            "question_text": template,
            "expected_answer": f"Expected answer for: {template}",
            "difficulty": random.choice(["easy", "medium", "hard"]),
            "bloom_level": random.choice(["understand", "apply", "analyze"]),
            "keywords": [f"keyword{i}" for i in range(3)]
        }

        return question

    def split_dataset(self, input_file: Path, train_ratio: float = 0.7,
                     val_ratio: float = 0.15, test_ratio: float = 0.15):
        """Split dataset into train, validation, and test sets"""

        # Load data
        data = []
        with open(input_file, 'r', encoding='utf-8') as f:
            for line in f:
                data.append(json.loads(line))

        # Shuffle
        random.shuffle(data)

        # Calculate split indices
        total = len(data)
        train_end = int(total * train_ratio)
        val_end = train_end + int(total * val_ratio)

        # Split
        train_data = data[:train_end]
        val_data = data[train_end:val_end]
        test_data = data[val_end:]

        # Save splits
        splits = {
            "train": train_data,
            "validation": val_data,
            "test": test_data
        }

        for split_name, split_data in splits.items():
            output_file = self.processed_path / split_name / input_file.name
            with open(output_file, 'w', encoding='utf-8') as f:
                for item in split_data:
                    f.write(json.dumps(item) + '\n')

        print(f"✓ Split {input_file.name}: Train={len(train_data)}, Val={len(val_data)}, Test={len(test_data)}")

    def prepare_finetuning_data(self, questions_file: Path, output_file: Path):
        """Prepare data in format suitable for LLaMA fine-tuning"""

        finetuning_data = []

        with open(questions_file, 'r', encoding='utf-8') as f:
            for line in f:
                question = json.loads(line)

                # Create instruction-response pair
                if question['question_type'] == 'mcq':
                    instruction = self._create_mcq_instruction(question)
                    response = self._create_mcq_response(question)
                else:
                    instruction = self._create_short_answer_instruction(question)
                    response = self._create_short_answer_response(question)

                finetuning_data.append({
                    "instruction": instruction,
                    "input": "",
                    "output": response
                })

        # Save
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(finetuning_data, f, indent=2)

        print(f"✓ Prepared {len(finetuning_data)} fine-tuning examples")

    def _create_mcq_instruction(self, question: Dict) -> str:
        """Create instruction for MCQ generation"""
        return f"""Generate a multiple-choice question for {question['subject']}.
Difficulty: {question['difficulty']}
Keywords: {', '.join(question['keywords'])}

Create a question with 4 options and indicate the correct answer."""

    def _create_mcq_response(self, question: Dict) -> str:
        """Create response for MCQ"""
        options_text = "\n".join([f"{opt['letter']}) {opt['text']}" for opt in question['options']])
        return f"""Question: {question['question_text']}
{options_text}
Correct Answer: {question['correct_answer']}
Explanation: {question['explanation']}"""

    def _create_short_answer_instruction(self, question: Dict) -> str:
        """Create instruction for short answer generation"""
        return f"""Generate a short answer question for {question['subject']}.
Difficulty: {question['difficulty']}
Keywords: {', '.join(question['keywords'])}

Create a question that requires a 2-3 sentence response."""

    def _create_short_answer_response(self, question: Dict) -> str:
        """Create response for short answer"""
        return f"""Question: {question['question_text']}
Expected Answer: {question['expected_answer']}"""


def main():
    """Main execution function"""

    print("=" * 60)
    print("Dataset Preparation for AI Homework Management System")
    print("=" * 60)

    preparator = DatasetPreparator()

    # Generate sample data for all subjects
    subjects = ["mathematics", "science", "english", "history", "health_science"]

    for subject in subjects:
        print(f"\n--- Processing {subject.upper()} ---")

        # Generate sample lessons
        preparator.generate_sample_lessons(subject, count=100)

        # Generate sample questions
        preparator.generate_sample_questions(subject, count=200)

        # Split datasets
        lessons_file = preparator.raw_path / "lessons" / subject / "lessons.jsonl"
        questions_file = preparator.raw_path / "questions" / subject / "questions.jsonl"

        preparator.split_dataset(lessons_file)
        preparator.split_dataset(questions_file)

        # Prepare fine-tuning data
        train_questions = preparator.processed_path / "train" / "questions.jsonl"
        finetuning_output = preparator.processed_path / "train" / f"{subject}_finetuning.json"

        if train_questions.exists():
            preparator.prepare_finetuning_data(train_questions, finetuning_output)

    print("\n" + "=" * 60)
    print("✓ Dataset preparation complete!")
    print("=" * 60)
    print(f"\nData saved to: {preparator.base_path}")
    print("\nNext steps:")
    print("1. Review the generated sample data")
    print("2. Replace with real data from textbooks/sources")
    print("3. Run validation: python scripts/validate_dataset.py")
    print("4. Start model training: python scripts/train_model.py")


if __name__ == "__main__":
    main()


