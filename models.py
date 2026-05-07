from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db_connection import Base


class Finding(Base):
    __tablename__ = "findings"

    id = Column(Integer, primary_key=True, index=True)
    ref_code = Column(String, unique=True, index=True)
    subject = Column(String)
    context = Column(String)
    impact_level = Column(String)
    status = Column(String, default="Open")
    priority = Column(Integer, default=0)
    age_in_days = Column(Integer, default=0)

    strategies = relationship("Strategy", back_populates="finding")


class Strategy(Base):
    __tablename__ = "strategies"

    id = Column(Integer, primary_key=True, index=True)
    finding_id = Column(Integer, ForeignKey("findings.id"))
    title = Column(String)
    methodology = Column(String)

    finding = relationship("Finding", back_populates="strategies")