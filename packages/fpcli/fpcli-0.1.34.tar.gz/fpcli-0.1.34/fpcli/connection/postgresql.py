from ..function.get_settings import get_settings


def get_postgresql_connection():
    """Get the PostgreSQL connection using psycopg2."""
    import psycopg2  # For PostgreSQL
    settings= get_settings()
    conn = psycopg2.connect(
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        dbname=settings.DB_NAME,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD

    )
    return conn