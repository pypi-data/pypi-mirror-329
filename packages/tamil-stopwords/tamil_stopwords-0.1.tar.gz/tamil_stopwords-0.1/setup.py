from setuptools import setup

setup(
    name="tamil_stopwords",
    version="0.1",
    description="A simple Tamil stopwords list for NLP preprocessing",
    author="Paithra Harini Sivakumar",
    author_email="pavitra040604@gmail.com",
    packages=["tamil_stopwords"],
    package_data={"tamil_stopwords": ["tamil_stopwords_cleaned.txt"]},
    install_requires=[],
)
