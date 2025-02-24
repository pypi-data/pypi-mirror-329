# setup.py
from setuptools import setup, find_packages

setup(
    name="currency_to_words",  # Name of your package
    version="0.1.0",  # Version of your package
    packages=find_packages(),  # Automatically find all packages in the project
    description="A library to convert currency to words in Indian numbering system",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Madhanagopal Mallayan",  # Replace with your name
    author_email="madhanagopalpro@gmail.com",  # Replace with your email
    url="https://github.com/Madhan-raio-97/currency_to_words",  # Your package's GitHub URL
    license="MIT",  # License type (MIT, GPL, etc.)
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Define the minimum Python version required
)
