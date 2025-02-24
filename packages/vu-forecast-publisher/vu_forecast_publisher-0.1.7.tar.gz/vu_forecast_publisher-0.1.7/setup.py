from setuptools import setup, find_packages

setup(
    name="vu_forecast_publisher",
    version="0.1.7",
    description="A library for publishing forecast data to an API",
    author="Ricardo Teixeira",
    author_email="ricardo.teixeira@obiio.com",
    packages=find_packages(),
    install_requires=[
        "requests",
        "pandas",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)