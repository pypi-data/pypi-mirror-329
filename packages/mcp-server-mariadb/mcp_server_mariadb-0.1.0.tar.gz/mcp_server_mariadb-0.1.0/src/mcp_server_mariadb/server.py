import os
from contextlib import closing
from dataclasses import dataclass

import mariadb
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

load_dotenv()

mcp = FastMCP(
    "MariaDB Explorer", dependencies=["mysql-connector-python", "python-dotenv"]
)

READ_ONLY_KEYWORDS = ("SELECT", "SHOW", "DESCRIBE", "DESC", "EXPLAIN")
READ_ONLY_KEYWORD_NAMES = ", ".join(READ_ONLY_KEYWORDS)


@dataclass
class DBconfig:
    host: str = os.getenv("MARIADB_HOST", "localhost")
    port: int = int(os.getenv("MARIADB_PORT", "3306"))
    user: str = os.getenv("MARIADB_USER", "")
    password: str = os.getenv("MARIADB_PASSWORD", "")
    database: str = os.getenv("MARIADB_DATABASE", "")


def get_connection():
    """Create a connection to the database connection"""

    config = DBconfig()

    try:
        conn = mariadb.connect(
            user=config.user,
            password=config.password,
            host=config.host,
            port=config.port,
            database=config.database,
        )
        return conn
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")


def is_read_only_query(query: str) -> bool:
    """check if a query is read-only by examining its first word"""
    first_word = query.strip().split()[0].upper()

    return first_word in READ_ONLY_KEYWORDS


@mcp.resource("schema://tables")
def list_tables() -> str:
    """Get the schema for a specific table"""
    try:
        with closing(get_connection()) as conn:
            cursor = conn.cursor()
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            return "\n".join(table[0] for table in tables)
    except Exception as e:
        return f"Error retrieving tables: {str(e)}"


@mcp.tool()
def query_database(query: str) -> str:
    """
    Execute a read-only SQL query on the database

    Args:
        query: SQL query to execute (must be SELECT, SHOW, DESCRIBE, DESC, EXPLAIN)
    """

    if not is_read_only_query(query):
        return "Error: Only read-only queries (SELECT, SHOW, DESCRIBE, DESC, EXPLAIN) are allowed"

    try:
        with closing(get_connection()) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            results = cursor.fetchall()

            # Get column names
            columns = [desc[0] for desc in cursor.description]

            # Format results as a table
            output = []
            output.append(" | ".join(columns))
            output.append(
                "-" * (sum(len(col) for col in columns) + 3 * (len(columns) - 1))
            )

            for row in results:
                output.append(" | ".join(str(val) for val in row))

            return "\n".join(output)
    except Exception as e:
        return f"Error executing query {str(e)}"


if __name__ == "__main__":
    mcp.run(transport="stdio")
