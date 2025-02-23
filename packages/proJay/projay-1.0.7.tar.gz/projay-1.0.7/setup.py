from setuptools import setup

setup(
    name="proJay",
    version="1.0.7",
    py_modules=["go"],
    description="A lightning-fast Python project generator with perfect GitHub workflows. Zero config, instant setup.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",    
    author="Fonk",
    author_email="feelthefonk@gmail.com",
    url="https://github.com/FeelTheFonk/proJay",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)