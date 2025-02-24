import time
import requests
import uvicorn
import threading
from fastapi import FastAPI
from typing import Type, Callable
from pydantic import BaseModel
from functools import wraps

from neurion_ganglion.blockchain.message import register_ion
from neurion_ganglion.types.capacity import Capacity
from neurion_ganglion.types.ion_type import IonType
from neurion_ganglion.ion.schema import schema_string_for_model


# ==========================
# Decorator to Define Input/Output Schemas
# ==========================
def ion_handler(input_schema: Type[BaseModel], output_schema: Type[BaseModel]):
    """
    Decorator to register input and output schemas for Ion handlers.

    Args:
        input_schema (Type[BaseModel]): Expected input schema.
        output_schema (Type[BaseModel]): Expected output schema.
    """
    def decorator(func: Callable):
        func.input_schema = input_schema
        func.output_schema = output_schema

        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper
    return decorator


# ==========================
# Ion Server Class
# ==========================

class Ion:
    def __init__(self, *args, **kwargs):
        """Prevent direct instantiation. Must use `Ion.create()`."""
        raise RuntimeError("Use `Ion.create(handler, host, port)` to create an Ion server.")

    @classmethod
    def create_self_hosting_ion(cls,description:str,stake:int,fee_per_thousand_calls:int,capacities:[Capacity],handler: Callable):
        """
        Ion Server to dynamically handle execution tasks.

        Args:
            description (str): Description of the Ion server.
            stake (int): Stake amount required to run the Ion server.
            fee_per_thousand_calls (int): Fee charged per 1000 calls to the Ion server.
            capacities ([Capacity]): List of capacities supported by the Ion server.
            handler (Callable): Function that processes execution requests.
        """
        """Internal method to instantiate Ion (bypasses __init__)."""
        self = object.__new__(cls)  # Manually create instance


        if not hasattr(handler, "input_schema") or not hasattr(handler, "output_schema"):
            raise ValueError("Handler must be decorated with @ion_handler to specify input and output schemas.")

        port = 8000
        self.description = description
        self.stake = stake
        self.fee_per_thousand_calls = fee_per_thousand_calls
        self.capacities = capacities
        self.handler = handler
        self.input_schema = handler.input_schema
        self.output_schema = handler.output_schema
        self.host = ['0.0.0.0']
        self.port = [port]
        self.mode = IonType.ION_TYPE_AUTO_REGISTERED
        self.endpoints= [f"http://{self._get_public_ip()}:{port}"]

        self.app = FastAPI()
        self._setup_routes()


        self.running = False  # Flag to track if the main server is running
        return self

    @classmethod
    def create_server_ready_ion(cls, description: str, stake: int, fee_per_thousand_calls: int, capacities: [Capacity],input_schema: Type[BaseModel], output_schema: Type[BaseModel],endpoints:[str]):
        """
        Ion Server to dynamically handle execution tasks.

        Args:
            description (str): Description of the Ion server.
            stake (int): Stake amount required to run the Ion server.
            fee_per_thousand_calls (int): Fee charged per 1000 calls to the Ion server.
            capacities ([Capacity]): List of capacities supported by the Ion server.
            input_schema (Type[BaseModel]): Expected input schema.
            output_schema (Type[BaseModel]): Expected output schema.
            endpoints ([str]): List of endpoints supported by the Ion server.
        """
        """Internal method to instantiate Ion (bypasses __init__)."""
        self = object.__new__(cls)  # Manually create instance

        self.description = description
        self.stake = stake
        self.fee_per_thousand_calls = fee_per_thousand_calls
        self.capacities = capacities
        self.input_schema = input_schema
        self.output_schema = output_schema
        self.mode = IonType.ION_TYPE_POST_REGISTERED
        self.endpoints = endpoints

        self.app = FastAPI()
        self._setup_routes()

        self.running = False  # Flag to track if the main server is running
        return self

    def _setup_routes(self):
        """Automatically register `/execute` with correct schemas."""
        @self.app.get("/health")
        def health_check():
            """Health check endpoint."""
            return {"status": "healthy"}

        @self.app.post("/execute", response_model=self.output_schema)
        async def execute_task(data: self.input_schema):
            """Handle execution request."""
            return self.handler(data)

    def _get_public_ip(self) -> str:
        """Fetch the public IP address of this machine."""
        try:
            response = requests.get("https://api64.ipify.org?format=text", timeout=5)
            response.raise_for_status()
            return response.text.strip()
        except requests.RequestException as e:
            print(f"Error retrieving public IP: {e}")
            return None

    def _is_ip_accessible(self) -> bool:
        """Check if the public IP is externally accessible."""
        public_ip = self._get_public_ip()
        if not public_ip:
            return False
        try:
            response = requests.get(f"http://{public_ip}:{self.port}/health", timeout=5)
            return response.status_code == 200
        except requests.RequestException:
            return False

    def _run_server(self):
        """Run the Uvicorn server inside the main thread and handle crashes."""
        while True:  # Ensure it retries indefinitely if it crashes
            try:
                print("Starting Uvicorn server...")
                uvicorn.run(self.app, host=self.host[0], port=self.port[0])
            except Exception as e:
                print(f"Unexpected server error: {e}")
                time.sleep(5)  # Wait before restarting
                print("Restarting server...")

    def _check_endpoints_health(self,health_path="/health", timeout=5):
        """
        Checks the health of multiple endpoints by sending a GET request to the /health path.

        Args:
            endpoints (list): List of endpoint base URLs (e.g., ["http://localhost:8000"]).
            health_path (str): The health check path (default is "/health").
            timeout (int): Timeout for the request in seconds (default is 5).

        Raises:
            RuntimeError: If any endpoint is not accessible or returns a non-healthy status.
        """
        print(self.endpoints)
        for endpoint in self.endpoints:
            health_url = f"{endpoint.rstrip('/')}{health_path}"
            try:
                response = requests.get(health_url, timeout=timeout)
                if response.status_code != 200:
                    raise RuntimeError(f"Health check failed for {endpoint}. Status Code: {response.status_code}")
                print(f"{endpoint} is healthy.")
            except requests.RequestException as e:
                raise RuntimeError(f"Error checking {endpoint}: {e}")

    def register_ion(self):
        """Register the Ion server with the central registry."""
        # Check if all endpoints are healthy
        # self._check_endpoints_health()
        print("Registering Ion to Neurion...")
        if not self.description:
            raise ValueError("Description, stake, fee, and capacities must be defined.")
        if not self.stake:
            raise ValueError("Stake must be defined.")
        if not self.fee_per_thousand_calls:
            raise ValueError("Fee per thousand calls must be defined.")
        if not self.capacities:
            raise ValueError("Capacities must be defined.")
        if not self.input_schema or not self.output_schema:
            raise ValueError("Input and output schemas must be defined.")
        if not self.endpoints:
            raise ValueError("Endpoints must be defined.")
        print(f"Description: {self.description}")
        print(f"Stake: {self.stake}")
        print(f"Fee per 1000 calls: {self.fee_per_thousand_calls}")
        print(f"Capacities: {self.capacities}")
        input_schema = schema_string_for_model(self.input_schema)
        output_schema = schema_string_for_model(self.output_schema)
        print(f"Input Schema: {input_schema}")
        print(f"Output Schema: {output_schema}")
        print(f"Endpoints: {self.endpoints}")
        register_ion(capacities=self.capacities, stake=self.stake, endpoints=self.endpoints, description=self.description,
                     fee_per_thousand_calls=self.fee_per_thousand_calls,input_schema=input_schema,output_schema=output_schema)

    def start(self):
        if self.mode == IonType.ION_TYPE_AUTO_REGISTERED:
            """Start the Ion server in the main thread with auto-recovery monitoring."""
            print("Starting Ion server...")

            # Start Uvicorn server in the main thread
            server_thread = threading.Thread(target=self._run_server, daemon=True)
            server_thread.start()

            # Wait for server to become accessible
            for _ in range(10):  # Check for up to 10 seconds
                if self._is_ip_accessible():
                    print("Server is accessible. Running normally.")
                    self.running = True
                    break
                time.sleep(1)
            else:
                print("Server failed to start. Exiting.")
                exit(1)
            self.register_ion()  # Register the Ion server
            # Keep the main thread alive
            server_thread.join()
        else:
            raise ValueError("Invalid Ion mode. Must be AUTO_REGISTERED.")