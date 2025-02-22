# genaitopic

`genaitopic` is a Python package that performs stratified sampling on datasets and leverages Language Models (LLMs) to extract and combine thematic topics. It offers a configurable pipeline with options to view intermediate results (strata, text samples, initial themes) and also saves final outputs both as files and variables.

## Features

- **Stratified Sampling with Bootstraps:** Sample data based on demographic groups.
- **Text String Generation:** Convert DataFrame samples to formatted text strings.
- **Initial Theme Extraction:** Use an LLM to extract key topics.
- **Final Theme Combination:** Merge similar themes into distinct final topics.
- **Configurable Pipeline:** Adjust hyperparameters and view intermediate outputs.

## Installation

Clone the repository and install using pip:

```bash
git clone https://github.com/yourusername/genaitopic.git
cd genaitopic
pip install -e .
