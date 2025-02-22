# setup.py
from setuptools import setup, find_packages
import os

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="diarize_whisper",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "pydub",
        "torch",
        "pyannote.audio",
        "transformers",
    ],
    author="Samy Le Galloudec",
    author_email="samy.legalloudec@gmail.com",
    description="Librairie pour la transcription ASR et la diarisation",
    # url="https://github.com/votrecompte/diarize_whisper",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    entry_points={
        'console_scripts': [
            'diarize_whisper=diarize_whisper.cli:main',
        ],
    },
)
