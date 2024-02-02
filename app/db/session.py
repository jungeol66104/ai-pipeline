import os
from dotenv import load_dotenv
from sqlalchemy import func
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.models import Timeline, Event, EventTimeline, InvalidEvents, TrainingSet, SerpUrl

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
Session = sessionmaker(engine)
session = Session()


# query
def query_instance_by_id(table, target_id):
    return session.query(table).filter(table.id == target_id).first()


query_invalid_event_by_id = lambda target_id: query_instance_by_id(InvalidEvents, target_id)
query_serp_url_by_id = lambda target_id: query_instance_by_id(SerpUrl, target_id)


def query_highest_column_value(column):
    return session.query(func.max(column)).scalar()


query_highest_timeline_id = lambda: query_highest_column_value(Timeline.id)
query_highest_event_id = lambda: query_highest_column_value(Event.id)
query_highest_event_timeline_id = lambda: query_highest_column_value(EventTimeline.id)
query_highest_invalid_event_id = lambda: query_highest_column_value(InvalidEvents.id)
query_highest_training_set_id = lambda: query_highest_column_value(TrainingSet.id)


def query_timeline_by_name(target_name):
    return session.query(Timeline).filter(Timeline.name == target_name).first()


def query_serp_urls_by_url(target_url):
    return session.query(SerpUrl).filter(SerpUrl.url == target_url).all()


def query_invalid_event_by_subject(target_subject):
    return session.query(InvalidEvents).filter(InvalidEvents.subject == target_subject).first()


def query_serp_urls_by_subject(target_subject):
    return session.query(SerpUrl).filter(SerpUrl.subject == target_subject).all()


# modify
def complete_invalid_event_by_id(target_id):
    try:
        invalid_event = query_invalid_event_by_id(target_id)
        invalid_event.is_completed = 1
        session.commit()
    except Exception as e:
        session.rollback()
        print(e)
    return


def complete_serp_urls_by_id(target_ids):
    try:
        for target_id in target_ids:
            serp_url = query_serp_url_by_id(target_id)
            serp_url.is_completed = 1
        session.commit()
    except Exception as e:
        session.rollback()
        print(e)

    return


# insert
def insert_data(table, data):
    try:
        session.bulk_insert_mappings(table, data)
        session.commit()
    except Exception as e:
        session.rollback()
        print(e)
    return


insert_timeline = lambda timelines: insert_data(Timeline, timelines)
insert_event = lambda events: insert_data(Event, events)
insert_event_timeline = lambda event_timelines: insert_data(EventTimeline, event_timelines)
insert_invalid_events = lambda invalid_events: insert_data(InvalidEvents, invalid_events)
insert_training_set = lambda training_sets: insert_data(TrainingSet, training_sets)
insert_serp_url = lambda serp_urls: insert_data(SerpUrl, serp_urls)
