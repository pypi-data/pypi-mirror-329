"""AWS CLI integration module."""

import click
import json
import logging
import os
from typing import Optional


logger = logging.getLogger("rich")


@click.group()
def awsv2():
    """AWS Integrations."""
    pass


@awsv2.command(name="sync_assets")
@click.option(
    "--region",
    type=str,
    default="us-east-1",
    help="AWS region to collect inventory from",
)
@click.option(
    "--regscale_id",
    "--id",
    type=click.INT,
    help="RegScale will create and update assets as children of this record.",
    required=True,
)
@click.option(
    "--regscale_module",
    "-m",
    type=click.STRING,
    help="RegScale module to push inventory to (e.g., securityplans).",
    default="securityplans",
    required=True,
)
@click.option(
    "--aws_access_key_id",
    type=str,
    required=False,
    help="AWS access key ID",
    envvar="AWS_ACCESS_KEY_ID",
)
@click.option(
    "--aws_secret_access_key",
    type=str,
    required=False,
    help="AWS secret access key",
    envvar="AWS_SECRET_ACCESS_KEY",
)
def sync_assets(
    region: str,
    regscale_id: int,
    regscale_module: str,
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
) -> None:
    """
    Sync AWS resources to RegScale assets.

    This command collects AWS resources and creates/updates corresponding assets in RegScale:
    - EC2 instances
    - S3 buckets
    - RDS instances
    - Lambda functions
    - DynamoDB tables
    - VPCs and networking resources
    - Container resources
    - And more...
    """
    try:
        logger.info("Starting AWS asset sync to RegScale...")
        from .scanner import AWSInventoryIntegration

        scanner = AWSInventoryIntegration(plan_id=regscale_id)
        scanner.sync_assets(
            plan_id=regscale_id,
            region=region,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )
        logger.info("AWS asset sync completed successfully.")
    except Exception as e:
        logger.error(f"Error syncing AWS assets: {e}", exc_info=True)
        raise click.ClickException(str(e))


@awsv2.group()
def inventory():
    """AWS resource inventory commands."""
    pass


@inventory.command(name="collect")
@click.option(
    "--region",
    type=str,
    default="us-east-1",
    help="AWS region to collect inventory from",
)
@click.option(
    "--aws_access_key_id",
    type=str,
    required=False,
    help="AWS access key ID",
    envvar="AWS_ACCESS_KEY_ID",
)
@click.option(
    "--aws_secret_access_key",
    type=str,
    required=False,
    help="AWS secret access key",
    envvar="AWS_SECRET_ACCESS_KEY",
)
@click.option(
    "--output",
    type=click.Path(dir_okay=False, writable=True),
    help="Output file path (JSON format)",
    required=False,
)
def collect_inventory(
    region: str,
    aws_access_key_id: Optional[str],
    aws_secret_access_key: Optional[str],
    output: Optional[str],
) -> None:
    """
    Collect AWS resource inventory.

    This command collects information about various AWS resources including:
    - EC2 instances
    - S3 buckets
    - RDS instances
    - Lambda functions
    - And more...

    The inventory can be displayed to stdout or saved to a JSON file.
    """
    try:
        from .inventory.base import DateTimeEncoder
        from .inventory import collect_all_inventory

        inventory = collect_all_inventory(
            region=region,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )

        if output:
            with open(output, "w") as f:
                json.dump(inventory, f, indent=2)
            logger.info(f"Inventory saved to {output}")
        else:
            click.echo(json.dumps(inventory, indent=2, cls=DateTimeEncoder))

    except Exception as e:
        logger.error(f"Error collecting AWS inventory: {e}")
        raise click.ClickException(str(e))


@awsv2.group(help="Sync AWS Inspector Scans to RegScale.")
def inspector():
    """Sync AWS Inspector scans."""


@awsv2.command(name="sync_findings")
@click.option(
    "--regscale_ssp_id",
    type=click.INT,
    required=True,
    prompt="Enter RegScale System Security Plan ID",
    help="The ID number from RegScale of the System Security Plan",
)
@click.option(
    "--create_issue",
    type=click.BOOL,
    required=False,
    help="Create Issue in RegScale from vulnerabilities in AWS Security Hub.",
    default=False,
)
@click.option(
    "--aws_access_key_id",
    "--key_id",
    type=click.STRING,
    required=False,
    help="AWS Access Key ID",
    default=os.environ.get("AWS_ACCESS_KEY_ID"),
)
@click.option(
    "--aws_secret_access_key",
    "--key",
    type=click.STRING,
    required=False,
    help="AWS Secret Access Key",
    default=os.environ.get("AWS_SECRET_ACCESS_KEY"),
)
def sync_findings(
    regscale_ssp_id: int,
    create_issue: bool = False,
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
) -> None:
    """Sync AWS Security Hub Findings."""
    from regscale.integrations.commercial.amazon.common import sync_aws_findings

    sync_aws_findings(regscale_ssp_id, create_issue, aws_access_key_id, aws_secret_access_key)
