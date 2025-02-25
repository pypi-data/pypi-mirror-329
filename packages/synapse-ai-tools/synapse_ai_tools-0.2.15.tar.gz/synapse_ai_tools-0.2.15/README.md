# `synapse_ai`

`synapse_ai` is a Python package designed for artificial intelligence development, offering utilities for machine learning (ML), deep learning (DL), data processing, and model deployment. It provides a comprehensive set of tools for AI developers to efficiently create and deploy AI models.

## Features

- **Machine Learning**: Utilities to facilitate the development and training of machine learning models.
- **Deep Learning**: Tools and models specific to deep learning to accelerate AI development.
- **Data Processing**: A set of utilities to preprocess and transform datasets for model training.
- **Model Deployment**: Tools for easy deployment of AI models, including model evaluation and optimization.
- **Modular Design**: The package is designed with modular components, so you can use only what you need.

## Modules and Functions

### **Module `phonemes`**
1. **`phoneme`**: Transforms Spanish text into a simplified phonetic representation based on predefined rules.
2. **`accent`**: Applies prosodic accentuation to Spanish text based on predefined phonetic and grammatical rules.
3. **`dictionaries`**: Generates two dictionaries from the input text: a phoneme-to-index dictionary and a phoneme frequency dictionary.
4. **`phoneme_graphs`**: Visualizes the frequency of phonemes in a bar chart.

### **Module `mel_spectrograms`**
1. **`load_audio_to_mel`**: Converts an audio file to a mel spectrogram.
2. **`graph_mel_spectrogram`**: Visualizes and optionally saves a mel spectrogram as an image.

### **Module `eda`**
1. **`heatmap_correlation`**: Generates and optionally saves a heatmap of correlation values for selected columns in a DataFrame.
2. **`outliers`**: Analyzes numerical outliers in a specified column of a DataFrame, visualizing its distribution, boxplot, and basic statistics.
3. **`nulls`**: Analyzes and prints the number and percentage of null values in a specified column of a DataFrame.

## Installation

To install the package, you can use `pip`:

```bash
pip install synapse_ai_tools
