# LeanQuant

## Overview

This package provides efficient inference kernels for running non-uniformly quantized LeanQuant models on CUDA-enabled GPUs. LeanQuant is a scalable and accurate quantization algorithm that compresses large language models by 4-8x while maintaining competitive performance.

## Installation

Ensure your GPU supports CUDA 11 or CUDA 12. You can check your CUDA version with the command `nvidia-smi | grep CUDA`.

To install:
```bash
# For CUDA 11.x
pip install leanquant[cuda11]

# For CUDA 12.x
pip install leanquant[cuda12]
```

## Models

Quantized LeanQuant models are available for download on our HuggingFace page: [huggingface.co/LeanQuant](https://huggingface.co/LeanQuant)

## Technical Details

LeanQuant introduces an innovative loss-error-aware grid approach to quantization that significantly outperforms traditional methods. Our technique:

- **Achieves superior compression ratios**: Reduces model size by 4-8x without sacrificing capability
- **Preserves model intelligence**: Maintains performance comparable to full-precision models across challenging benchmarks
- **Optimizes GPU execution**: Features custom CUDA kernels specifically designed for non-uniform quantization format

The algorithm strategically allocates quantization precision based on parameter sensitivity, ensuring computational resources are focused where they matter most.

For a comprehensive explanation of our methodology and benchmark results, please refer to our [research paper](https://arxiv.org/pdf/2407.10032).

## Citation

If you find LeanQuant useful in your research or applications, please consider citing our work:

```bibtex
@inproceedings{
    zhang2025leanquant,
    title={LeanQuant: Accurate and Scalable Large Language Model Quantization with Loss-error-aware Grid},
    author={Tianyi Zhang and Anshumali Shrivastava},
    booktitle={The Thirteenth International Conference on Learning Representations},
    year={2025},
    url={https://openreview.net/forum?id=ISqx8giekS}
}
```