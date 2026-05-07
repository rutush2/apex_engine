from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime, timezone
from sqlalchemy.ext.hybrid import hybrid_property


Base = declarative_base()

resolution_map = Table(
    'resolution_map', Base.metadata,
    Column('finding_id', Integer, ForeignKey('findings.id'), primary_key=True),
    Column('strategy_id', Integer, ForeignKey('strategies.id'), primary_key=True)
)

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)
    findings = relationship("Finding", back_populates="category")

class Finding(Base):
    __tablename__ = "findings"
    id = Column(Integer, primary_key=True, autoincrement=True)
    ref_code = Column(String, unique=True, index=True)
    subject = Column(String)
    context = Column(Text)
    impact_level = Column(String)
    status = Column(String, default="Identified")
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=True)
    category = relationship("Category", back_populates="findings", lazy="joined")
    detected_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    strategies = relationship("Strategy", secondary=resolution_map, back_populates="findings", lazy="joined")

    @hybrid_property
    def age_in_days(self):
        if self.detected_at:
            now = datetime.now(timezone.utc)
            detected = self.detected_at.replace(tzinfo=timezone.utc) if self.detected_at.tzinfo is None else self.detected_at
            return (now - detected).days
        return 0

    @property
    def priority_score(self):
        from apex_processor import RiskAnalyzer
        return RiskAnalyzer.calculate_priority(self.impact_level, self.age_in_days)


class Strategy(Base):
    __tablename__ = "strategies"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    methodology = Column(Text)
    findings = relationship("Finding", secondary=resolution_map, back_populates="strategies")