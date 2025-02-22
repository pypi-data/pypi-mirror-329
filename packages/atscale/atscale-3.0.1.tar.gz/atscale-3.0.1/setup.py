import setuptools
from setuptools import setup


# read the contents of your README file
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

NAME = "atscale"
VERSION = "3.0.1"
DESCRIPTION = "The AI-Link package created by AtScale"
URL = "https://www.atscale.com/"
AUTHOR = "The AI-Link Development Team at AtScale"
AUTHOR_EMAIL = "ailink@atscale.com"
REQUIRES_PYTHON = ">=3.8.0"
REQUIRED = ["pandas>=2.2", "requests>=2.0.0", "aenum", "cryptography", "psycopg2-binary"]

SPARK_REQUIRED = ["pyspark>=3.4.0"]
JDBC_REQUIRED = ["jaydebeapi>=1.2.3"]

SQLALCHEMY_REQUIRED = ["sqlalchemy>=2.0"]
PYODBC_REQUIRED = ["pyodbc>=4.0.27"]

DATABRICKS_REQUIRED = ["databricks-sql-connector[sqlalchemy]>=3.0.0"]
# google-cloud-bigquery in pandas-gbq, just in case and for inspection
GBQ_REQUIRED = ["pandas-gbq!=0.17.6", "google-cloud-bigquery"]
IRIS_REQUIRED = PYODBC_REQUIRED
SNOWFLAKE_REQUIRED = SQLALCHEMY_REQUIRED + [
    "snowflake-sqlalchemy>=1.6.0",
    "snowflake-connector-python[pandas]>=2.7.9",
]
POSTGRES_REQUIRED = SQLALCHEMY_REQUIRED + ["psycopg2-binary"]
TEST_REQUIRED = [
    "pytest",
    "pytest-random-order",
    "scipy",
    "scikit-learn",
    "aws-secretsmanager-caching",
    "boto3",
]
DEV_REQUIRED = (
    GBQ_REQUIRED
    + DATABRICKS_REQUIRED
    + IRIS_REQUIRED
    + SNOWFLAKE_REQUIRED
    + POSTGRES_REQUIRED
    + JDBC_REQUIRED
    + SPARK_REQUIRED
    + TEST_REQUIRED
)

EXTRAS_REQUIRE = {
    "dev": DEV_REQUIRED,
    "test": TEST_REQUIRED,
    "gbq": GBQ_REQUIRED,
    "databricks": DATABRICKS_REQUIRED,
    "iris": IRIS_REQUIRED,
    "snowflake": SNOWFLAKE_REQUIRED,
    "jdbc": JDBC_REQUIRED,
    "spark": SPARK_REQUIRED,
    "postgres": POSTGRES_REQUIRED,
}

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    project_urls={
        "HomePage": URL,
        "Documentation": "https://documentation.atscale.com/ailink-container",
        "Release Notes": "https://documentation.atscale.com/ailink-container/release-notes",
    },
    packages=setuptools.find_packages(include=["atscale", "atscale.*"]),
    install_requires=REQUIRED,
    python_requires=REQUIRES_PYTHON,
    license_files=("LICENSE.md",),
    long_description=long_description,
    long_description_content_type="text/markdown",
    extras_require=EXTRAS_REQUIRE,
    classifiers=["Programming Language :: Python :: 3", "License :: Other/Proprietary License"],
)
