"""Conexão local com PostgreSQL do Comex Support Intelligence."""

import os
import sys
from pathlib import Path

import psycopg
from dotenv import load_dotenv


# Localiza a raiz do projeto independentemente do diretório atual.
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Carrega as configurações privadas do arquivo .env.
load_dotenv(PROJECT_ROOT / ".env")


def get_connection():
    """Cria uma conexão com o PostgreSQL usando variáveis de ambiente."""

    required_variables = [
        "DB_NAME",
        "DB_USER",
        "DB_PASSWORD",
    ]

    missing = [
        variable
        for variable in required_variables
        if not os.getenv(variable)
    ]

    if missing:
        raise ValueError(
            "Variáveis de ambiente ausentes: "
            + ", ".join(missing)
        )

    return psycopg.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        connect_timeout=5,
    )


def test_connection():
    """Verifica a conexão e identifica o banco e usuário ativos."""

    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        current_database(),
                        current_user,
                        current_schema(),
                        version();
                    """
                )

                database, user, schema, version = cursor.fetchone()

                print("\n=== COMEX SUPPORT INTELLIGENCE ===")
                print("Status: CONEXÃO BEM-SUCEDIDA")
                print(f"Banco: {database}")
                print(f"Usuário: {user}")
                print(f"Esquema: {schema}")
                print(f"PostgreSQL: {version.split(',')[0]}")

                return True

    except (psycopg.Error, ValueError) as error:
        print("\n=== COMEX SUPPORT INTELLIGENCE ===")
        print("Status: FALHA NA CONEXÃO")
        print(f"Tipo do erro: {type(error).__name__}")
        print("Verifique o PostgreSQL e as configurações do .env.")
        return False


if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1)
