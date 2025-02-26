from setuptools import setup

# Read the contents of README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="lockfile-extract",
    version="1.0.3",
    py_modules=["extract_versions"],
    entry_points={
        "console_scripts": [
            "lockfile-extract=extract_versions:main",
        ],
    },
    author="Sidhan Shamil M",
    author_email="sidhanshamil3@gmail.com",
    description="Extract package versions from package-lock.json without installing dependencies!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sidhanshamil/lockfile-extract",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
