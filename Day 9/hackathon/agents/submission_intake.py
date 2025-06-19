# agents/submission_intake.py
import pandas as pd

def validate_csv(df: pd.DataFrame) -> bool:
    return {"Name", "Title", "Messages", "Endorsements", "Events"}.issubset(df.columns)
