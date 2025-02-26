import os
from distutils.command.install import install as _install

from setuptools import find_namespace_packages, find_packages, setup
from setuptools.command.install import install

PROJECT_DIR = os.path.dirname(__file__)
INFO = open(os.path.join(PROJECT_DIR, "INFO")).readlines()
INFO = dict(line.strip().split("=") for line in INFO)

DEPENDENCIES = open(os.path.join(PROJECT_DIR, "requirements.txt")).readlines()

setup(
    name="MedRoom.AI.DataEngineer",
    description="A Natural Language Processing Data Engineer",
    version=INFO["version"],
    author=INFO["author"],
    author_email=INFO["author_email"],
    url=INFO["url"],
    license=open(os.path.join(PROJECT_DIR, "LICENSE")).read(),
    packages=find_namespace_packages(
        include=[
            "medroom",
            "medroom.dna",
            "medroom.dna.processors",
            "medroom.dna.processors.*",
            "medroom.dna.processors.utils",
        ]
    ),
    install_requires=[d for d in DEPENDENCIES if "://" not in d],
    extras_require={"plotting": ["matplotlib==3.7.0", "seaborn==0.13.0"]},
    python_requires=">=3.8",
    # TO-DO: Fix dependency links : not working with bdist_wheel
    dependency_links=[
        "git+https://github.com/explosion/spacy-models/releases/download/pt_core_news_sm-3.2.0/pt_core_news_sm-3.2.0.tar.gz"
    ],
    tests_require=["pytest", "parameterized"],
    zip_safe=False,
)
