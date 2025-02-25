from setuptools import setup, find_packages

setup(
    name="solai-db",
    packages=find_packages(
        include=["shared_db", "shared_db.*"]
    ),  # This will include all subpackages
    version="0.1.3",
    author="SolAI",
    description="The database for SolAI",
    install_requires=[
        "sqlalchemy>=2.0.0",
        "psycopg2-binary>=2.9.0",
    ],
)
