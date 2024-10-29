from litemultiagent.core.agent_manager import AgentManager

import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("log.txt", mode="w"),
        logging.StreamHandler()
    ]
)

# Create a logger
logger = logging.getLogger(__name__)
def main():
    agent_manager = AgentManager()
    from litemultiagent.tools.registry import Tool
    from dotenv import load_dotenv
    _ = load_dotenv()

    def calculate(operation, num1, num2):
        if operation == 'add':
            return num1 + num2
        elif operation == 'subtract':
            return num1 - num2
        elif operation == 'multiply':
            return num1 * num2
        elif operation == 'divide':
            if num2 != 0:
                return num1 / num2
            else:
                raise ValueError("Cannot divide by zero")
        else:
            raise ValueError("Invalid operation. Choices are 'add', 'subtract', 'multiply', 'divide'")

    name = 'calculate'
    func = calculate
    description = 'This is a function that takes two numbers and an operation (add, subtract, multiply, divide) as inputs and returns the result of the operation.'
    parameters = {'operation': {'type': 'string',
                                'description': 'Operation to be performed. Allowed operations are add, subtract, multiply and divide.'},
                  'num1': {'type': 'number', 'description': 'First number.'},
                  'num2': {'type': 'number', 'description': 'Second number.'}}

    new_tool = Tool(name, func, description, parameters)
    test_agent_config = {
        "name": "test_agent",
        "type": "atomic",
        "agent_class": "FunctionCallingAgent",
        "meta_data":
            {
                "meta_task_id": "io_subtask",
                "task_id": 1,
                "save_to": "supabase",
                "log": "log",
                "model_name": "gpt-4o-mini",
                "tool_choice": "auto"
            },
        "tool_names": ["read_file", "write_to_file", "generate_and_download_image"],
        "self_defined_tools": [new_tool],
        "agent_description": "test ai agent",
        "parameter_description": "test ai agent"
    }
    test_agent = agent_manager.get_agent(test_agent_config)

    # Example usage
    task = "calculate 3+4"
    result = test_agent.execute(task)
    print("Test Agent Result:", result)

    task = "calculate 3 times 4"
    result = test_agent.execute(task)
    print("Test Agent Result:", result)



if __name__ == "__main__":
    main()