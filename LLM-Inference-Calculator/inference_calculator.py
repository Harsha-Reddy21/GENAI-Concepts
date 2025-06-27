import math

class InferenceCalculator:
    def __init__(self):
        self.models = {
            "7B": {"params": 7e9, "mem_per_param": 2},
            "13B": {"params": 13e9, "mem_per_param": 2},
            "GPT-4": {"params": 1.76e12, "mem_per_param": 2},
        }

        self.hardware = {
            "T4": {"vram": 15.9, "compute_factor": 1.0, "cost_per_hour": 0.35},
            "A100": {"vram": 80, "compute_factor": 5.0, "cost_per_hour": 3.0},
            "CPU": {"vram": 0, "compute_factor": 0.2, "cost_per_hour": 0.1},
        }
        
        self.deployment_modes = {
            "vLLM": {"memory_factor": 1.05, "speed_factor": 1.5},
            "HuggingFace": {"memory_factor": 1.2, "speed_factor": 1.0},
            "ONNX": {"memory_factor": 0.8, "speed_factor": 1.2},
        }
    
    def calculate_memory_usage(self, model_size, batch_size, deployment_mode):
        model_params = self.models[model_size]["params"]
        mem_per_param = self.models[model_size]["mem_per_param"]
        
        base_memory = model_params * mem_per_param
        
        kv_cache = model_params * 0.08 * batch_size
        
        # Apply deployment mode memory factor
        total_memory = (base_memory + kv_cache) * self.deployment_modes[deployment_mode]["memory_factor"]
        
        return total_memory / 1e9  # Convert to GB
    
    def calculate_latency(self, model_size, tokens, batch_size, hardware_type, deployment_mode):
        # Base latency calculation
        base_latency = (self.models[model_size]["params"] / 1e9) * tokens * 0.001
        
        # Adjust for hardware speed
        hardware_adjusted = base_latency / self.hardware[hardware_type]["compute_factor"]
        
        # Batch processing efficiency
        if batch_size > 1:
            batch_factor = 1 + math.log(batch_size) / 2
            hardware_adjusted = hardware_adjusted * batch_size / batch_factor
            
        return hardware_adjusted / self.deployment_modes[deployment_mode]["speed_factor"]
    
    def calculate_cost(self, model_size, tokens, hardware_type, latency):
        # Hardware cost
        hourly_cost = self.hardware[hardware_type]["cost_per_hour"]
        cost_per_second = hourly_cost / 3600
        hardware_cost = latency * cost_per_second
        
        # API cost for GPT-4
        token_cost = 0
        if model_size == "GPT-4":
            token_cost = tokens * 0.00003
            
        return hardware_cost + token_cost
    
    def check_hardware_compatibility(self, model_size, batch_size, hardware_type, deployment_mode):
        required_memory = self.calculate_memory_usage(model_size, batch_size, deployment_mode)
        available_memory = self.hardware[hardware_type]["vram"]
        
        if hardware_type == "CPU":
            return "Compatible with CPU but extremely slow"
        
        if required_memory > available_memory:
            return f"Not compatible - Requires {required_memory:.2f}GB but only {available_memory}GB available"
        else:
            headroom = (available_memory - required_memory) / available_memory * 100
            if headroom < 10:
                return f"Compatible but limited memory headroom ({headroom:.1f}%)"
            else:
                return f"Compatible with good memory headroom ({headroom:.1f}%)"
    
    def estimate_inference(self, model_size, tokens, batch_size, hardware_type, deployment_mode):
        memory_usage = self.calculate_memory_usage(model_size, batch_size, deployment_mode)
        latency = self.calculate_latency(model_size, tokens, batch_size, hardware_type, deployment_mode)
        cost = self.calculate_cost(model_size, tokens, hardware_type, latency)
        compatibility = self.check_hardware_compatibility(model_size, batch_size, hardware_type, deployment_mode)
        
        return {
            "model_size": model_size,
            "memory_usage_gb": memory_usage,
            "latency_seconds": latency,
            "cost_usd": cost,
            "hardware_compatibility": compatibility
        }

def get_user_input():
    print("\n===== LLM Inference Calculator =====\n")
    
    # Model size input
    print("Available model sizes: 7B, 13B, GPT-4")
    model_size = input("Enter model size: ").strip()
    while model_size not in ["7B", "13B", "GPT-4"]:
        print("Invalid model size. Please enter 7B, 13B, or GPT-4.")
        model_size = input("Enter model size: ").strip()
    
    # Tokens input
    tokens = input("Enter number of tokens: ").strip()
    while not tokens.isdigit() or int(tokens) <= 0:
        print("Invalid token count. Please enter a positive number.")
        tokens = input("Enter number of tokens: ").strip()
    tokens = int(tokens)
    
    # Batch size input
    batch_size = input("Enter batch size (default 1): ").strip()
    batch_size = 1 if not batch_size else int(batch_size)
    
    # Hardware type input
    print("Available hardware types: T4, A100, CPU")
    hardware_type = input("Enter hardware type (default T4): ").strip()
    hardware_type = "T4" if not hardware_type else hardware_type
    
    # Deployment mode input
    print("Available deployment modes: vLLM, HuggingFace, ONNX")
    deployment_mode = input("Enter deployment mode (default vLLM): ").strip()
    deployment_mode = "vLLM" if not deployment_mode else deployment_mode
    
    return model_size, tokens, batch_size, hardware_type, deployment_mode

if __name__ == "__main__":
    calculator = InferenceCalculator()
    
    # Get user input
    model_size, tokens, batch_size, hardware_type, deployment_mode = get_user_input()
    
    # Calculate inference metrics
    result = calculator.estimate_inference(
        model_size=model_size,
        tokens=tokens,
        batch_size=batch_size,
        hardware_type=hardware_type,
        deployment_mode=deployment_mode
    )
    
    # Display results
    print("\n===== Results =====")
    print(f"Model: {model_size}")
    print(f"Tokens: {tokens}")
    print(f"Batch Size: {batch_size}")
    print(f"Hardware: {hardware_type}")
    print(f"Deployment: {deployment_mode}")
    print("\n--- Estimates ---")
    print(f"Memory Usage: {result['memory_usage_gb']:.2f} GB")
    print(f"Latency: {result['latency_seconds']:.4f} seconds")
    print(f"Cost: ${result['cost_usd']:.6f}")
    print(f"Hardware Compatibility: {result['hardware_compatibility']}")
    print("===================\n") 