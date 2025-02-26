import random

from fastapi import FastAPI, Path, Body,Response
import requests
import uvicorn
from typing import Any

from neurionpy.synapse.config import NetworkConfig

from neurion_ganglion.blockchain.query import ion_by_ion_address, get_pathway
from neurion_ganglion.pathway.schema import transform


class GanglionServer:
    def __init__(self, *args, **kwargs):
        """Prevent direct instantiation. Must use `Ion.create()`."""
        raise RuntimeError("Use `Ion.create(handler, host, port)` to create an Ion server.")

    @classmethod
    def start(cls,config:NetworkConfig):
        """Start the Ion server."""
        self = object.__new__(cls)  # Manually create instance
        self.config=config
        self.app = FastAPI()
        self.setup_routes()
        self.run()

    def _get_public_ip(self) -> str:
        """Fetch the public IP address of this machine."""
        try:
            response = requests.get("https://api64.ipify.org?format=text", timeout=5)
            response.raise_for_status()
            return response.text.strip()
        except requests.RequestException as e:
            print(f"Error retrieving public IP: {e}")
            return None
    def setup_routes(self):
        @self.app.post("/ion/{ion_address}")
        async def ion_endpoint(
            ion_address: str = Path(..., description="Ion address"),
            body: Any = Body(...)
        ):
            ion_response=ion_by_ion_address(self.config,ion_address)
            endpoints=ion_response.ion.endpoints
            random_endpoint = random.choice(endpoints)
            response = requests.post(f"{random_endpoint}/execute", json=body)
            return Response(content=response.content, status_code=response.status_code, headers=dict(response.headers))

        @self.app.post("/pathway/{id}")
        async def pathway_endpoint(
            id: int = Path(..., description="Pathway ID"),
            body: Any = Body(...)
        ):
            pathway_response=get_pathway(self.config,id)
            ion_addresses=pathway_response.pathway.ions
            field_maps=pathway_response.pathway.field_maps
            ions=[ion_by_ion_address(self.config,ion_address).ion for ion_address in ion_addresses]
            ion_input=body
            if len(ions)==0 or ions is None:
                return Response(content="No ions available", status_code=500)

            ion_availables=[ion.available for ion in ions]
            if not all(ion_availables):
                return Response(content="Not all ions available", status_code=500)

            counter=0
            for ion in ions:
                random_endpoint = random.choice(ion.endpoints)
                response = requests.post(f"{random_endpoint}/execute", json=ion_input)
                response_object=response.json()
                ion_input=transform(response_object,field_maps[counter])
                counter+=1

            return Response(content=response.content, status_code=response.status_code, headers=dict(response.headers))

    def run(self, host="0.0.0.0", port=8000):
        ip=self._get_public_ip()
        print(f"Starting Ganglion server at {ip}:{port}")
        uvicorn.run(self.app, host=host, port=port)
