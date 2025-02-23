from setuptools import setup, find_packages

setup(
    name="spssvalidate",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "hashlib",
        "time",
    ],
    author="Sumedh Patil",
    author_email="admin@aipresso.uk",
    description="A library to validate the authenticity and integrity of star maps.",
    url="https://github.com/Sumedh1599/spssvalidate",  # Optional: Link to your repository
)