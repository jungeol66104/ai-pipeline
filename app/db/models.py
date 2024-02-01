from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Timeline(Base):
    __tablename__ = 'timeline'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200))
    description = Column(Text)
    image_url = Column(String(30))
    created_dt = Column(DateTime)
    updated_dt = Column(DateTime)


class Event(Base):
    __tablename__ = 'event'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    date = Column(String(100))
    ephemeris_time = Column(Float)
    is_enabled = Column(Integer)
    created_dt = Column(DateTime, nullable=False, default=func.current_timestamp())
    updated_dt = Column(DateTime, nullable=False, default=func.current_timestamp(), onupdate=func.current_timestamp())


class EventTimeline(Base):
    __tablename__ = 'event_timeline'

    id = Column(Integer, primary_key=True, autoincrement=True)
    event_id = Column(Integer, ForeignKey('event.id', ondelete='CASCADE'))
    timeline_id = Column(Integer, ForeignKey('timeline.id', ondelete='CASCADE'))
    importance = Column(Integer)
    event = relationship('Event')
    timeline = relationship('Timeline')


class Series(Base):
    __tablename__ = 'series'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)


class TimelineSeries(Base):
    __tablename__ = 'timeline_series'

    id = Column(Integer, primary_key=True, autoincrement=True)
    timeline_id = Column(Integer, ForeignKey('timeline.id', ondelete='CASCADE'))
    series_id = Column(Integer, ForeignKey('series.id', ondelete='CASCADE'))
    timeline = relationship('Timeline')
    series = relationship('Series')


class LanguageCode(Base):
    __tablename__ = 'language_code'

    id = Column(Integer, primary_key=True, autoincrement=True)
    language_code = Column(String(10))


class TimelineTranslation(Base):
    __tablename__ = 'timeline_translation'

    id = Column(Integer, primary_key=True, autoincrement=True)
    timeline_id = Column(Integer, ForeignKey('timeline.id', ondelete='CASCADE'))
    language_code_id = Column(Integer, ForeignKey('language_code.id', ondelete='CASCADE'))
    name = Column(String(200), nullable=False)
    description = Column(Text)
    timeline = relationship('Timeline')
    language_code = relationship('LanguageCode')


class EventTranslation(Base):
    __tablename__ = 'event_translation'

    id = Column(Integer, primary_key=True, autoincrement=True)
    event_id = Column(Integer, ForeignKey('event.id', ondelete='CASCADE'))
    language_code_id = Column(Integer, ForeignKey('language_code.id', ondelete='CASCADE'))
    name = Column(String(200), nullable=False)
    description = Column(Text)
    event = relationship('Event')
    language_code = relationship('LanguageCode')


class SeriesTranslation(Base):
    __tablename__ = 'series_translation'

    id = Column(Integer, primary_key=True, autoincrement=True)
    series_id = Column(Integer, ForeignKey('series.id', ondelete='CASCADE'))
    language_code_id = Column(Integer, ForeignKey('language_code.id', ondelete='CASCADE'))
    name = Column(String(200), nullable=False)
    description = Column(Text)
    event = relationship('Series')
    language_code = relationship('LanguageCode')


class InvalidEvents(Base):
    __tablename__ = 'invalid_events'

    id = Column(Integer, primary_key=True, autoincrement=True)
    subject = Column(String(200))
    name = Column(String(200))
    description = Column(Text)
    date = Column(String(100))
    importance = Column(Integer)
    is_completed = Column(Integer, nullable=False, default=0)
    created_dt = Column(DateTime, nullable=False, default=func.current_timestamp())
    updated_dt = Column(DateTime, nullable=False, default=func.current_timestamp(), onupdate=func.current_timestamp())


class PipelineModel(Base):
    __tablename__ = 'pipeline_model'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20))
    created_dt = Column(DateTime, nullable=False, default=func.current_timestamp())
    updated_dt = Column(DateTime, nullable=False, default=func.current_timestamp(), onupdate=func.current_timestamp())


class TrainingSet(Base):
    __tablename__ = 'training_set'

    id = Column(Integer, primary_key=True, autoincrement=True)
    pipeline_model_id = Column(Integer, ForeignKey('pipeline_model.id', ondelete='CASCADE'))
    input = Column(Text)
    output = Column(Text)
    pipeline_model = relationship('PipelineModel')
    created_dt = Column(DateTime, nullable=False, default=func.current_timestamp())
    updated_dt = Column(DateTime, nullable=False, default=func.current_timestamp(), onupdate=func.current_timestamp())


class UserTimeline(Base):
    __tablename__ = 'user_timeline'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text)
    user_email = Column(String(30))
    is_completed = Column(Integer)
    created_dt = Column(DateTime, nullable=False, default=func.current_timestamp())
    updated_dt = Column(DateTime, nullable=False, default=func.current_timestamp(), onupdate=func.current_timestamp())


class SerpUrl(Base):
    __tablename__ = 'serp_url'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False, default='')
    url = Column(Text(30))
    subject = Column(String(200), nullable=False, default='')
    is_completed = Column(Integer, nullable=False, default=0)
    created_dt = Column(DateTime, default=func.current_timestamp())
    updated_dt = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())
