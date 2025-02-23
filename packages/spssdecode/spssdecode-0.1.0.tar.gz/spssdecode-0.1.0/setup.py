from setuptools import setup, find_packages

setup(
    name="spssdecode",
    version="0.1.0",
    author="Sumedh Patil",
    author_email="admin@aipresso.uk",
    description="A library to decode star maps into structured data.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/spssdecode",  # Optional: Link to your repository
    packages=find_packages(),
    install_requires=[
        "numpy",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)