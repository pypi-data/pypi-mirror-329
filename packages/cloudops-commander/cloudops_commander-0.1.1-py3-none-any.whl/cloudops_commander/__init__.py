"""
CloudOps Commander

A package that simplifies cloud deployments, automates CI/CD pipelines, and monitors microservices.
"""

from .deploy import deploy
from .monitor import watch
from .cli import main as cli_main
from .iac import generate_terraform_config, generate_cloudformation_config
from .config import DEFAULT_REGION, DEFAULT_CLOUD_PROVIDER

__all__ = [
    "deploy",
    "watch",
    "cli_main",
    "generate_terraform_config",
    "generate_cloudformation_config",
    "DEFAULT_REGION",
    "DEFAULT_CLOUD_PROVIDER",
]
__version__ = "0.1.0"