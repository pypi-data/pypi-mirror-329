from .basic import app
from ..connection import get_postgresql_connection
import json
import typer

@app.command("importdata")
def load_json(input_file: str):
    """Load JSON data into the PostgreSQL database (import table data)."""
    try:
        # Read JSON file
        with open(input_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        conn = get_postgresql_connection()
        cursor = conn.cursor()

        for table_name, table_data in data.items():
            columns = table_data["columns"]
            rows = table_data["data"]

            if not rows:
                typer.echo(f"⚠️ Skipping {table_name}: No data to insert.")
                continue  # Skip empty tables

            # Convert JSON null values to Python None
            cleaned_rows = [[None if value is None else value for value in row] for row in rows]

            # Handle alembic_version separately to avoid duplicates
            if table_name == "alembic_version":
                cursor.execute("SELECT version_num FROM alembic_version;")
                existing_versions = {row[0] for row in cursor.fetchall()}

                new_versions = [row for row in cleaned_rows if row[0] not in existing_versions]
                if not new_versions:
                    typer.echo("⚠️ Skipping alembic_version: No new versions to insert.")
                    continue  # Skip if no new versions

                query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES (%s)"
                cursor.executemany(query, new_versions)

            else:
                # Prepare SQL statement
                placeholders = ", ".join(["%s"] * len(columns))
                query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"

                try:
                    cursor.executemany(query, cleaned_rows)  # Efficient batch insert
                    typer.echo(f"✅ Inserted {len(rows)} records into {table_name}.")
                except Exception as e:
                    typer.echo(f"❌ Error inserting data into {table_name}: {e}")

        conn.commit()
        cursor.close()
        conn.close()
        
        typer.echo(f"🎉 Successfully imported data from {input_file} into the database.")

    except Exception as e:
        typer.echo(f"❌ Error loading data: {e}")