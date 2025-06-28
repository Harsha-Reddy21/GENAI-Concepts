class BaseOptimizer:
    """Base class for all tool-specific optimizers"""
    
    def __init__(self, tool_data):
        self.tool_data = tool_data
        self.name = "Generic Tool"
        self.capabilities = tool_data.get("capabilities", [])
        self.best_practices = tool_data.get("best_practices", [])
        self.limitations = tool_data.get("limitations", [])
    
    def optimize(self, prompt, additional_context=None):
        raise NotImplementedError("Each optimizer must implement its own optimize method")
    
    def get_tool_info(self):
        """Return information about this tool"""
        return {
            "name": self.name,
            "capabilities": self.capabilities,
            "best_practices": self.best_practices,
            "limitations": self.limitations
        } 