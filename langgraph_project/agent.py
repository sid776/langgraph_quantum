class Agent:
    def __init__(self, name, skill, tools=None):
        self.name = name
        self.skill = skill
        self.tools = tools if tools else {}
        
    def add_tool(self, tool_name, tool_function):
        self.tools[tool_name] = tool_function
        
    def perform_task(self):
        print(f"\nAgent {self.name} is active:")
        print(f"Specialized in: {self.skill}")
        if self.tools:
            print("Available tools:")
            for tool_name in self.tools:
                print(f"- {tool_name}")
            
            # Execute tools if available
            for tool_name, tool_function in self.tools.items():
                print(f"\nExecuting {tool_name}:")
                tool_function() 