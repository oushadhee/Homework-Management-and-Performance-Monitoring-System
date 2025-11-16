"""
Sri Lanka Syllabus Dataset Preparation Script
Generates comprehensive datasets for Grades 6-11
Subjects: Science, History, English, Health Science
Based on Sri Lankan National Curriculum (English Medium)
"""

import json
import os
from pathlib import Path
from typing import List, Dict
import random
from datetime import datetime


class SriLankaSyllabusDataset:
    """Prepare datasets based on Sri Lankan syllabus for grades 6-11"""

    def __init__(self, base_path: str = "./data"):
        self.base_path = Path(base_path)
        self.raw_path = self.base_path / "raw" / "srilanka_syllabus"
        self.processed_path = self.base_path / "processed" / "srilanka_syllabus"

        # Grades 6-11
        self.grades = [6, 7, 8, 9, 10, 11]

        # Subjects
        self.subjects = ["science", "history", "english", "health_science"]

        self._create_directories()

    def _create_directories(self):
        """Create directory structure for Sri Lankan syllabus data"""
        directories = []

        for subject in self.subjects:
            for grade in self.grades:
                directories.append(self.raw_path / "lessons" / subject / f"grade_{grade}")
                directories.append(self.raw_path / "questions" / subject / f"grade_{grade}")

        directories.extend([
            self.processed_path / "train",
            self.processed_path / "validation",
            self.processed_path / "test",
        ])

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

        print(f"✓ Created Sri Lankan syllabus directory structure at {self.base_path}")

    def get_science_curriculum(self, grade: int) -> Dict:
        """Get Science curriculum topics for each grade (Sri Lankan syllabus)"""

        curriculum = {
            6: {
                "units": [
                    "Measurements and Units",
                    "Force and Motion",
                    "Energy",
                    "Matter",
                    "Living Things and Their Environment",
                    "Plant Kingdom",
                    "Animal Kingdom",
                    "Human Body Systems"
                ],
                "topics": {
                    "Measurements and Units": ["Length", "Mass", "Time", "Temperature", "SI Units"],
                    "Force and Motion": ["Types of Forces", "Friction", "Simple Machines", "Motion"],
                    "Energy": ["Forms of Energy", "Energy Transformation", "Heat", "Light", "Sound"],
                    "Matter": ["States of Matter", "Properties of Matter", "Changes in Matter"],
                    "Living Things and Their Environment": ["Ecosystems", "Food Chains", "Habitats"],
                    "Plant Kingdom": ["Parts of Plants", "Photosynthesis", "Plant Classification"],
                    "Animal Kingdom": ["Animal Classification", "Vertebrates", "Invertebrates"],
                    "Human Body Systems": ["Digestive System", "Respiratory System", "Circulatory System"]
                }
            },
            7: {
                "units": [
                    "Scientific Investigation",
                    "Electricity and Magnetism",
                    "Heat and Temperature",
                    "Atomic Structure",
                    "Chemical Reactions",
                    "Cell Biology",
                    "Reproduction in Plants",
                    "Health and Hygiene"
                ],
                "topics": {
                    "Scientific Investigation": ["Scientific Method", "Variables", "Data Collection"],
                    "Electricity and Magnetism": ["Electric Circuits", "Conductors and Insulators", "Magnets"],
                    "Heat and Temperature": ["Heat Transfer", "Thermal Expansion", "Temperature Scales"],
                    "Atomic Structure": ["Atoms", "Elements", "Compounds", "Mixtures"],
                    "Chemical Reactions": ["Physical Changes", "Chemical Changes", "Acids and Bases"],
                    "Cell Biology": ["Cell Structure", "Cell Functions", "Microscopy"],
                    "Reproduction in Plants": ["Sexual Reproduction", "Asexual Reproduction", "Seed Dispersal"],
                    "Health and Hygiene": ["Personal Hygiene", "Food Hygiene", "Disease Prevention"]
                }
            },
            8: {
                "units": [
                    "Mechanics",
                    "Light and Optics",
                    "Chemical Bonding",
                    "Periodic Table",
                    "Genetics",
                    "Evolution",
                    "Microorganisms",
                    "Environmental Science"
                ],
                "topics": {
                    "Mechanics": ["Speed and Velocity", "Acceleration", "Newton's Laws"],
                    "Light and Optics": ["Reflection", "Refraction", "Lenses", "Mirrors"],
                    "Chemical Bonding": ["Ionic Bonds", "Covalent Bonds", "Molecular Structure"],
                    "Periodic Table": ["Groups", "Periods", "Element Properties", "Trends"],
                    "Genetics": ["DNA", "Genes", "Heredity", "Mendel's Laws"],
                    "Evolution": ["Natural Selection", "Adaptation", "Fossils"],
                    "Microorganisms": ["Bacteria", "Viruses", "Fungi", "Protozoa"],
                    "Environmental Science": ["Pollution", "Conservation", "Climate Change"]
                }
            },
            9: {
                "units": [
                    "Work, Energy and Power",
                    "Waves and Sound",
                    "Chemical Equations",
                    "Organic Chemistry Basics",
                    "Human Reproduction",
                    "Nervous System",
                    "Ecology",
                    "Biotechnology"
                ],
                "topics": {
                    "Work, Energy and Power": ["Work", "Power", "Mechanical Energy", "Energy Conservation"],
                    "Waves and Sound": ["Wave Properties", "Sound Waves", "Frequency", "Amplitude"],
                    "Chemical Equations": ["Balancing Equations", "Stoichiometry", "Mole Concept"],
                    "Organic Chemistry Basics": ["Hydrocarbons", "Functional Groups", "Isomers"],
                    "Human Reproduction": ["Reproductive System", "Fertilization", "Development"],
                    "Nervous System": ["Neurons", "Brain", "Spinal Cord", "Reflexes"],
                    "Ecology": ["Ecosystems", "Biodiversity", "Food Webs", "Nutrient Cycles"],
                    "Biotechnology": ["Genetic Engineering", "Cloning", "Applications"]
                }
            },
            10: {
                "units": [
                    "Electricity and Electronics",
                    "Nuclear Physics",
                    "Electrochemistry",
                    "Environmental Chemistry",
                    "Human Physiology",
                    "Plant Physiology",
                    "Biodiversity",
                    "Sustainable Development"
                ],
                "topics": {
                    "Electricity and Electronics": ["Ohm's Law", "Series and Parallel Circuits", "Semiconductors"],
                    "Nuclear Physics": ["Radioactivity", "Nuclear Reactions", "Half-life"],
                    "Electrochemistry": ["Electrolysis", "Batteries", "Corrosion"],
                    "Environmental Chemistry": ["Air Pollution", "Water Pollution", "Soil Chemistry"],
                    "Human Physiology": ["Endocrine System", "Immune System", "Homeostasis"],
                    "Plant Physiology": ["Transpiration", "Tropisms", "Plant Hormones"],
                    "Biodiversity": ["Species Diversity", "Ecosystem Diversity", "Conservation"],
                    "Sustainable Development": ["Renewable Energy", "Waste Management", "Green Technology"]
                }
            },
            11: {
                "units": [
                    "Advanced Mechanics",
                    "Thermodynamics",
                    "Organic Chemistry Advanced",
                    "Analytical Chemistry",
                    "Molecular Biology",
                    "Biochemistry",
                    "Genetics and Evolution",
                    "Applied Biology"
                ],
                "topics": {
                    "Advanced Mechanics": ["Momentum", "Circular Motion", "Gravitation"],
                    "Thermodynamics": ["Laws of Thermodynamics", "Heat Engines", "Entropy"],
                    "Organic Chemistry Advanced": ["Alcohols", "Carboxylic Acids", "Polymers"],
                    "Analytical Chemistry": ["Qualitative Analysis", "Quantitative Analysis", "Spectroscopy"],
                    "Molecular Biology": ["DNA Replication", "Protein Synthesis", "Gene Expression"],
                    "Biochemistry": ["Enzymes", "Metabolism", "Cellular Respiration"],
                    "Genetics and Evolution": ["Population Genetics", "Speciation", "Evolutionary Theory"],
                    "Applied Biology": ["Agriculture", "Medicine", "Industrial Applications"]
                }
            }
        }

        return curriculum.get(grade, curriculum[6])

    def get_history_curriculum(self, grade: int) -> Dict:
        """Get History curriculum topics for each grade (Sri Lankan syllabus)"""

        curriculum = {
            6: {
                "units": [
                    "Ancient Sri Lanka",
                    "Early Civilizations",
                    "Buddhism in Sri Lanka",
                    "Ancient Kingdoms",
                    "Trade and Commerce",
                    "Art and Culture"
                ],
                "topics": {
                    "Ancient Sri Lanka": ["Prehistoric Period", "Stone Age", "Iron Age", "Early Settlements"],
                    "Early Civilizations": ["Indus Valley", "Mesopotamia", "Egypt", "China"],
                    "Buddhism in Sri Lanka": ["Introduction of Buddhism", "Mahinda Thero", "Buddhist Culture"],
                    "Ancient Kingdoms": ["Anuradhapura Kingdom", "Kings and Queens", "Irrigation Systems"],
                    "Trade and Commerce": ["Ancient Trade Routes", "Spice Trade", "Maritime Trade"],
                    "Art and Culture": ["Ancient Architecture", "Sculpture", "Painting", "Literature"]
                }
            },
            7: {
                "units": [
                    "Medieval Sri Lanka",
                    "Polonnaruwa Period",
                    "South Indian Influence",
                    "Medieval World",
                    "Religious Developments",
                    "Social Structure"
                ],
                "topics": {
                    "Medieval Sri Lanka": ["Transition Period", "Political Changes", "Economic Development"],
                    "Polonnaruwa Period": ["Parakramabahu the Great", "Irrigation Works", "Cultural Achievements"],
                    "South Indian Influence": ["Chola Invasions", "Cultural Exchange", "Tamil Settlements"],
                    "Medieval World": ["Feudalism", "Crusades", "Islamic Civilization", "Byzantine Empire"],
                    "Religious Developments": ["Spread of Buddhism", "Hindu Temples", "Religious Tolerance"],
                    "Social Structure": ["Caste System", "Village Organization", "Family Life"]
                }
            },
            8: {
                "units": [
                    "Colonial Period Begins",
                    "Portuguese in Sri Lanka",
                    "Dutch Period",
                    "Renaissance and Reformation",
                    "Age of Exploration",
                    "Cultural Changes"
                ],
                "topics": {
                    "Colonial Period Begins": ["European Arrival", "Motives for Colonization", "Impact"],
                    "Portuguese in Sri Lanka": ["Portuguese Rule", "Conversion to Christianity", "Resistance"],
                    "Dutch Period": ["Dutch East India Company", "Administrative System", "Economic Policies"],
                    "Renaissance and Reformation": ["Renaissance Art", "Scientific Revolution", "Protestant Reformation"],
                    "Age of Exploration": ["Voyages of Discovery", "Colonization", "Global Trade"],
                    "Cultural Changes": ["Language", "Religion", "Architecture", "Customs"]
                }
            },
            9: {
                "units": [
                    "British Colonial Period",
                    "Kandyan Kingdom",
                    "British Administration",
                    "Industrial Revolution",
                    "Social Reforms",
                    "Independence Movement Begins"
                ],
                "topics": {
                    "British Colonial Period": ["British Conquest", "Kandyan Convention", "Colonial Rule"],
                    "Kandyan Kingdom": ["Last Sinhalese Kingdom", "Cultural Preservation", "Resistance"],
                    "British Administration": ["Colebrooke-Cameron Reforms", "Plantation Economy", "Infrastructure"],
                    "Industrial Revolution": ["Technological Changes", "Social Impact", "Economic Transformation"],
                    "Social Reforms": ["Education System", "Legal Reforms", "Social Changes"],
                    "Independence Movement Begins": ["Early Nationalism", "Political Organizations", "Leaders"]
                }
            },
            10: {
                "units": [
                    "Struggle for Independence",
                    "World War I and II",
                    "National Movement",
                    "Post-War World",
                    "Decolonization",
                    "Path to Independence"
                ],
                "topics": {
                    "Struggle for Independence": ["Political Awakening", "Mass Movements", "Constitutional Reforms"],
                    "World War I and II": ["Causes", "Impact on Sri Lanka", "Global Consequences"],
                    "National Movement": ["Ceylon National Congress", "Donoughmore Commission", "Soulbury Commission"],
                    "Post-War World": ["United Nations", "Cold War", "Decolonization Movement"],
                    "Decolonization": ["Asian Independence", "African Independence", "New Nations"],
                    "Path to Independence": ["Constitutional Development", "Universal Suffrage", "Independence 1948"]
                }
            },
            11: {
                "units": [
                    "Independent Sri Lanka",
                    "Post-Independence Politics",
                    "Economic Development",
                    "Modern World History",
                    "Contemporary Issues",
                    "Sri Lanka Today"
                ],
                "topics": {
                    "Independent Sri Lanka": ["First Government", "Democratic System", "Nation Building"],
                    "Post-Independence Politics": ["Political Parties", "Elections", "Constitutional Changes"],
                    "Economic Development": ["Nationalization", "Open Economy", "Economic Policies"],
                    "Modern World History": ["Cold War", "Globalization", "International Relations"],
                    "Contemporary Issues": ["Ethnic Conflict", "Peace Process", "Reconciliation"],
                    "Sri Lanka Today": ["Current Politics", "Economy", "Society", "Future Challenges"]
                }
            }
        }

        return curriculum.get(grade, curriculum[6])



    def get_english_curriculum(self, grade: int) -> Dict:
        """Get English curriculum topics for each grade (Sri Lankan syllabus)"""

        curriculum = {
            6: {
                "units": [
                    "Reading Comprehension",
                    "Grammar Basics",
                    "Vocabulary Building",
                    "Writing Skills",
                    "Poetry",
                    "Short Stories"
                ],
                "topics": {
                    "Reading Comprehension": ["Main Idea", "Supporting Details", "Inference", "Context Clues"],
                    "Grammar Basics": ["Parts of Speech", "Sentence Structure", "Tenses", "Subject-Verb Agreement"],
                    "Vocabulary Building": ["Synonyms", "Antonyms", "Word Families", "Prefixes and Suffixes"],
                    "Writing Skills": ["Paragraph Writing", "Descriptive Writing", "Letter Writing"],
                    "Poetry": ["Rhyme", "Rhythm", "Simple Poems", "Recitation"],
                    "Short Stories": ["Story Elements", "Characters", "Plot", "Setting"]
                }
            },
            7: {
                "units": [
                    "Advanced Reading",
                    "Grammar and Usage",
                    "Creative Writing",
                    "Literature",
                    "Speaking and Listening",
                    "Language Skills"
                ],
                "topics": {
                    "Advanced Reading": ["Critical Reading", "Analysis", "Summarizing", "Note-taking"],
                    "Grammar and Usage": ["Clauses", "Phrases", "Active and Passive Voice", "Direct and Indirect Speech"],
                    "Creative Writing": ["Narrative Writing", "Dialogue", "Character Development"],
                    "Literature": ["Fables", "Folktales", "Moral Stories", "Cultural Stories"],
                    "Speaking and Listening": ["Presentations", "Discussions", "Listening Comprehension"],
                    "Language Skills": ["Idioms", "Proverbs", "Figurative Language"]
                }
            },
            8: {
                "units": [
                    "Literary Analysis",
                    "Advanced Grammar",
                    "Essay Writing",
                    "Drama",
                    "Media Literacy",
                    "Research Skills"
                ],
                "topics": {
                    "Literary Analysis": ["Theme", "Symbolism", "Point of View", "Literary Devices"],
                    "Advanced Grammar": ["Complex Sentences", "Conditionals", "Modals", "Reported Speech"],
                    "Essay Writing": ["Expository Essays", "Persuasive Essays", "Essay Structure"],
                    "Drama": ["Play Reading", "Stage Directions", "Character Analysis", "Dialogue"],
                    "Media Literacy": ["Advertisements", "News Articles", "Digital Media"],
                    "Research Skills": ["Library Skills", "Citations", "Bibliography", "Research Methods"]
                }
            },
            9: {
                "units": [
                    "World Literature",
                    "Advanced Composition",
                    "Critical Thinking",
                    "Shakespeare Introduction",
                    "Debate and Argumentation",
                    "Language and Society"
                ],
                "topics": {
                    "World Literature": ["International Authors", "Cultural Perspectives", "Comparative Literature"],
                    "Advanced Composition": ["Argumentative Writing", "Research Papers", "Editing and Revision"],
                    "Critical Thinking": ["Logical Reasoning", "Bias Detection", "Fact vs Opinion"],
                    "Shakespeare Introduction": ["Sonnets", "Simple Plays", "Elizabethan English"],
                    "Debate and Argumentation": ["Debate Structure", "Evidence", "Counterarguments"],
                    "Language and Society": ["Language Variation", "Formal vs Informal", "Register"]
                }
            },
            10: {
                "units": [
                    "British Literature",
                    "Academic Writing",
                    "Poetry Analysis",
                    "Novel Study",
                    "Public Speaking",
                    "Language Theory"
                ],
                "topics": {
                    "British Literature": ["Victorian Era", "Romantic Period", "Modern British Writers"],
                    "Academic Writing": ["Research Papers", "Citations (MLA/APA)", "Academic Style"],
                    "Poetry Analysis": ["Meter", "Form", "Imagery", "Tone", "Mood"],
                    "Novel Study": ["Plot Analysis", "Character Development", "Themes", "Context"],
                    "Public Speaking": ["Speech Writing", "Delivery Techniques", "Audience Analysis"],
                    "Language Theory": ["Linguistics Basics", "Phonetics", "Semantics", "Pragmatics"]
                }
            },
            11: {
                "units": [
                    "American Literature",
                    "Advanced Literary Criticism",
                    "Professional Writing",
                    "Contemporary Literature",
                    "Communication Skills",
                    "Exam Preparation"
                ],
                "topics": {
                    "American Literature": ["American Authors", "American Dream Theme", "Modern American Writing"],
                    "Advanced Literary Criticism": ["Critical Theories", "Feminist Criticism", "Post-colonial Theory"],
                    "Professional Writing": ["Business Letters", "Reports", "Proposals", "CVs"],
                    "Contemporary Literature": ["21st Century Authors", "Global Literature", "Digital Literature"],
                    "Communication Skills": ["Interpersonal Communication", "Professional Communication", "Negotiation"],
                    "Exam Preparation": ["Essay Techniques", "Comprehension Strategies", "Time Management"]
                }
            }
        }

        return curriculum.get(grade, curriculum[6])

    def get_health_science_curriculum(self, grade: int) -> Dict:
        """Get Health Science curriculum topics for each grade (Sri Lankan syllabus)"""

        curriculum = {
            6: {
                "units": [
                    "Personal Hygiene",
                    "Nutrition Basics",
                    "Physical Fitness",
                    "Disease Prevention",
                    "Safety and First Aid",
                    "Mental Health Basics"
                ],
                "topics": {
                    "Personal Hygiene": ["Hand Washing", "Dental Care", "Bathing", "Grooming"],
                    "Nutrition Basics": ["Food Groups", "Balanced Diet", "Healthy Eating", "Water Importance"],
                    "Physical Fitness": ["Exercise Benefits", "Sports", "Physical Activities", "Rest"],
                    "Disease Prevention": ["Common Diseases", "Vaccinations", "Hygiene Practices"],
                    "Safety and First Aid": ["Home Safety", "Road Safety", "Basic First Aid", "Emergency Numbers"],
                    "Mental Health Basics": ["Emotions", "Stress", "Friendship", "Self-esteem"]
                }
            },
            7: {
                "units": [
                    "Human Body Systems",
                    "Nutrition and Health",
                    "Adolescent Health",
                    "Communicable Diseases",
                    "Environmental Health",
                    "Health Habits"
                ],
                "topics": {
                    "Human Body Systems": ["Skeletal System", "Muscular System", "Digestive System", "Respiratory System"],
                    "Nutrition and Health": ["Vitamins", "Minerals", "Proteins", "Carbohydrates", "Fats"],
                    "Adolescent Health": ["Puberty", "Growth", "Body Changes", "Hygiene"],
                    "Communicable Diseases": ["Transmission", "Prevention", "Common Infections", "Immunity"],
                    "Environmental Health": ["Clean Water", "Sanitation", "Waste Disposal", "Air Quality"],
                    "Health Habits": ["Sleep", "Exercise Routine", "Healthy Lifestyle", "Avoiding Harmful Substances"]
                }
            },
            8: {
                "units": [
                    "Advanced Anatomy",
                    "Nutrition Science",
                    "Reproductive Health",
                    "Non-Communicable Diseases",
                    "Mental Wellness",
                    "Health Education"
                ],
                "topics": {
                    "Advanced Anatomy": ["Circulatory System", "Nervous System", "Endocrine System"],
                    "Nutrition Science": ["Metabolism", "Nutritional Deficiencies", "Diet Planning"],
                    "Reproductive Health": ["Reproductive System", "Menstruation", "Hygiene", "Respect"],
                    "Non-Communicable Diseases": ["Diabetes", "Heart Disease", "Cancer", "Prevention"],
                    "Mental Wellness": ["Stress Management", "Anxiety", "Depression Awareness", "Coping Skills"],
                    "Health Education": ["Health Information", "Making Decisions", "Peer Pressure"]
                }
            },
            9: {
                "units": [
                    "Health and Wellness",
                    "Sports Medicine",
                    "Substance Abuse",
                    "Sexual Health",
                    "Chronic Diseases",
                    "Community Health"
                ],
                "topics": {
                    "Health and Wellness": ["Holistic Health", "Wellness Dimensions", "Lifestyle Choices"],
                    "Sports Medicine": ["Sports Injuries", "Prevention", "Treatment", "Rehabilitation"],
                    "Substance Abuse": ["Drugs", "Alcohol", "Tobacco", "Addiction", "Prevention"],
                    "Sexual Health": ["STIs", "HIV/AIDS", "Prevention", "Safe Practices", "Respect"],
                    "Chronic Diseases": ["Asthma", "Arthritis", "Management", "Living with Chronic Illness"],
                    "Community Health": ["Public Health", "Health Services", "Community Programs"]
                }
            },
            10: {
                "units": [
                    "Advanced Nutrition",
                    "Mental Health and Counseling",
                    "Occupational Health",
                    "Health Policy",
                    "Emergency Care",
                    "Health Technology"
                ],
                "topics": {
                    "Advanced Nutrition": ["Dietary Guidelines", "Nutrition for Athletes", "Special Diets", "Food Science"],
                    "Mental Health and Counseling": ["Mental Disorders", "Therapy", "Support Systems", "Resilience"],
                    "Occupational Health": ["Workplace Safety", "Ergonomics", "Occupational Diseases"],
                    "Health Policy": ["Healthcare Systems", "Health Insurance", "Public Health Policy"],
                    "Emergency Care": ["CPR", "Advanced First Aid", "Emergency Response", "Disaster Preparedness"],
                    "Health Technology": ["Medical Devices", "Health Apps", "Telemedicine", "Health Records"]
                }
            },
            11: {
                "units": [
                    "Public Health",
                    "Epidemiology",
                    "Health Research",
                    "Global Health",
                    "Health Careers",
                    "Integrated Health"
                ],
                "topics": {
                    "Public Health": ["Disease Surveillance", "Health Promotion", "Prevention Programs"],
                    "Epidemiology": ["Disease Patterns", "Outbreak Investigation", "Statistical Analysis"],
                    "Health Research": ["Research Methods", "Clinical Trials", "Evidence-Based Practice"],
                    "Global Health": ["International Health Issues", "WHO", "Global Diseases", "Health Equity"],
                    "Health Careers": ["Medical Professions", "Allied Health", "Career Paths", "Education Requirements"],
                    "Integrated Health": ["Traditional Medicine", "Complementary Medicine", "Holistic Approaches"]
                }
            }
        }

        return curriculum.get(grade, curriculum[6])


    def generate_lesson(self, subject: str, grade: int, unit: str, topics: List[str]) -> Dict:
        """Generate a lesson based on curriculum"""

        lesson_templates = {
            "science": """
# {unit} - Grade {grade}

## Learning Objectives
By the end of this lesson, students will be able to:
- Understand the fundamental concepts of {topics}
- Apply scientific principles to real-world situations
- Analyze and interpret scientific data related to {unit}

## Introduction
This lesson explores {unit}, focusing on {topics}. Students will learn through hands-on activities,
demonstrations, and practical applications relevant to Sri Lankan context.

## Main Content
{detailed_content}

## Key Concepts
{key_concepts}

## Activities
1. Laboratory experiment demonstrating {topics[0]}
2. Group discussion on applications in Sri Lanka
3. Problem-solving exercises
4. Real-world case studies

## Assessment
Students will be assessed through practical work, written tests, and project presentations.

## Resources
- Textbook: Science for Grade {grade} (Sri Lankan Curriculum)
- Laboratory equipment
- Digital resources and simulations
""",
            "history": """
# {unit} - Grade {grade}

## Learning Objectives
By the end of this lesson, students will be able to:
- Understand the historical significance of {topics}
- Analyze causes and effects of historical events
- Evaluate the impact on Sri Lankan and world history

## Historical Context
This lesson examines {unit}, with particular focus on {topics}. We will explore how these events
shaped Sri Lankan society and its place in world history.

## Timeline
{timeline_content}

## Main Content
{detailed_content}

## Key Historical Figures
{key_figures}

## Primary Sources
Students will analyze historical documents, photographs, and artifacts from this period.

## Discussion Questions
1. What were the main causes of {topics[0]}?
2. How did these events affect Sri Lankan society?
3. What lessons can we learn from this period?

## Assessment
Essays, timeline projects, source analysis, and presentations.

## Resources
- History textbook for Grade {grade}
- National Archives of Sri Lanka
- Museum artifacts and photographs
""",
            "english": """
# {unit} - Grade {grade}

## Learning Objectives
By the end of this lesson, students will be able to:
- Master key concepts in {topics}
- Apply language skills in written and oral communication
- Analyze literary texts critically

## Introduction
This lesson focuses on {unit}, covering {topics}. Students will develop their English language
proficiency through reading, writing, speaking, and listening activities.

## Main Content
{detailed_content}

## Language Focus
{language_points}

## Reading Passage
{reading_text}

## Writing Activities
1. {topics[0]} exercises
2. Creative writing tasks
3. Formal and informal writing practice

## Speaking and Listening
- Class discussions
- Presentations
- Pair and group work
- Listening comprehension exercises

## Assessment
Written assignments, oral presentations, comprehension tests, and portfolio work.

## Resources
- English textbook for Grade {grade}
- Literary texts
- Audio-visual materials
- Online resources
""",
            "health_science": """
# {unit} - Grade {grade}

## Learning Objectives
By the end of this lesson, students will be able to:
- Understand health concepts related to {topics}
- Apply health knowledge to daily life
- Make informed decisions about personal and community health

## Introduction
This lesson covers {unit}, focusing on {topics}. Students will learn practical health information
relevant to Sri Lankan context and their daily lives.

## Main Content
{detailed_content}

## Health Guidelines
{health_guidelines}

## Practical Applications
1. Personal health practices
2. Community health initiatives
3. Prevention strategies
4. Health promotion activities

## Case Studies
Real-life scenarios from Sri Lankan communities demonstrating health concepts.

## Activities
- Health assessments
- Group projects
- Community surveys
- Health promotion campaigns

## Assessment
Projects, presentations, practical demonstrations, and written tests.

## Resources
- Health Science textbook for Grade {grade}
- WHO and Ministry of Health guidelines
- Local health statistics
- Guest speakers from health sector
"""
        }

        template = lesson_templates.get(subject, lesson_templates["science"])

        # Generate detailed content based on topics
        detailed_content = f"This section covers {', '.join(topics)}. "
        detailed_content += f"Students will explore each topic through theoretical understanding and practical application."

        lesson_text = template.format(
            unit=unit,
            grade=grade,
            topics=', '.join(topics),
            detailed_content=detailed_content,
            key_concepts=', '.join(topics[:3]),
            timeline_content="Key dates and events will be discussed",
            key_figures="Important historical figures relevant to this period",
            language_points="Grammar, vocabulary, and usage points",
            reading_text="Selected passages for comprehension and analysis",
            health_guidelines="Evidence-based health recommendations"
        )

        return {
            "subject": subject,
            "grade": grade,
            "unit": unit,
            "title": f"{unit} - Grade {grade}",
            "topics": topics,
            "content": lesson_text,
            "difficulty": self._estimate_difficulty(grade),
            "duration_minutes": 60,
            "learning_outcomes": [
                f"Understand {topics[0]}",
                f"Apply knowledge of {topics[1] if len(topics) > 1 else topics[0]}",
                f"Analyze concepts related to {unit}"
            ]
        }

    def _estimate_difficulty(self, grade: int) -> str:
        """Estimate difficulty based on grade level"""
        if grade <= 7:
            return "beginner"
        elif grade <= 9:
            return "intermediate"
        else:
            return "advanced"


    def generate_questions(self, lesson: Dict, num_questions: int = 10) -> List[Dict]:
        """Generate questions for a lesson"""

        questions = []
        subject = lesson["subject"]
        grade = lesson["grade"]
        topics = lesson["topics"]
        unit = lesson["unit"]

        # Distribution: 40% MCQ, 35% Short Answer, 25% Descriptive
        num_mcq = int(num_questions * 0.4)
        num_short = int(num_questions * 0.35)
        num_descriptive = num_questions - num_mcq - num_short

        # Generate MCQ questions
        for i in range(num_mcq):
            topic = topics[i % len(topics)]
            questions.append(self._generate_mcq(subject, grade, unit, topic, i + 1))

        # Generate Short Answer questions
        for i in range(num_short):
            topic = topics[i % len(topics)]
            questions.append(self._generate_short_answer(subject, grade, unit, topic, i + 1))

        # Generate Descriptive questions
        for i in range(num_descriptive):
            topic = topics[i % len(topics)]
            questions.append(self._generate_descriptive(subject, grade, unit, topic, i + 1))

        return questions

    def _generate_mcq(self, subject: str, grade: int, unit: str, topic: str, q_num: int) -> Dict:
        """Generate a multiple choice question"""

        question_templates = {
            "science": [
                f"What is the primary function of {topic}?",
                f"Which of the following best describes {topic}?",
                f"In the context of {unit}, {topic} is responsible for:",
                f"What happens when {topic} occurs?",
            ],
            "history": [
                f"What was the main cause of {topic}?",
                f"Which period is associated with {topic}?",
                f"Who was primarily responsible for {topic}?",
                f"What was the significance of {topic} in Sri Lankan history?",
            ],
            "english": [
                f"Which of the following is an example of {topic}?",
                f"In {unit}, {topic} refers to:",
                f"What is the correct usage of {topic}?",
                f"Identify the {topic} in the following sentence:",
            ],
            "health_science": [
                f"What is the recommended practice for {topic}?",
                f"Which of the following promotes {topic}?",
                f"What is a common symptom of {topic}?",
                f"How can {topic} be prevented?",
            ]
        }

        templates = question_templates.get(subject, question_templates["science"])
        question_text = random.choice(templates)

        return {
            "question_type": "MCQ",
            "question_text": question_text,
            "options": [
                f"Option A related to {topic}",
                f"Option B related to {topic}",
                f"Option C related to {topic}",
                f"Option D related to {topic}"
            ],
            "correct_answer": "A",
            "explanation": f"This is correct because {topic} functions in this way according to {unit} principles.",
            "difficulty": self._estimate_difficulty(grade),
            "bloom_level": "remember",
            "marks": 1,
            "subject": subject,
            "grade": grade,
            "unit": unit,
            "topic": topic
        }

    def _generate_short_answer(self, subject: str, grade: int, unit: str, topic: str, q_num: int) -> Dict:
        """Generate a short answer question"""

        question_templates = {
            "science": [
                f"Explain the process of {topic}.",
                f"Describe the relationship between {topic} and {unit}.",
                f"What are the main characteristics of {topic}?",
                f"How does {topic} affect the system?",
            ],
            "history": [
                f"Briefly explain the significance of {topic}.",
                f"What were the main outcomes of {topic}?",
                f"Describe the role of {topic} in this period.",
                f"How did {topic} impact Sri Lankan society?",
            ],
            "english": [
                f"Define {topic} and give an example.",
                f"Explain how {topic} is used in writing.",
                f"What is the purpose of {topic}?",
                f"Describe the key features of {topic}.",
            ],
            "health_science": [
                f"Explain why {topic} is important for health.",
                f"Describe the main components of {topic}.",
                f"What are the benefits of {topic}?",
                f"How can you practice {topic} in daily life?",
            ]
        }

        templates = question_templates.get(subject, question_templates["science"])
        question_text = random.choice(templates)

        return {
            "question_type": "SHORT_ANSWER",
            "question_text": question_text,
            "expected_answer": f"A comprehensive explanation of {topic} including its key aspects, relevance to {unit}, and practical applications.",
            "key_points": [
                f"Definition of {topic}",
                f"Relationship to {unit}",
                f"Practical application or example"
            ],
            "difficulty": self._estimate_difficulty(grade),
            "bloom_level": "understand",
            "marks": 3,
            "subject": subject,
            "grade": grade,
            "unit": unit,
            "topic": topic
        }

    def _generate_descriptive(self, subject: str, grade: int, unit: str, topic: str, q_num: int) -> Dict:
        """Generate a descriptive question"""

        question_templates = {
            "science": [
                f"Discuss in detail the scientific principles underlying {topic} and their applications in {unit}.",
                f"Analyze the role of {topic} in the broader context of {unit}. Provide examples from Sri Lankan context.",
                f"Evaluate the importance of {topic} and explain how it relates to other concepts in {unit}.",
            ],
            "history": [
                f"Analyze the causes and consequences of {topic} in Sri Lankan history.",
                f"Discuss the significance of {topic} and its long-term impact on society.",
                f"Evaluate different perspectives on {topic} and explain its relevance to modern Sri Lanka.",
            ],
            "english": [
                f"Write a detailed essay on {topic}, including examples and analysis.",
                f"Discuss the importance of {topic} in effective communication. Provide relevant examples.",
                f"Analyze how {topic} contributes to language proficiency and literary understanding.",
            ],
            "health_science": [
                f"Discuss the importance of {topic} for individual and community health in Sri Lanka.",
                f"Analyze the factors affecting {topic} and propose strategies for improvement.",
                f"Evaluate current practices related to {topic} and suggest evidence-based recommendations.",
            ]
        }

        templates = question_templates.get(subject, question_templates["science"])
        question_text = random.choice(templates)

        return {
            "question_type": "DESCRIPTIVE",
            "question_text": question_text,
            "expected_answer": f"A comprehensive analysis of {topic} covering theoretical understanding, practical applications, examples from Sri Lankan context, and critical evaluation.",
            "key_points": [
                f"Theoretical foundation of {topic}",
                f"Practical applications and examples",
                f"Analysis and critical thinking",
                f"Relevance to Sri Lankan context",
                f"Conclusions and recommendations"
            ],
            "difficulty": self._estimate_difficulty(grade),
            "bloom_level": "analyze",
            "marks": 5,
            "subject": subject,
            "grade": grade,
            "unit": unit,
            "topic": topic
        }


    def generate_all_datasets(self):
        """Generate comprehensive datasets for all subjects and grades"""

        print("=" * 80)
        print("Sri Lankan Syllabus Dataset Generation")
        print("Grades 6-11 | Subjects: Science, History, English, Health Science")
        print("=" * 80)
        print()

        total_lessons = 0
        total_questions = 0

        for subject in self.subjects:
            print(f"\n📚 Generating {subject.upper()} datasets...")
            print("-" * 80)

            subject_lessons = 0
            subject_questions = 0

            for grade in self.grades:
                print(f"\n  Grade {grade}:")

                # Get curriculum for this grade
                if subject == "science":
                    curriculum = self.get_science_curriculum(grade)
                elif subject == "history":
                    curriculum = self.get_history_curriculum(grade)
                elif subject == "english":
                    curriculum = self.get_english_curriculum(grade)
                elif subject == "health_science":
                    curriculum = self.get_health_science_curriculum(grade)
                else:
                    continue

                grade_lessons = []
                grade_questions = []

                # Generate lessons for each unit
                for unit in curriculum["units"]:
                    topics = curriculum["topics"].get(unit, [])

                    # Generate lesson
                    lesson = self.generate_lesson(subject, grade, unit, topics)
                    grade_lessons.append(lesson)

                    # Generate questions for this lesson
                    questions = self.generate_questions(lesson, num_questions=10)
                    grade_questions.extend(questions)

                # Save lessons
                lessons_file = self.raw_path / "lessons" / subject / f"grade_{grade}" / "lessons.jsonl"
                with open(lessons_file, 'w', encoding='utf-8') as f:
                    for lesson in grade_lessons:
                        f.write(json.dumps(lesson, ensure_ascii=False) + '\n')

                # Save questions
                questions_file = self.raw_path / "questions" / subject / f"grade_{grade}" / "questions.jsonl"
                with open(questions_file, 'w', encoding='utf-8') as f:
                    for question in grade_questions:
                        f.write(json.dumps(question, ensure_ascii=False) + '\n')

                subject_lessons += len(grade_lessons)
                subject_questions += len(grade_questions)

                print(f"    ✓ Generated {len(grade_lessons)} lessons and {len(grade_questions)} questions")

            total_lessons += subject_lessons
            total_questions += subject_questions

            print(f"\n  {subject.upper()} Total: {subject_lessons} lessons, {subject_questions} questions")

        print("\n" + "=" * 80)
        print(f"✅ Dataset Generation Complete!")
        print(f"   Total Lessons: {total_lessons}")
        print(f"   Total Questions: {total_questions}")
        print(f"   Subjects: {len(self.subjects)}")
        print(f"   Grades: {len(self.grades)}")
        print("=" * 80)

        # Generate summary report
        self._generate_summary_report(total_lessons, total_questions)

    def _generate_summary_report(self, total_lessons: int, total_questions: int):
        """Generate a summary report of the dataset"""

        report = {
            "generation_date": datetime.now().isoformat(),
            "curriculum": "Sri Lankan National Curriculum (English Medium)",
            "grades": self.grades,
            "subjects": self.subjects,
            "statistics": {
                "total_lessons": total_lessons,
                "total_questions": total_questions,
                "lessons_per_subject": total_lessons // len(self.subjects),
                "questions_per_subject": total_questions // len(self.subjects),
                "lessons_per_grade": total_lessons // len(self.grades),
                "questions_per_grade": total_questions // len(self.grades)
            },
            "breakdown": {
                subject: {
                    f"grade_{grade}": {
                        "lessons": len(self.get_science_curriculum(grade)["units"]) if subject == "science"
                        else len(self.get_history_curriculum(grade)["units"]) if subject == "history"
                        else len(self.get_english_curriculum(grade)["units"]) if subject == "english"
                        else len(self.get_health_science_curriculum(grade)["units"]),
                        "questions": len(self.get_science_curriculum(grade)["units"]) * 10 if subject == "science"
                        else len(self.get_history_curriculum(grade)["units"]) * 10 if subject == "history"
                        else len(self.get_english_curriculum(grade)["units"]) * 10 if subject == "english"
                        else len(self.get_health_science_curriculum(grade)["units"]) * 10
                    }
                    for grade in self.grades
                }
                for subject in self.subjects
            },
            "data_location": {
                "raw_data": str(self.raw_path),
                "processed_data": str(self.processed_path)
            }
        }

        # Save report
        report_file = self.base_path / "srilanka_dataset_report.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        print(f"\n📊 Summary report saved to: {report_file}")


def main():
    """Main execution function"""

    print("\n" + "=" * 80)
    print("SRI LANKAN SYLLABUS DATASET PREPARATION")
    print("AI-Powered Homework Management System")
    print("=" * 80)

    # Initialize dataset generator
    generator = SriLankaSyllabusDataset()

    # Generate all datasets
    generator.generate_all_datasets()

    print("\n✨ Dataset preparation complete!")
    print("\nNext Steps:")
    print("1. Review the generated datasets in data/raw/srilanka_syllabus/")
    print("2. Customize lesson content with actual curriculum materials")
    print("3. Add real questions from past papers and textbooks")
    print("4. Run data validation and quality checks")
    print("5. Process datasets for model training")
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
