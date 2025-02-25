from setuptools import find_packages, setup

name = "altrustworthyai-api"
# NOTE: Versioning for altrustworthyai-api does not update step-lock with other altrustworthyai packages.
version = "0.0.1"
long_description = """
Minimal dependency ALTrustworthyAI API for machine learning interpretability.

https://github.com/AffectLog360/altrustworthyai
"""

setup(
    name=name,
    version=version,
    author="AffectLog Developer",
    author_email="hi@affectlog.com",
    description="Fit interpretable machine learning models. Explain blackbox machine learning.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AffectLog360/altrustworthyai",
    packages=find_packages(),
    package_data={},
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "slicer>=0.0.5",
    ],
)
