import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from app.db.models import Timeline, Event, EventTimeline, TimelineTranslation, EventTranslation, InvalidEvents, FineTuningTrainingSet

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()
engine = db.bind
connection = engine.connect()


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
insert_timeline_translation = lambda timeline_translations: insert_data(TimelineTranslation, timeline_translations)
insert_event_translation = lambda event_translations: insert_data(EventTranslation, event_translations)
insert_invalid_events = lambda invalid_events: insert_data(InvalidEvents, invalid_events)
insert_fine_tuning_training_set = lambda fine_tuning_training_sets: insert_data(FineTuningTrainingSet, fine_tuning_training_sets)


# query
def query_highest_column_value(column):
    return db.query(func.max(column)).scalar()


query_highest_timeline_id = query_highest_column_value(Timeline.id)
query_highest_event_id = query_highest_column_value(Event.id)
query_highest_event_timeline_id = query_highest_column_value(EventTimeline.id)
query_highest_timeline_translation_id = query_highest_column_value(TimelineTranslation.id)
query_highest_event_translation_id = query_highest_column_value(EventTranslation.id)
query_highest_invalid_events_id = query_highest_column_value(InvalidEvents.id)
query_highest_fine_tuning_training_set_id = query_highest_column_value(FineTuningTrainingSet.id)


def query_timeline_by_name(target_name):
    return db.query(Timeline).filter(Timeline.name == target_name).first()
