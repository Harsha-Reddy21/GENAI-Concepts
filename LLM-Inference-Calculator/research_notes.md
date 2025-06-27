# LLM Inference Research Notes

## Basic Concepts of LLM Inference

### Model Architecture
- **Transformer Architecture**: Most LLMs use transformer-based architectures with attention mechanisms
- **Parameters**: Model size is measured in number of parameters (e.g., 7B = 7 billion parameters)
- **Layers**: Composed of multiple transformer layers with self-attention and feed-forward networks

### Inference Process
1. **Tokenization**: Convert input text to tokens (subword units)
2. **Forward Pass**: Process tokens through transformer layers
3. **KV Cache**: Store key-value pairs from previous tokens to speed up generation
4. **Sampling**: Generate next token based on probability distribution
5. **Repeat**: Continue generating tokens until completion

### Key Metrics
- **Latency**: Time to generate a response (affected by model size, hardware, batch size)
- **Throughput**: Number of tokens generated per second
- **Memory Usage**: VRAM required for model weights and inference state
- **Cost**: Hardware costs + API costs (for commercial models)

## Model Comparison

| Aspect | 7B Model (e.g., Llama 2 7B) | 13B Model (e.g., Llama 2 13B) | GPT-4 |
|--------|------------------------------|-------------------------------|-------|
| **Parameters** | 7 billion | 13 billion | ~1.76 trillion (estimated) |
| **Memory Requirements** | ~14 GB (base) | ~26 GB (base) | Cloud API only |
| **Inference Speed** | Fastest of the three | ~1.8x slower than 7B | Varies (API-dependent) |
| **Quality** | Good for simple tasks | Better reasoning than 7B | State-of-the-art |
| **Hardware** | Consumer GPUs (≥16GB VRAM) | Gaming/Pro GPUs (≥32GB VRAM) | API only |
| **Quantization Options** | 4-bit, 8-bit possible | 4-bit, 8-bit possible | N/A (API only) |
| **Cost** | Free (open-source) | Free (open-source) | ~$0.03 per 1K tokens |

## Optimization Techniques

### Quantization
- **FP16**: Half-precision (16-bit) floating point - 2x memory reduction
- **INT8**: 8-bit integer quantization - 4x memory reduction
- **INT4**: 4-bit integer quantization - 8x memory reduction
- **Trade-offs**: Lower precision = lower memory usage but potential quality degradation

### Inference Engines
- **vLLM**: Optimized for throughput with PagedAttention
- **ONNX Runtime**: Cross-platform acceleration
- **TensorRT-LLM**: NVIDIA-specific optimizations
- **llama.cpp**: CPU inference with minimal dependencies

### KV Cache Optimization
- **Key-Value Caching**: Stores intermediate attention values to avoid recomputation
- **Memory Impact**: KV cache scales with batch size × sequence length × model dimensions
- **Continuous Batching**: Dynamic allocation of resources for multiple requests

## Hardware Considerations

### GPU Options
- **Consumer GPUs (RTX series)**: Good for smaller models (7B-13B)
- **Data Center GPUs (A100, H100)**: Required for larger models or high throughput
- **Multi-GPU Setups**: Model parallelism for larger models

### CPU Inference
- **Possible but slow**: 10-20x slower than GPU inference
- **Quantization required**: INT8/INT4 quantization essential
- **Best for**: Small models, low throughput requirements

## Deployment Considerations
- **Scaling**: Horizontal vs. vertical scaling strategies
- **Caching**: Response caching for common queries
- **Prompt Engineering**: Efficient prompts reduce token usage and latency
- **Streaming**: Token-by-token streaming improves perceived latency 