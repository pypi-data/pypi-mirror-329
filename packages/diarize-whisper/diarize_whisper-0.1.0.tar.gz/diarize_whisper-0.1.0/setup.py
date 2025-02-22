# setup.py
from setuptools import setup, find_packages

setup(
    name="diarize_whisper",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pydub",
        "torch",
        "pyannote.audio",
        "transformers",
    ],
    author="Samy Le Galloudec",
    author_email="samy.legalloudec@sodebo.fr",
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
            'asr_diarization=diarize_whisper.cli:main',
        ],
    },
)
