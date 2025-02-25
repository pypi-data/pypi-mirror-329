# Neurion Ganglion - Ion Framework

## Overview
Neurion Ganglion provides a framework for defining, deploying, and managing Ions – decentralized computational units that operate within the Neurion ecosystem. This repository offers a streamlined way to create and register Ions, either as self-hosted services or pre-existing services ready for registration.

## Features
- Define input and output schemas using Pydantic.
- Register Ions with Neurion automatically or manually.
- Health-check endpoints for ensuring service availability.
- Auto-recovery mechanism for self-hosted Ions.
- Easy-to-use decorators for defining execution logic.

## Installation

```sh
pip install neurion-ganglion
```

## Creating an Ion
You can create an Ion in two different ways:

### 1. Self-Hosting Ion (Auto-Registering)
This mode runs the Ion server locally and automatically registers it with Neurion.

```python
from pydantic import BaseModel
from neurion_ganglion.ion.ion import Ion, ion_handler
from neurion_ganglion.types.capacity import Capacity

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
    """Handles execution logic."""
    return MyOutputSchema(message="Success", result=12)

# Start Ion Server
if __name__ == "__main__":
    description = "My custom Ion server"
    stake = 20000000
    fee_per_thousand_calls = 1
    capacities = [Capacity.SCRAPER, Capacity.AI_AGENT]
    Ion.create_self_hosting_ion(description, stake, fee_per_thousand_calls, capacities, my_ion_handler).start()
```

### 2. Registering an Existing Server (Server-Ready Ion)
If your Ion is already running and accessible, you can register it without hosting a new server.

```python
from neurion_ganglion.ion.ion import Ion
from neurion_ganglion.types.capacity import Capacity
from pydantic import BaseModel

# Define Input Schema
class MyInputSchema(BaseModel):
    task_id: str
    parameters: int

# Define Output Schema
class MyOutputSchema(BaseModel):
    message: str
    result: float

# Register an existing Ion
if __name__ == "__main__":
    description = "My external Ion server"
    stake = 20000000
    fee_per_thousand_calls = 1
    capacities = [Capacity.SCRAPER, Capacity.AI_AGENT]
    endpoints = ["http://167.99.69.198:8000"]
    Ion.create_server_ready_ion(description, stake, fee_per_thousand_calls, capacities, MyInputSchema, MyOutputSchema, endpoints).register_ion()
```

## Health Check
All Ions expose a `/health` endpoint that can be used to check their availability.

```sh
curl http://localhost:8000/health
```

## License
This project is licensed under the MIT License.

