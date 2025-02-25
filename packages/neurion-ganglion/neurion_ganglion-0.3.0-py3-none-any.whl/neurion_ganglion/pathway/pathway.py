import random
import time
import requests
import uvicorn
import threading
from fastapi import FastAPI, Request, HTTPException, Depends
from typing import Type, Callable

from neurionpy.synapse.config import NetworkConfig
from pydantic import BaseModel
from functools import wraps
from google.protobuf.json_format import MessageToDict
from neurion_ganglion.blockchain.message import register_ion
from neurion_ganglion.blockchain.query import get_allowed_ips, ion_by_ion_address, get_pathway
from neurion_ganglion.blockchain.wallet import get_wallet
from neurion_ganglion.custom_types.capacity import Capacity
from neurion_ganglion.custom_types.ion_type import IonType
from neurion_ganglion.ion.schema import schema_string_for_model

# ==========================
# Pathway Class
# ==========================

class Pathway:
    def __init__(self, *args, **kwargs):
        """Prevent direct instantiation. Must use `Pathway.of()`."""
        raise RuntimeError("Use `Pathway.of(id)` to create an Pathway.")

    @classmethod
    def of_id(cls,config:NetworkConfig,id: int):
        """
        Pathway to dynamically handle execution tasks.

        Args:
            config (NetworkConfig): Network configuration.
            id (int): ID of the Pathway.
        """
        pathway_response=get_pathway(config,id)
        pathway=pathway_response.pathway
        pathway_dict = MessageToDict(pathway)
        self = object.__new__(cls)  # Manually create instance
        for key, value in pathway_dict.items():
            setattr(self, key, value)
        self.config=config
        return self

    def call(self,body: dict):
        print("Calling Ganglion server...")
        # Get the ganglion server addresss
        ips_response=get_allowed_ips(self.config)
        ip=random.choice(ips_response.ips)
        # get the endpoint of the ganglion server
        ganglion_server_endpoint=f"http://{ip}:8000"
        response = requests.post(f"{ganglion_server_endpoint}/pathway/{self.id}", json=body)
        return response.json()