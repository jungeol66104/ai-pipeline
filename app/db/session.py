import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from app.db.models import Timeline, Event, EventTimeline, InvalidEvents, TrainingSet, SerpUrl

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()
engine = db.bind
connection = engine.connect()


# query
def query_instance_by_id(table, target_id):
    return db.query(table).filter(table.id == target_id).first()


query_invalid_event_by_id = lambda target_id: query_instance_by_id(InvalidEvents, target_id)


def query_highest_column_value(column):
    return db.query(func.max(column)).scalar()


query_highest_timeline_id = query_highest_column_value(Timeline.id)
query_highest_event_id = query_highest_column_value(Event.id)
query_highest_event_timeline_id = query_highest_column_value(EventTimeline.id)
query_highest_invalid_events_id = query_highest_column_value(InvalidEvents.id)
query_highest_training_set_id = query_highest_column_value(TrainingSet.id)


def query_timeline_by_name(target_name):
    return db.query(Timeline).filter(Timeline.name == target_name).first()


def query_serp_urls_by_url(target_url):
    return db.query(SerpUrl).filter(SerpUrl.url == target_url).all()


def query_invalid_events_by_subject(target_subject):
    return db.query(InvalidEvents).filter(InvalidEvents.subject == target_subject).all()


# insert
def insert_data(table, data):
    try:
        db.bulk_insert_mappings(table, data)
        db.commit()
    except Exception as e:
        db.rollback()
        print(e)


insert_timeline = lambda timelines: insert_data(Timeline, timelines)
insert_event = lambda events: insert_data(Event, events)
insert_event_timeline = lambda event_timelines: insert_data(EventTimeline, event_timelines)
insert_invalid_events = lambda invalid_events: insert_data(InvalidEvents, invalid_events)
insert_training_set = lambda training_sets: insert_data(TrainingSet, training_sets)
insert_serp_url = lambda serp_urls: insert_data(SerpUrl, serp_urls)
