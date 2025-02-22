# inference/__init__.py

from .local_inference import local_inference
from .live_inference import LiveInference

__all__ = ["local_inference","LiveInference"]
