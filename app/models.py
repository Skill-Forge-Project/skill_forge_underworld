import random
from datetime import datetime
from app.database_conn import db
from sqlalchemy.orm import relationship
from sqlalchemy import Enum


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
    date_created = db.Column(db.DateTime, default=datetime.now())
    
    # Relationship with Challenge Class
    challenges = relationship('Challenge', back_populates='boss_name')
    
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
            
            
# Underworld Challenge Class
class Challenge(db.Model):
    __tablename__ = 'underworld_challenges'
    challenge_id = db.Column(db.String(20), primary_key=True, nullable=False)
    boss_id = db.Column(db.String(11), db.ForeignKey('underworld_bosses.boss_id'), nullable=False)
    # Relationship with Boss Class
    boss_name = relationship("Boss", back_populates="challenges")
    user_id = db.Column(db.String(11), nullable=False)
    user_name = db.Column(db.String(50), nullable=False)
    challenge_date = db.Column(db.DateTime, default=datetime.now())
    state = db.Column(Enum('In Progress', 'Finished', 'Failed', name='challenge_state'), default='In Progress', nullable=False)
    
    # Class Constructor
    def __init__(self, boss_id, user_id, user_name):
        self.challenge_id = self.generate_challenge_id()
        self.boss_id = boss_id
        self.user_id = user_id
        self.user_name = user_name
        self.state = 'In Progress'
    
    # Generate Challenge ID
    def generate_challenge_id(self):
        # Generate a unique challenge ID in the format CHALLENGE-XXXXXX
        while True:
            challenge_id = f'CHALLENGE-{random.randint(1000000000, 9999999999)}'
            if not Challenge.query.filter_by(challenge_id=challenge_id).first():
                return challenge_id
    
    # Save the challenge to the database
    def create_challenge(self):
        db.session.add(self)
        db.session.commit()

    # Finish Challenge
    @classmethod
    def finish_challenge(cls, challenge_id):
        challenge = cls.query.filter_by(challenge_id=challenge_id).first()
        if challenge:
            challenge.state = 'Finished'
            db.session.commit()
        else:
            print(f"Challenge with ID {challenge_id} not found.")
    
    # Fail Challenge(if the Skill Forge timer is over)
    @classmethod
    def fail_challenge(cls, challenge_id):
        challenge = cls.query.filter_by(challenge_id=challenge_id).first()
        if challenge:
            challenge.state = 'Failed'
            db.session.commit()
        else:
            print(f"Challenge with ID {challenge_id} not found.")