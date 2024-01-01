from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Event(Base):
    __tablename__ = 'event'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    date = Column(String(100))
    ephemeris_time = Column(Float)


class Timeline(Base):
    __tablename__ = 'timeline'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200))


class EventTimeline(Base):
    __tablename__ = 'event_timeline'

    id = Column(Integer, primary_key=True, autoincrement=True)
    event_id = Column(Integer, ForeignKey('event.id', ondelete='CASCADE'))
    timeline_id = Column(Integer, ForeignKey('timeline.id', ondelete='CASCADE'))
    importance = Column(Integer)
    event = relationship('Event')
    timeline = relationship('Timeline')


class LanguageCode(Base):
    __tablename__ = 'language_code'

    id = Column(Integer, primary_key=True, autoincrement=True)
    language_code = Column(String(10))


class EventTranslation(Base):
    __tablename__ = 'event_translation'

    id = Column(Integer, primary_key=True, autoincrement=True)
    event_id = Column(Integer, ForeignKey('event.id', ondelete='CASCADE'))
    language_code_id = Column(Integer, ForeignKey('language_code.id', ondelete='CASCADE'))
    name = Column(String(200), nullable=False)
    description = Column(Text)
    event = relationship('Event')
    language_code = relationship('LanguageCode')


class TimelineTranslation(Base):
    __tablename__ = 'timeline_translation'

    id = Column(Integer, primary_key=True, autoincrement=True)
    timeline_id = Column(Integer, ForeignKey('timeline.id', ondelete='CASCADE'))
    language_code_id = Column(Integer, ForeignKey('language_code.id', ondelete='CASCADE'))
    name = Column(String(200), nullable=False)
    timeline = relationship('Timeline')
    language_code = relationship('LanguageCode')


class InvalidEvents(Base):
    __tablename__ = 'invalid_events'

    id = Column(Integer, primary_key=True, autoincrement=True)
    subject = Column(String(200))
    name = Column(String(200))
    description = Column(Text)
    date = Column(String(100))
    importance = Column(Integer)


class PipelineModel(Base):
    __tablename__ = 'pipeline_model'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20))


class FineTuningTrainingSet(Base):
    __tablename__ = 'fine_tuning_training_set'

    id = Column(Integer, primary_key=True, autoincrement=True)
    pipeline_model_id = Column(Integer, ForeignKey('pipeline_model.id', ondelete='CASCADE'))
    input = Column(Text)
    output = Column(Text)
    pipeline_model = relationship('PipelineModel')