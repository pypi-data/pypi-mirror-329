from setuptools import setup, find_packages

setup(
    name="onesource-db",
    packages=find_packages(
        include=["onesource_db", "onesource_db.*"]
    ),  # This will include all subpackages
    version="0.1.0",
    author="OneSource",
    description="The shared database for OneSource",
    install_requires=[
        "sqlalchemy>=2.0.0",
        "python-dotenv>=1.0.0",
        "psycopg2-binary>=2.9.0",
        # other dependencies
    ],
)
