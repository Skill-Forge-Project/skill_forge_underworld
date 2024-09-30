import random
from app.database_conn import db
from sqlalchemy.orm import relationship


# Underworld Boss Class
class Boss(db.Model):
    __tablename__ = 'underworld_bosses'
    boss_id = db.Column(db.String(11), primary_key=True, nullable=False)
    boss_name = db.Column(db.String(50), nullable=False)
    boss_title = db.Column(db.String(50), nullable=False)
    boss_language = db.Column(db.String(50), nullable=False)
    boss_difficulty = db.Column(db.String(50), nullable=False)
    boss_specialty = db.Column(db.String(50), nullable=False)
    boss_description = db.Column(db.Text, nullable=False)
    
    # Class Constructor
    def __init__(self, boss_name, boss_title, boss_language, boss_difficulty, boss_specialty, boss_description):
        self.boss_id = self.generate_boss_id()  # Generate ID on initialization
        self.boss_name = boss_name
        self.boss_title = boss_title
        self.boss_language = boss_language
        self.boss_difficulty = boss_difficulty
        self.boss_specialty = boss_specialty
        self.boss_description = boss_description
    
    # Generate Boss ID
    def generate_boss_id(self):
        # Generate a unique boss ID in the format BOSS-XXXXXX
        while True:
            boss_id = f'BOSS-{random.randint(100000, 999999)}'
            if not Boss.query.filter_by(boss_id=boss_id).first():  # Ensure uniqueness
                return boss_id

    # Save the boss to the database
    def create_boss(self):
        db.session.add(self)
        db.session.commit()
    
    # Delete Boss
    @classmethod
    def delete_boss(cls, boss_id):
        boss = cls.query.filter_by(boss_id=boss_id).first()
        if boss:
            db.session.delete(boss)
            db.session.commit()
        else:
            print(f"Boss with ID {boss_id} not found.")
