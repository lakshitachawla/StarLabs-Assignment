from database import Base, engine, SessionLocal, FitnessClass
from datetime import datetime
import pytz

def seed_data():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    ist = pytz.timezone('Asia/Kolkata')
    
    # Check if data already exists
    if db.query(FitnessClass).count() == 0:
        sample_classes = [
            FitnessClass(name="Yoga Flow", instructor="John Doe", available_slots=20, 
                         date_time=datetime(2025, 6, 15, 10, 0, tzinfo=ist)),
            FitnessClass(name="Zumba Dance", instructor="Sarah Lee", available_slots=15, 
                         date_time=datetime(2025, 6, 16, 18, 0, tzinfo=ist)),
            FitnessClass(name="HIIT Session", instructor="Jane Smith", available_slots=10, 
                         date_time=datetime(2025, 6, 18, 8, 0, tzinfo=ist))
        ]
        db.add_all(sample_classes)
        db.commit()
        print("Database seeded successfully!")
    db.close()

if __name__ == "__main__":
    seed_data()