from setuptools import setup, find_packages

setup(
    name="daniel_zindi_utils",
    version="0.3.0",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "pandas",
        "datasets",
    ],
    author="Daniel Byiringiro",
    author_email="daniel.byiringiro@ashesi.edu.gh",
)