from setuptools import find_packages, setup

name = "altrustworthyai"
# NOTE: Version is replaced by a regex script.
version = "0.7.0"
long_description = """
In the beginning machines learned in darkness, and data scientists struggled in the void to explain them.

Let there be light.

https://github.com/AffectLog360/altrustworthyai/
"""
interpret_core_extra = [
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
    author="ALTrustworthyAI",
    author_email="hi@affectlog.com",
    description="Fit interpretable models. Explain blackbox machine learning.",
    long_description=long_description,
    url="https://github.com/AffectLog360/altrustworthyai/",
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
        "altrustworthyai-core[{}]=={}".format(",".join(interpret_core_extra), version)
    ],
)
