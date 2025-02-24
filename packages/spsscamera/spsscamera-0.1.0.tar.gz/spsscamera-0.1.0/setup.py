from setuptools import setup, find_packages

setup(
    name="spsscamera",
    version="0.1.0",
    author="Sumedh Patil",
    author_email="admin@aipresso.uk",
    description="A library to access the device's camera and preprocess images for decoding.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/spsscamera",  # Optional: Link to your repository
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)