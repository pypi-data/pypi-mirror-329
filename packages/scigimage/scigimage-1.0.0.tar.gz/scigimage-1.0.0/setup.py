from setuptools import setup, find_packages

setup(
    name="scigimage",
    version="1.0.0",
    author="Sumedh Patil",
    author_email="admin@aipress.uk",
    description="A lightweight library for generating dynamic star maps and animations.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Sumedh1599/scigimage",  # Replace with your GitHub repo URL
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "numpy",
        "Pillow",  # Temporary dependency; replace later with custom GIF encoder
    ],
)