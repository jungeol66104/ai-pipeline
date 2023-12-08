import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from app.db.models import Test, Timeline, Event, EventTimelineAssociation

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()
engine = db.bind
connection = engine.connect()


# insert
def insert_timeline(timelines):
    try:
        db.bulk_insert_mappings(Timeline, timelines)
        db.commit()
    except Exception as e:
        db.rollback()
        print(e)


def insert_event(events):
    try:
        db.bulk_insert_mappings(Event, events)
        db.commit()
    except Exception as e:
        db.rollback()
        print(e)


def insert_association(associations):
    try:
        db.bulk_insert_mappings(EventTimelineAssociation, associations)
        db.commit()
    except Exception as e:
        db.rollback()
        print(e)


# query
def query_timeline_by_name(target_name):
    return db.query(Timeline).filter(Timeline.name == target_name).first()


def query_timeline_highest_id():
    return db.query(func.max(Timeline.id)).scalar()


def query_event_highest_id():
    return db.query(func.max(Event.id)).scalar()
