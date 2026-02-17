from sqlalchemy import create_engine, inspect
import os

engine = create_engine(os.getenv("DATABASE_URL"))
inspector = inspect(engine)
cols = inspector.get_columns("documents")

print("Documents table columns:")
for c in cols:
    print(f"  {c['name']}: {c['type']}")
