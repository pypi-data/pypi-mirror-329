from setuptools import setup, find_packages

setup(
    name="apollo-tracker",
    version="0.1.2",
    description="A lightweight Flask middleware that captures and reports errors to Apollo, a centralized error tracking system.",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/TORNIXTECH/apollo-tracker",  # Add your repo
    project_urls={
        "Documentation": "https://github.com/TORNIXTECH/apollo-tracker/wiki",
        "Source Code": "https://github.com/TORNIXTECH/apollo-tracker",
        "Issue Tracker": "https://github.com/TORNIXTECH/apollo-tracker/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: Flask",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)