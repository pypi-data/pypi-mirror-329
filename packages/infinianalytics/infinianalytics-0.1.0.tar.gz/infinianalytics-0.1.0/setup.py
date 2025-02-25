from setuptools import setup, find_packages

setup(
    name="infinianalytics",
    version="0.1.0",
    description="Librería para registrar eventos en la API de InfiniAnalytics",
    author="Infini Analytics",
    author_email="analytics@infini.es",
    packages=find_packages(),
    install_requires=[
        "requests>=2.32.3"
    ],
    python_requires=">=3.7",
)
