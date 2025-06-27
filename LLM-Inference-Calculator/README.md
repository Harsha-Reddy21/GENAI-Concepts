# LLM Inference Calculator

A calculator that estimates LLM inference costs, latency, and memory usage.

## Overview

Provides estimates for:
- Memory usage (GB)
- Inference latency (seconds)
- Cost per request (USD)
- Hardware compatibility

## Features

- Models: 7B, 13B, GPT-4
- Hardware: T4, A100, CPU
- Deployment: vLLM, HuggingFace, ONNX

## Usage

```bash
python inference_calculator.py
```

Input parameters:
- Model size (7B, 13B, or GPT-4)
- Number of tokens
- Batch size
- Hardware type (T4, A100, or CPU)
- Deployment mode (vLLM, HuggingFace, or ONNX)
