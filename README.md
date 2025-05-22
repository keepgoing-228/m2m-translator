# M2M100 Translation Project

This project uses Facebook's M2M100 multilingual translation model to translate text from English to Chinese. It processes data stored in Parquet format, performs the translations, and saves the results.

## Overview

The project consists of two main components:
1. A translation script that processes data and performs translations
2. A utility script to convert Parquet files to CSV format

## Requirements

- Python 3.x
- PyTorch
- Transformers library (Hugging Face)
- Polars
- Pandas

## Installation
1. Build the docker image
```bash
./build.sh
```

2. Run the docker container
```bash
./launch.sh
```

## Usage
```bash
python translation.py
```

