import setuptools
import sys
import subprocess

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

def is_package_installed(package_name):
    """Check if a package is installed."""
    try:
        subprocess.run([sys.executable, "-m", "pip", "show", package_name],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

# Check if torch or pytorch is already installed
torch_installed = is_package_installed("torch")
pytorch_installed = is_package_installed("pytorch")

# If neither is installed, add "torch" to install_requires
install_requires = ["sentence-transformers", "huggingface_hub"]
if not torch_installed and not pytorch_installed:
    install_requires.append("torch")

setuptools.setup(
    name="implicit-score",            # This is the name that will appear on PyPI
    version="0.1.3",            # Update as needed (semantic versioning)
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
    python_requires=">=3.7",
    install_requires=install_requires
)