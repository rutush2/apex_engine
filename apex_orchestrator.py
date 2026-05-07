from db_connection import SessionLocal, engine
from db_logic import Finding, Strategy, Base, Category
from apex_processor import DataRefiner


class ApexManager:
    def __init__(self):
        Base.metadata.create_all(bind=engine)

    def register_finding(self, subject: str, context: str, impact: str, category_name: str = None):
        db = SessionLocal()
        try:
            existing = db.query(Finding).filter(Finding.subject == subject).first()
            if existing:
                return existing

            count = db.query(Finding).count()
            cat = self.get_or_create_category(category_name) if category_name else None

            new_entry = Finding(
                ref_code=DataRefiner.format_ref_code(count + 1),
                subject=subject,
                context=context,
                impact_level=impact,
                category_id=cat.id if cat else None
            )
            db.add(new_entry)
            db.commit()
            db.refresh(new_entry)
            return new_entry
        finally:
            db.close()

    @staticmethod
    def link_finding_to_strategy(finding_id: int, strategy_id: int):
        db = SessionLocal()
        try:
            finding = db.query(Finding).filter(Finding.id == finding_id).first()
            strategy = db.query(Strategy).filter(Strategy.id == strategy_id).first()
            if finding and strategy and strategy not in finding.strategies:
                finding.strategies.append(strategy)
                db.commit()
                return True
            return False
        finally:
            db.close()


    @staticmethod
    def register_strategy(title: str, methodology: str):
        db = SessionLocal()
        try:
            new_strategy = Strategy(
                title=DataRefiner.refine_text(title) or title,
                methodology=methodology
            )
            db.add(new_strategy)
            db.commit()
            db.refresh(new_strategy)
            return new_strategy
        except Exception as e:
            print(f"Strategy Registration Error: {e}")
            db.rollback()
            return None
        finally:
            db.close()


    @staticmethod
    def update_status(ref_code: str, new_status: str):
        db = SessionLocal()
        try:
            finding = db.query(Finding).filter(Finding.ref_code == ref_code).first()
            if finding:
                finding.status = new_status
                db.commit()
                return True
            return False
        finally:
            db.close()

    @staticmethod
    def get_or_create_category(name: str):
        db = SessionLocal()
        try:
            name_clean = DataRefiner.refine_text(name) or name
            category = db.query(Category).filter(Category.name == name_clean).first()
            if not category:
                category = Category(name=name_clean)
                db.add(category)
                db.commit()
                db.refresh(category)
            return category
        finally:
            db.close()


