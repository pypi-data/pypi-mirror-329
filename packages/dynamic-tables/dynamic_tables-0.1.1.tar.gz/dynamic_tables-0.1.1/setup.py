from setuptools import setup, find_packages

setup(
    name="dynamic_tables",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "psycopg2",
    ],
    author="Scott Rodeo",
    author_email="signcactus@gmail.com",
    description="A dynamic table creation and management library for PostgreSQL",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/scottrodeo/dynamic-tables-python",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)

