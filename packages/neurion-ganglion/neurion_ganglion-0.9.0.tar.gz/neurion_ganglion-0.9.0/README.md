# Neurion Ganglion - Ion Framework

## Overview
Neurion Ganglion provides a framework for defining, deploying, and managing Ions – decentralized computational units that operate within the Neurion ecosystem. This repository offers a streamlined way to create and register Ions, either as self-hosted services or pre-existing services ready for registration.

## Features
- Define input and output schemas using Pydantic.
- Register Ions with Neurion automatically or manually.
- Health-check endpoints for ensuring service availability.
- Auto-recovery mechanism for self-hosted Ions.
- Easy-to-use decorators for defining execution logic.
- Integrated Ganglion Server for managing pathways and processing Ion calls.
- Support for both **localnet** and **alpha testnet** environments.

## Installation

```sh
pip install neurion-ganglion
```

## Network Configuration
Neurion supports multiple networks. Initialize a network configuration before using Ganglion or Ions:

```python
from neurionpy.synapse.config import NetworkConfig

# Choose the appropriate network
config = NetworkConfig.neurion_localnet()  # For local development
# config = NetworkConfig.neurion_alpha_testnet()  # For testnet
```

## Creating an Ion
You can create an Ion in two different ways:

### 1. Self-Hosting Ion (Auto-Registering)
This mode runs the Ion server locally and automatically registers it with Neurion.

```python
from pydantic import BaseModel
from neurion_ganglion.ion.ion import Ion, ion_handler
from neurion_ganglion.custom_types.capacity import Capacity
from neurionpy.synapse.config import NetworkConfig

config = NetworkConfig.neurion_localnet()  # Set network config

# Define Input Schema
class MyInputSchema(BaseModel):
    task_id: str
    parameters: int

# Define Output Schema
class MyOutputSchema(BaseModel):
    message: str
    result: float

# Use decorator to attach schemas
@ion_handler(MyInputSchema, MyOutputSchema)
def my_ion_handler(data: MyInputSchema) -> MyOutputSchema:
    return MyOutputSchema(message="Success", result=12)

# Start Ion Server
if __name__ == "__main__":
    description = "My custom Ion server"
    stake = 20000000
    fee_per_thousand_calls = 1
    capacities = [Capacity.SCRAPER, Capacity.AI_AGENT]
    Ion.create_self_hosting_ion(config, description, stake, fee_per_thousand_calls, capacities, my_ion_handler).start()
```

### 2. Starting a Pure Ion Server & Registering it
If you want to set up multiple backend Ion servers and manually register them, you can start a **pure Ion server** first, note its public IP, and then use the registration function.

#### **Step 1: Start the Pure Ion Server**
```python
from neurion_ganglion.ion.ion import Ion
from pydantic import BaseModel
from neurionpy.synapse.config import NetworkConfig

config = NetworkConfig.neurion_localnet()  # Set network config

# Define Input Schema
class MyInputSchema(BaseModel):
    task_id: str
    parameters: int

# Define Output Schema
class MyOutputSchema(BaseModel):
    message: str
    result: float

@ion_handler(MyInputSchema, MyOutputSchema)
def my_ion_handler(data: MyInputSchema) -> MyOutputSchema:
    return MyOutputSchema(message="Success", result=12)

# Start a pure Ion server
if __name__ == "__main__":
    Ion.start_pure_ion_server(config, my_ion_handler)
```

#### **Step 2: Manually Register the Running Ion Server**
Once the pure Ion server is running, note its **IP address** and use the following script to register it:

```python
from neurion_ganglion.ion.ion import Ion
from neurion_ganglion.custom_types.capacity import Capacity
from neurionpy.synapse.config import NetworkConfig

config = NetworkConfig.neurion_localnet()  # Set network config

description = "My external Ion server"
stake = 20000000
fee_per_thousand_calls = 1
capacities = [Capacity.SCRAPER, Capacity.AI_AGENT]
endpoints = ["http://<noted-public-ip>:8000"]  # Replace <noted-public-ip> with actual IP

Ion.create_server_ready_ion(config, description, stake, fee_per_thousand_calls, capacities, MyInputSchema, MyOutputSchema, endpoints).register_ion()
```

## Using Pathways
A **Pathway** defines a structured flow between multiple Ions.

```python
from neurion_ganglion.ion.pathway import Pathway
from neurionpy.synapse.config import NetworkConfig

config = NetworkConfig.neurion_localnet()  # Set network config

# Initialize Pathway by ID
pathway = Pathway.of_id(config, 1)

# Call Pathway
response = pathway.call({"task_id": "1234", "parameters": 100})
print(response)
```

## Ganglion Server
The **Ganglion Server** handles requests, routing them to the appropriate **Ion** or **Pathway**.

```python
from neurion_ganglion.ganglion.server import GanglionServer
from neurionpy.synapse.config import NetworkConfig

config = NetworkConfig.neurion_localnet()  # Set network config

# Start Ganglion Server
GanglionServer.start(config)
```

## Health Check
All Ions expose a `/health` endpoint that can be used to check their availability.

```sh
curl http://localhost:8000/health
```

## License
This project is licensed under the MIT License.

