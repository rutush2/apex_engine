from sqlalchemy import inspect
from database import SessionLocal, engine, Base
from models import Finding, Strategy

class ApexAuditor:
    def __init__(self):
        self.session = SessionLocal()
        self._ensure_tables_exist()

    def _ensure_tables_exist(self):
        inspector = inspect(engine)
        if "findings" not in inspector.get_table_names():
            Base.metadata.create_all(bind=engine)

    def calculate_priority(self, impact, age):
        impact_map = {"Critical": 10, "High": 7, "Medium": 4, "Low": 2}
        base_score = impact_map.get(impact, 1)
        return impact_map.get(impact, 1)

    def generate_audit_report(self):
        self._ensure_tables_exist()
        return self.session.query(Finding).all()

    def ingest_finding(self, ref_code, subject, impact, status, age):
        auto_priority = self.calculate_priority(impact, age)
        new_finding = Finding(
            ref_code=ref_code,
            subject=subject,
            impact_level=impact,
            status=status,
            age_in_days=age,
            priority=auto_priority
        )
        try:
            self.session.add(new_finding)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e

    def add_strategy(self, finding_id, title, steps):
        new_strategy = Strategy(
            title=title,
            methodology=steps,
            finding_id=finding_id
        )
        self.session.add(new_strategy)
        self.session.commit()

    def update_finding_status(self, finding_id, new_status):
        finding = self.session.query(Finding).filter(Finding.id == finding_id).first()
        if finding:
            finding.status = new_status
            self.session.commit()
