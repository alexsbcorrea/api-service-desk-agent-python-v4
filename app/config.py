import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", 
        'postgresql+psycopg2://postgres.fzabhceycspgakfqrrzx:SD#2025@aws-0-us-west-2.pooler.supabase.com:5432/postgres'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "secret")
