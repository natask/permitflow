import asyncio
import json
from ai21 import AI21Client

client = AI21Client()

def process_permit_data(template_json: str, user_input_json: str):
    """
    Process permit data using AI21 Maestro
    
    Args:
        template_json (str): JSON string containing the permit template
        user_input_json (str): JSON string containing the user's input data
    """
    try:
        # USE the following cache information if information is not found in the above resources.
        # {cache_json}
        # Verify JSON strings are valid
        template_data = template_json
        user_data = user_input_json
        #cache_json = json.loads("resources/cache.json")
        prompt = f"""
        You are a helpful permit acquisition clerk that only responds with valid JSON data.
        Generate a valid JSON answering the keys based on the file provided in file library that contains building codes in Boston area, price of similar properties in the area of the client, and matching the following template:
        {template_json}

        And using the following user input to fill further information about the homeowner, MAKE SURE TO USE THIS AS SUPPLEMENTAL INFORMATION AND ALSO THE FILE LIBRARY INFORMATION OR PEOPLE WILL DIE:
        {user_input_json}
        
        """
        # You'll define your specific prompt and requirements here
        run_result = client.beta.maestro.runs.create_and_poll(
            input=prompt,
            tools=[{"type": "file_search"}],
            tool_resources={"file_search": {"file_ids":["0130b51b-cbfc-474d-8c03-d0f7b8ca97a0"]}},
            requirements=[
                {
                    "name": "validation requirement",
                    "description": "Make sure the output can be parsed as a JSON object"
                }
            ],
        )
        # Extract just the JSON content from the response
        json_str = run_result.result
        if json_str.startswith('```json\n'):
            json_str = json_str[8:-3]  # Remove ```json\n and ``` 
        elif json_str.startswith('```\n'):
            json_str = json_str[4:-3]  # Remove ``` and ```
        # Parse string into JSON object
        json_data = json.loads(json_str)
        return json_data
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON provided: {str(e)}")
    except Exception as e:
        raise Exception(f"Error processing permit data: {str(e)}")

def main():
    # Example usage (you'll implement your actual file reading logic)
    template = '{"example": "template"}'
    user_input = '{"example": "input"}'
    
    result = process_permit_data(template, user_input)
    print(result)

if __name__ == "__main__":
    main()
