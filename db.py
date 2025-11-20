import os
from contextlib import contextmanager
from datetime import datetime, timedelta
from typing import List

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    Integer,
    String,
    Text,
    create_engine,
)
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import declarative_base, sessionmaker

# Default connection string for local development.
# Replace password/host/port as needed or provide DATABASE_URL env var.
DEFAULT_DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:5432/civicguardian"

DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_DATABASE_URL)

engine = create_engine(DATABASE_URL, pool_pre_ping=True, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
Base = declarative_base()


class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(50), nullable=False)
    description = Column(Text, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    distance_label = Column(String(50), nullable=True)
    occurred_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)


class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(50), nullable=False)
    description = Column(Text, nullable=False)
    location = Column(String(255), nullable=False)
    status = Column(String(50), nullable=False, default="pending")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    unread = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)


@contextmanager
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def seed_initial_data() -> None:
    """Populate the database with demo content when tables are empty."""
    with get_session() as session:
        try:
            incident_count = session.query(Incident).count()
            report_count = session.query(Report).count()
            notification_count = session.query(Notification).count()

            now = datetime.utcnow()

            if incident_count == 0:
                session.add_all(
                    [
                        Incident(
                            type="theft",
                            description="Car break-in",
                            latitude=40.7128,
                            longitude=-74.0060,
                            distance_label="0.5 miles",
                            occurred_at=now - timedelta(minutes=15),
                        ),
                        Incident(
                            type="vandalism",
                            description="Graffiti on building",
                            latitude=40.7180,
                            longitude=-74.0100,
                            distance_label="0.8 miles",
                            occurred_at=now - timedelta(hours=2),
                        ),
                        Incident(
                            type="accident",
                            description="Two-car collision",
                            latitude=40.7080,
                            longitude=-74.0050,
                            distance_label="1.2 miles",
                            occurred_at=now - timedelta(hours=5),
                        ),
                        Incident(
                            type="suspicious",
                            description="Suspicious person spotted",
                            latitude=40.7150,
                            longitude=-74.0150,
                            distance_label="0.3 miles",
                            occurred_at=now - timedelta(days=1),
                        ),
                        Incident(
                            type="hazard",
                            description="Fallen tree blocking road",
                            latitude=40.7100,
                            longitude=-74.0080,
                            distance_label="0.7 miles",
                            occurred_at=now - timedelta(days=2),
                        ),
                    ]
                )

            if report_count == 0:
                session.add_all(
                    [
                        Report(
                            type="theft",
                            description="Bike stolen from parking area.",
                            location="Main St & 3rd Ave",
                            status="resolved",
                            created_at=now - timedelta(days=1),
                        ),
                        Report(
                            type="accident",
                            description="Minor collision at the intersection.",
                            location="5th Avenue",
                            status="pending",
                            created_at=now - timedelta(hours=6),
                        ),
                    ]
                )

            if notification_count == 0:
                session.add_all(
                    [
                        Notification(
                            title="New Incident Near You",
                            description="A traffic accident was reported 0.3 miles from your location.",
                            unread=True,
                            created_at=now - timedelta(minutes=2),
                        ),
                        Notification(
                            title="Report Resolved",
                            description="Your report #1256 has been resolved by local authorities.",
                            unread=False,
                            created_at=now - timedelta(hours=1),
                        ),
                        Notification(
                            title="App Update Available",
                            description="Update to version 2.1.0 is now available with new features.",
                            unread=False,
                            created_at=now - timedelta(hours=3),
                        ),
                    ]
                )

            session.commit()
        except SQLAlchemyError:
            session.rollback()
            raise


def init_db() -> None:
    """Create tables and seed sample content if needed."""
    Base.metadata.create_all(bind=engine)
    seed_initial_data()

