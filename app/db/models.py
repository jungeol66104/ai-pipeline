from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Test(Base):
    __tablename__ = 'test'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    date = Column(String(100))
    julian_date = Column(Float)


class Timeline(Base):
    __tablename__ = 'timeline'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200))
    # Add an index on the 'name' column
    Index('idx_timeline_name', name, unique=False)


class Event(Base):
    __tablename__ = 'event'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    date = Column(String(100))
    julian_date = Column(Float)


class EventTimelineAssociation(Base):
    __tablename__ = 'event_timeline_association'

    id = Column(Integer, primary_key=True, autoincrement=True)
    event_id = Column(Integer, ForeignKey('event.id'), nullable=False)
    timeline_id = Column(Integer, ForeignKey('timeline.id'), nullable=False)
    importance = Column(Integer)
    # Define relationships to access related objects
    event = relationship('Event', backref='event_timeline_associations')
    timeline = relationship('Timeline', backref='event_timeline_associations')
