"""
Initialize subjects in the database

This script creates the core subjects for the homework management system:
- Science
- History
- English
- Health Science
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.ext.asyncio import AsyncSession
from src.config.database import AsyncSessionLocal, init_db
from src.models.subject import Subject


# Subject data
SUBJECTS = [
    {
        "name": "Science",
        "code": "SCI",
        "description": "General Science covering Physics, Chemistry, Biology, and Earth Science",
        "grade_level": "6-12",
        "icon": "🔬",
        "color": "#4CAF50",
        "is_active": True
    },
    {
        "name": "History",
        "code": "HIST",
        "description": "World History, American History, and Social Studies",
        "grade_level": "6-12",
        "icon": "📚",
        "color": "#FF9800",
        "is_active": True
    },
    {
        "name": "English",
        "code": "ENG",
        "description": "English Language Arts including Reading, Writing, Grammar, and Literature",
        "grade_level": "6-12",
        "icon": "📖",
        "color": "#2196F3",
        "is_active": True
    },
    {
        "name": "Health Science",
        "code": "HLTH",
        "description": "Health Education, Nutrition, Anatomy, and Wellness",
        "grade_level": "6-12",
        "icon": "🏥",
        "color": "#E91E63",
        "is_active": True
    }
]


async def create_subjects():
    """Create subjects in the database"""
    
    print("🚀 Initializing database tables...")
    await init_db()
    print("✅ Database tables initialized\n")
    
    async with AsyncSessionLocal() as session:
        try:
            print("📚 Creating subjects...")
            
            for subject_data in SUBJECTS:
                # Check if subject already exists
                from sqlalchemy import select
                stmt = select(Subject).where(Subject.code == subject_data["code"])
                result = await session.execute(stmt)
                existing_subject = result.scalar_one_or_none()
                
                if existing_subject:
                    print(f"⚠️  Subject '{subject_data['name']}' ({subject_data['code']}) already exists - skipping")
                    continue
                
                # Create new subject
                subject = Subject(**subject_data)
                session.add(subject)
                print(f"✅ Created subject: {subject_data['name']} ({subject_data['code']})")
            
            # Commit all changes
            await session.commit()
            print("\n🎉 All subjects created successfully!")
            
            # Display all subjects
            print("\n" + "="*60)
            print("📋 Current Subjects in Database:")
            print("="*60)
            
            stmt = select(Subject).order_by(Subject.id)
            result = await session.execute(stmt)
            subjects = result.scalars().all()
            
            for subject in subjects:
                print(f"\n{subject.icon} {subject.name}")
                print(f"   Code: {subject.code}")
                print(f"   Description: {subject.description}")
                print(f"   Grade Level: {subject.grade_level}")
                print(f"   Color: {subject.color}")
                print(f"   Active: {'Yes' if subject.is_active else 'No'}")
            
            print("\n" + "="*60)
            print(f"Total subjects: {len(subjects)}")
            print("="*60)
            
        except Exception as e:
            await session.rollback()
            print(f"\n❌ Error creating subjects: {e}")
            raise
        finally:
            await session.close()


async def list_subjects():
    """List all subjects in the database"""
    
    async with AsyncSessionLocal() as session:
        try:
            from sqlalchemy import select
            
            stmt = select(Subject).order_by(Subject.id)
            result = await session.execute(stmt)
            subjects = result.scalars().all()
            
            if not subjects:
                print("⚠️  No subjects found in database")
                return
            
            print("\n" + "="*60)
            print("📋 Subjects in Database:")
            print("="*60)
            
            for subject in subjects:
                print(f"\n{subject.icon} {subject.name}")
                print(f"   ID: {subject.id}")
                print(f"   Code: {subject.code}")
                print(f"   Description: {subject.description}")
                print(f"   Grade Level: {subject.grade_level}")
                print(f"   Active: {'Yes' if subject.is_active else 'No'}")
            
            print("\n" + "="*60)
            print(f"Total subjects: {len(subjects)}")
            print("="*60)
            
        except Exception as e:
            print(f"\n❌ Error listing subjects: {e}")
            raise
        finally:
            await session.close()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Initialize subjects in the database")
    parser.add_argument(
        "--list",
        action="store_true",
        help="List existing subjects instead of creating new ones"
    )
    
    args = parser.parse_args()
    
    if args.list:
        print("📚 Listing subjects...\n")
        asyncio.run(list_subjects())
    else:
        print("🚀 Initializing subjects...\n")
        asyncio.run(create_subjects())

