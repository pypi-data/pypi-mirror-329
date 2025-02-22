# AZTP Client Python

AZTP (Agentic Zero Trust Protocol) Client is an enterprise-grade identity service client that provides secure workload identity management using AZTP standards. The client library facilitates secure communication between workloads by managing digital identities and certificates.

## Installation

```bash
pip install aztp-client
```

## Requirements

- Python 3.8 or higher

## Quick Start

```python
from aztp_client import Aztp

# Initialize client
client = Aztp(api_key="your-api-key")

# Create a secure agent
agent = await client.secure_connect(name="service1")

# Verify identity
is_valid = await client.verify_identity(agent)

# Verify identity using agent name (multiple methods)
is_valid = await client.verify_identity_using_agent_name(name)
is_valid = await client.verify_identity_using_agent_name(full_aztp_id)
is_valid = await client.verify_identity_using_agent_name(
    name=name,
    trust_domain="aztp.network",
    workload="workload",
    environment="production",
    method="node"
)

# Get identity details
identity = await client.get_identity(agent)
```
## Example

```python
import asyncio
import os
from aztp_client import Aztp
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def main():
    # Initialize the client with your API key
    client = Aztp(
        api_key=os.getenv("AZTP_API_KEY"),
    )
    name = os.getenv("AZTP_AGENT_NAME")

    try:
        crewAgent = {}
        
        # Create a secure agent
        print("\nCreating secure agent...")
        agent = await client.secure_connect(crewAgent, name="MyAgent") # you may edit the name to your liking
        print(f"Agent created successfully!")
        
        if agent.identity.aztp_id:
            print(f"Agent: {agent.identity.aztp_id}")

        
        # Verify the identity
        print("\nVerifying identity...")
        is_valid = await client.verify_identity(agent)
        print(f"Identity valid: {is_valid}")

        # Verify identity using agent name (multiple methods)
        print("\nVerifying identity using agent name...")
        
        # Using default parameters
        is_valid = await client.verify_identity_using_agent_name(name)
        print(f"Identity valid (defaults): {is_valid}")
        
        # Using full AZTP ID
        full_aztp_id = f"aztp://aztp.network/workload/production/node/{name}"
        is_valid = await client.verify_identity_using_agent_name(full_aztp_id)
        print(f"Identity valid (full ID): {is_valid}")
        
        # Using explicit parameters
        is_valid = await client.verify_identity_using_agent_name(
            name=name,
            trust_domain="aztp.network",
            workload="workload",
            environment="production",
            method="node"
        )
        print(f"Identity valid (explicit params): {is_valid}")
        
        # Get identity details
        print("\nGetting identity details...")
        identity = await client.get_identity(agent)
        if identity:
            print(f"Retrieved identity: {identity}")
        else:
            print("No identity found") 

    except ConnectionError as e:
        print(f"Connection Error: Could not connect to the AZTP server. Please check your connection and server URL.")
        print(f"Details: {e}")
    except Exception as e:
        print(f"Error: {str(e)}")
        print("\nCurrent configuration:")
        print(f"Base URL: {client.config.base_url}")
        print(f"Environment: {client.config.environment}")
        print("API Key: ********")  # Don't print the API key for security

if __name__ == "__main__":
    asyncio.run(main())
```

## Features

- Workload Identity Management using AZTP standards
- Certificate Management (X.509)
- Secure Communication
- Identity Verification
- Metadata Management
- Environment-specific Configuration

## License

MIT License 