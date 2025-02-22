# diarize_whisper

**diarize_whisper** est une librairie Python permettant la transcription automatique (ASR) et la diarisation d'un fichier audio en utilisant des modèles HuggingFace. Elle offre des outils pour :

- Convertir un fichier audio en format WAV mono 16kHz.
- Découper l'audio en segments de durée configurable.
- Transcrire chaque segment via un modèle ASR (par exemple, `openai/whisper-large-v3-turbo`).
- Appliquer une diarisation avec le modèle `pyannote/speaker-diarization-3.1` pour identifier les différents locuteurs.
- Fusionner les résultats de la transcription et de la diarisation afin de reconstruire les dialogues avec attribution des locuteurs.
- Fournir une interface en ligne de commande (CLI) pour faciliter l'exécution du pipeline complet.

## Table des matières

- [Fonctionnalités](#fonctionnalités)
- [Installation](#installation)
- [Utilisation](#utilisation)
  - [Utilisation en tant que librairie Python](#utilisation-en-tant-que-librairie-python)
  - [Utilisation via la CLI](#utilisation-via-la-cli)
- [Structure du projet](#structure-du-projet)
- [Configuration](#configuration)
- [Licence](#licence)

## Fonctionnalités

- **Conversion Audio**  
  Convertit n'importe quel fichier audio en un fichier WAV mono 16kHz afin d'assurer la compatibilité avec les modèles de transcription.

- **Segmentation Audio**  
  Découpe le fichier WAV en segments de durée fixe (par défaut 25 secondes, mais paramétrable) pour faciliter le traitement par le modèle ASR.

- **Transcription (ASR)**  
  Utilise un modèle de transcription (ASR) de HuggingFace pour extraire le texte du fichier audio. Le modèle par défaut est `openai/whisper-large-v3-turbo`.

- **Diarisation**  
  Applique la diarisation afin d'identifier et d'attribuer les segments de texte aux différents locuteurs à l'aide du modèle `pyannote/speaker-diarization-3.1`.

- **Fusion et Reconstruction des Dialogues**  
  Combine les résultats de l'ASR et de la diarisation, ajuste les timestamps et attribue les dialogues aux locuteurs, en affinant la segmentation pour de meilleurs résultats.

- **Interface en Ligne de Commande**  
  Un outil CLI (`asr_diarization`) permet d'exécuter l'ensemble du pipeline (conversion, segmentation, ASR, diarisation et reconstruction) en une seule commande.

## Installation

### Prérequis

- Python 3.10 ou supérieur.
- FFMPEG installé sur le poste.
- Un environnement compatible avec `torch`, `pydub`, `pyannote.audio` et `transformers`.

## Utilisation