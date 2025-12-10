# Multilingual Negation Benchmark for Vision-Language Models

A benchmark for evaluating negation understanding in vision-language models across seven typologically diverse languages.

## Authors

**Gwen Flusche, Hara Moraitaki, Sarah Pan, Sky Pulling**  
MIT · 6.3950 Fall 2025

{gflusche, hmor, sarahpan, spulling}@mit.edu

## Overview

Vision-language models (VLMs) exhibit **affirmation bias**: a tendency to match captions like "there is no boat" to images containing boats, simply because the word "boat" appears. While prior work has documented this failure in English, negation manifests differently across languages through varying morphology, word order, and script systems.

This repository provides the first human-verified multilingual negation benchmark, enabling evaluation of how VLMs handle negation across linguistic diversity.

## Languages

| Language | Script | Family | Negation Type |
|----------|--------|--------|---------------|
| English | Latin | Indo-European | Adverbial |
| Spanish | Latin | Indo-European | Adverbial |
| Greek | Greek | Indo-European | Verbal/particle |
| Russian | Cyrillic | Indo-European | Morphological |
| Mandarin Chinese | Logographic | Sino-Tibetan | Isolating particles |
| Arabic | Arabic (RTL) | Afro-Asiatic | Cliticized |
| Tagalog | Latin | Austronesian | Particle-based |

## Models Evaluated

- **CLIP** (ViT-B/32)
- **SigLIP** (multilingual)
- **MultiCLIP** (clip-ViT-B-32-multilingual-v1)
- **SpaceVLM** — subspace-based negation correction method

## Key Findings

1. **CLIP** shows severe degradation on non-Latin-script languages (below chance for Arabic, Greek, Russian, Tagalog)
2. **MultiCLIP** achieves highest and most uniform accuracy across languages
3. **SpaceVLM** produces substantial gains for English, Greek, Spanish, and Tagalog, but shows varied effectiveness for Chinese, Arabic, and Russian

## Dataset

Built upon NegBench (Alhamoud et al., 2025), with captions translated via Google Translate and verified by native speakers. Each sample presents an image with 4 candidate captions for a multiple-choice ranking task.


## Acknowledgments

This work builds upon two papers:

- **NegBench**: Alhamoud, K., Alshammari, S., Tian, Y., Li, G., Torr, P., Kim, Y., & Ghassemi, M. (2025). [Vision-language models do not understand negation](https://arxiv.org/abs/2501.09425). *arXiv:2501.09425*

- **SpaceVLM**: Kazemi Ranjbar, S., Alhamoud, K., & Ghassemi, M. (2025). [SpaceVLM: Sub-space modeling of negation in vision-language models](https://arxiv.org/abs/2511.12331). *arXiv:2511.12331*

