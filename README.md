# OmniDimension Client Usage

This project demonstrates how to use the OmniDimension Python client to interact with the OmniDimension API, including listing agents and dispatching calls.

## Setup

1. Ensure you have Python installed.
2. Install the required dependencies (e.g., `omnidimension` package) in your virtual environment.
3. Set your API key as an environment variable:

```bash
export OMNIDIM_API_KEY="your_api_key_here"
```

On Windows PowerShell:

```powershell
setx OMNIDIM_API_KEY "your_api_key_here"
```

Alternatively, you can replace the API key directly in the scripts (not recommended for production).

## Listing Agents

To list all agents and get their IDs, run the `omni.py` script:

```bash
python omni.py
```

This will print a list of agents with their details. Use a valid `agent_id` from this list for dispatching calls.

## Dispatching a Call

The `call.py` script demonstrates how to dispatch a call to a specific number using an agent.

```python
import os
from omnidimension import Client

api_key = os.environ.get('OMNIDIM_API_KEY', 'your_api_key_here')
client = Client(api_key)

agent_id = 123  # Replace with a valid agent ID from the agent list
to_number = "+919821238977"  # Must include country code

response = client.call.dispatch_call(agent_id, to_number)
print(response)
```

**Important:** Replace `agent_id` with a valid ID obtained from the agent list. Using an invalid `agent_id` may result in a `500 Internal Server Error` from the API.

## Troubleshooting

- If you encounter a `500 Internal Server Error` when dispatching a call, verify that:
  - The `agent_id` is valid and exists on the server.
  - The `to_number` includes the correct country code and is in the correct format.
  - Your API key is valid and has the necessary permissions.

- Use the `omni.py` script to list agents and confirm valid IDs.

- Check your network connection and API server status.

## Additional Scripts

- `agentomni.py`: Example script to create a new agent.

```python
from omnidimension import Client
client = Client('your_api_key_here')

response = client.agent.create(
    name="Customer Support Agent",
    welcome_message="Hello! I'm your customer support assistant. How can I help you today?",
    context_breakdown=[
        {"title": "Purpose", "body": "This agent helps customers with product inquiries and support issues."}
    ]
)
print(response)
```

## License

This project is provided as-is without warranty. Use at your own risk.
