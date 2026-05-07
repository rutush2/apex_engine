class DataRefiner:
    @staticmethod
    def refine_text(text: str):
        """Cleans up input text before it hits the database."""
        return text.strip() if text and text.strip() else ""

    @staticmethod
    def format_ref_code(number: int):
        """Standardizes the APEX-FND format."""
        return f"APEX-FND-{number:04d}"

    @staticmethod
    def validate_impact(impact: str):
        """Ensures the impact level matches your system expectations."""
        valid_levels = ["Low", "Medium", "High", "Critical"]
        return impact if impact in valid_levels else "Medium"

class RiskAnalyzer:
    @staticmethod
    def calculate_priority(impact_level: str, days_open: int) -> float:
        scales = {"Critical": 10.0, "High": 7.5, "Medium": 5.0, "Low": 2.5}
        base = scales.get(impact_level, 5.0)
        age_factor = min(days_open, 30) / 3.0
        return round(min((base * 0.7) + (age_factor * 0.3), 10.0), 2)
