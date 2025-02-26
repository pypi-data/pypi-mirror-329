from setuptools import setup, find_packages


# Ensure UTF-8 encoding while reading README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setup(
    name="random-ml",
    version="0.1.0",
    author="Your Name",
    author_email="your_email@example.com",
    description="An implementation of MLPedRVFL with Boosting and Bagging support.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yuvrajiro/random-ml",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "torch",
        "scikit-learn"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
