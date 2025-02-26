from setuptools import setup

setup(
    name="lockfile-extract",
    version="1.0.2",
    py_modules=["extract_versions"],
    entry_points={
        "console_scripts": [
            "lockfile-extract=extract_versions:main",
        ],
    },
)
