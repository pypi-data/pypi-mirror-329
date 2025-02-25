from setuptools import find_packages, setup

name = "altrustworthyai"
# NOTE: Version is replaced by a regex script.
version = "0.6.9"
long_description = """
The AffectLog’s Trustworthy AI (ALT-AI) provides a suite of tools for the explanation, visualization, and understanding of complex machine learning models. It acts as a bridge between raw model output and actionable insights, making it easier for data scientists and stakeholders to interpret model predictions, understand feature importance, and evaluate model fairness and performance across different segments.

https://github.com/AffectLog360/altrustworthyai
"""
altrustworthyai_core_extra = [
    "debug",
    "notebook",
    "plotly",
    # "lime",  # no longer maintained
    "sensitivity",
    "shap",
    # "skoperules",  # no longer maintained
    "linear",
    "dash",
    # "treeinterpreter",  # no longer maintained
    "aplr",
]

setup(
    name=name,
    version=version,
    author="AffectLog Developer",
    author_email="hi@affectlog.com",
    description="ALT-AI provides a suite of tools for the explanation, visualization, and understanding of complex machine learning models.",
    long_description=long_description,
    url="https://github.com/AffectLog360/altrustworthyai",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "altrustworthyai-core[{}]=={}".format(",".join(altrustworthyai_core_extra), version)
    ],
)
