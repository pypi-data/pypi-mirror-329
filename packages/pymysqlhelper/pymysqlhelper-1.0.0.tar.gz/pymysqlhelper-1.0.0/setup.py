from setuptools import setup, find_packages

setup(
    name="pymysqlhelper",
    version="1.0.0",
    description="A simple MySQL database helper for easy interactions",
    author="DEAMJAVA",
    author_email="deamminecraft3@gmail.com",
    packages=find_packages(),
    install_requires=["pymysql", "sqlalchemy"],
    python_requires=">=3.6",
)
