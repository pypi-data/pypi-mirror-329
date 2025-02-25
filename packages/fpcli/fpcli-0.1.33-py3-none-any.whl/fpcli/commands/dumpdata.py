import json
import typer
from .basic import app
from ..connection import get_postgresql_connection
# Database connection configuration



def get_all_tables():
    """Fetch all table names from the PostgreSQL database."""
    conn = get_postgresql_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
    tables = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return tables

def get_table_data(table_name):
    """Fetch all data from a table along with column names."""
    conn = get_postgresql_connection()
    cursor = conn.cursor()
    
    # Fetch table data and column names in a single query
    cursor.execute(f"SELECT * FROM {table_name};")
    records = cursor.fetchall()
    
    # Fetch column names from cursor.description
    columns = [desc[0] for desc in cursor.description]

    cursor.close()
    conn.close()
    
    return {"columns": columns, "data": records}

def export_to_json(data, output):
    """Export data to JSON file."""
    with open(output, "w", encoding="utf-8") as f:
        json.dump(data, f)

def export_to_sql(data, output):
    """Export data to SQL file (only INSERT statements)."""
    with open(output, "w", encoding="utf-8") as f:
        for table_name, table_data in data.items():
            f.write(f"-- Data for table {table_name}\n")
            
            for row in table_data["data"]:
                values = ', '.join([repr(value) for value in row])
                f.write(f"INSERT INTO {table_name} ({', '.join(table_data['columns'])}) VALUES ({values});\n")
            
            f.write("\n")

@app.command("exportdata")
def datadump(
    output: str = "datadump.json",
    include: list[str] = typer.Option(None, help="List of tables to include"),
    exclude: list[str] = typer.Option(None, help="List of tables to exclude")
):
    """Dump only table data (not structure) to JSON or SQL format."""
    all_tables = get_all_tables()

    # Determine which tables to export
    if include:
        tables_to_export = [table for table in all_tables if table in include]
    elif exclude:
        tables_to_export = [table for table in all_tables if table not in exclude]
    else:
        tables_to_export = all_tables  # Default: Export all tables

    data = {table: get_table_data(table) for table in tables_to_export}

    # Determine export format
    if output.endswith(".json"):
        export_to_json(data, output)
    elif output.endswith(".sql"):
        export_to_sql(data, output)
    else:
        raise ValueError(f"Unsupported file format: {output.split('.')[-1]}")

    typer.echo(typer.style(f"Data successfully dumped to {output}",typer.colors.GREEN,bold=True))

