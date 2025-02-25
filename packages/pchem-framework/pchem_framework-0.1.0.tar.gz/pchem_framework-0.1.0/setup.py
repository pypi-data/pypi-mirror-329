from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pchem-framework",
    version="0.1.0",
    author="Ouedraogo Somkieta",
    author_email="s.r.a.ouedraogo@gmail.com",
    description="Practical chemistry calculations and data handling framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/somkietacode/pchem-framework",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.21.0",
        "pandas>=1.3.0",
        "matplotlib>=3.4.0",
        "pint>=0.18"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Chemistry",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education"
    ],
    python_requires='>=3.8',
)