from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import relationship

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)


session_speakers = db.Table(
    "session_speakers",
    db.Column("id", db.Integer, primary_key=True),
    db.Column(
        "session_id",
        db.Integer,
        db.ForeignKey("sessions.id", ondelete="CASCADE"),
        nullable=False,
    ),
    db.Column(
        "speaker_id",
        db.Integer,
        db.ForeignKey("speakers.id", ondelete="CASCADE"),
        nullable=False,
    ),
)



class Event(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)


    sessions = relationship(
        "Session",
        back_populates="event",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    def __repr__(self):
        return f"<Event {self.id}, {self.name}, {self.location}>"


class Session(db.Model):
    __tablename__ = "sessions"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    start_time = db.Column(db.DateTime)


    event_id = db.Column(
        db.Integer,
        db.ForeignKey("events.id", ondelete="CASCADE"),
        nullable=False,
    )
    event = relationship("Event", back_populates="sessions")


    speakers = relationship(
        "Speaker",
        secondary=session_speakers,
        back_populates="sessions",
    )

    def __repr__(self):
        return f"<Session {self.id}, {self.title}, {self.start_time}>"


class Speaker(db.Model):
    __tablename__ = "speakers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)


    bio = relationship(
        "Bio",
        back_populates="speaker",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

 
    sessions = relationship(
        "Session",
        secondary=session_speakers,
        back_populates="speakers",
    )

    def __repr__(self):
        return f"<Speaker {self.id}, {self.name}>"


class Bio(db.Model):
    __tablename__ = "bios"

    id = db.Column(db.Integer, primary_key=True)
    bio_text = db.Column(db.Text, nullable=False)


    speaker_id = db.Column(
        db.Integer,
        db.ForeignKey("speakers.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )
    speaker = relationship("Speaker", back_populates="bio")

    def __repr__(self):
        return f"<Bio {self.id}, speaker_id={self.speaker_id}>"