"""AWS resource inventory collection module."""

from typing import Dict, Any, Optional

from .base import BaseCollector
from .resources.compute import ComputeCollector
from .resources.containers import ContainerCollector
from .resources.database import DatabaseCollector
from .resources.integration import IntegrationCollector
from .resources.networking import NetworkingCollector
from .resources.security import SecurityCollector
from .resources.storage import StorageCollector


class AWSInventoryCollector:
    """Collects inventory of AWS resources."""

    def __init__(
        self,
        region: str = "us-east-1",
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
    ):
        """
        Initialize the AWS inventory collector.

        :param str region: AWS region to collect inventory from
        :param str aws_access_key_id: Optional AWS access key ID
        :param str aws_secret_access_key: Optional AWS secret access key
        """
        import boto3

        self.region = region
        self.session = boto3.Session(
            aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region
        )

        # Initialize collectors
        self.compute = ComputeCollector(self.session, self.region)
        self.storage = StorageCollector(self.session, self.region)
        self.database = DatabaseCollector(self.session, self.region)
        self.networking = NetworkingCollector(self.session, self.region)
        self.security = SecurityCollector(self.session, self.region)
        self.integration = IntegrationCollector(self.session, self.region)
        self.containers = ContainerCollector(self.session, self.region)

    def collect_all(self) -> Dict[str, Any]:
        """
        Collect all AWS resources.

        :return: Dictionary containing all AWS resource information
        :rtype: Dict[str, Any]
        """
        inventory = {}

        # Collect compute resources
        compute_resources = self.compute.collect()
        inventory.update(compute_resources)

        # Collect storage resources
        storage_resources = self.storage.collect()
        inventory.update(storage_resources)

        # Collect database resources
        database_resources = self.database.collect()
        inventory.update(database_resources)

        # Collect networking resources
        networking_resources = self.networking.collect()
        inventory.update(networking_resources)

        # Collect security resources
        security_resources = self.security.collect()
        inventory.update(security_resources)

        # Collect integration resources
        integration_resources = self.integration.collect()
        inventory.update(integration_resources)

        # Collect container resources
        container_resources = self.containers.collect()
        inventory.update(container_resources)

        return inventory


def collect_all_inventory(
    region: str = "us-east-1", aws_access_key_id: Optional[str] = None, aws_secret_access_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Collect inventory of all AWS resources.

    :param str region: AWS region to collect inventory from
    :param str aws_access_key_id: Optional AWS access key ID
    :param str aws_secret_access_key: Optional AWS secret access key
    :return: Dictionary containing all AWS resource information
    :rtype: Dict[str, Any]
    """
    collector = AWSInventoryCollector(region, aws_access_key_id, aws_secret_access_key)
    return collector.collect_all()
