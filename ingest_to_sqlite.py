from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd


TABLE_FILES = {
    "users": "users.csv",
    "products": "products.csv",
    "orders": "orders.csv",
    "order_items": "order_items.csv",
    "payments": "payments.csv",
}


def ingest_csvs_to_sqlite(data_dir: Path, db_path: Path) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(db_path) as conn:
        for table_name, file_name in TABLE_FILES.items():
            csv_path = data_dir / file_name
            if not csv_path.exists():
                raise FileNotFoundError(f"Missing required CSV: {csv_path}")

            df = pd.read_csv(csv_path)
            df.to_sql(table_name, conn, if_exists="replace", index=False)
            print(f"Loaded {len(df)} rows into '{table_name}'")

        conn.commit()
    print(f"Ingestion complete. SQLite DB located at {db_path.resolve()}")


def main() -> None:
    project_root = Path(__file__).parent
    data_dir = project_root / "data"
    db_path = project_root / "ecommerce.db"

    ingest_csvs_to_sqlite(data_dir, db_path)


if __name__ == "__main__":
    main()


