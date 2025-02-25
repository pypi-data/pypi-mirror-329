import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="implicit-score",            # This is the name that will appear on PyPI
    version="0.1.2",            # Update as needed (semantic versioning)
    author="Yuxin Wang",
    author_email="yuxinwangcs@outlook.com",
    description="A learnable metric to calculate the implicitness of an English sentence",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/audreycs/impscore",  # or your project URL
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # or whichever you choose
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "pytorch", # Add any runtime dependencies here, like "numpy>=1.21.0"
        "sentence-transformers",
        "huggingface_hub"
    ],
)