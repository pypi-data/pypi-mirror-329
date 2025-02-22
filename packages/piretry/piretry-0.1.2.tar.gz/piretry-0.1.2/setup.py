from setuptools import setup, find_packages

# Read README.md for the long description
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="piretry",  # Use a clean, simple name for PyPI
    version="0.1.2",
    author="APTIVMIND",
    author_email="aptivmind@gmail.com",  # Replace with a valid email
    description="A retry decorator for Python functions supporting both sync and async.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/APTIVMIND/piretry",  # Replace with the actual repo link
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.12",
)
