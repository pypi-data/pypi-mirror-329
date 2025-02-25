#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""IBM AppScan RegScale integration"""
from datetime import datetime
from os import PathLike

import click
from pathlib import Path

from regscale.core.app.application import Application
from regscale.core.app.utils.file_utils import download_from_s3
from regscale.models.integration_models.flat_file_importer import FlatFileImporter
from regscale.models.integration_models.ibm import AppScan
from regscale.validation.record import validate_regscale_object


@click.group()
def ibm():
    """Performs actions on IBM AppScan files."""


@ibm.command(name="import_appscan")
@FlatFileImporter.common_scanner_options(
    message="File path to the folder containing IBM AppScan .csv files to process to RegScale.",
    prompt="File path for IBM AppScan files",
    import_name="ibm_appscan",
)
def import_appscan(
    folder_path: PathLike[str],
    regscale_ssp_id: int,
    scan_date: datetime,
    mappings_path: PathLike[str],
    disable_mapping: bool,
    s3_bucket: str,
    s3_prefix: str,
    aws_profile: str,
) -> None:
    """
    Import IBM AppScan scans, vulnerabilities and assets to RegScale from IBM AppScan files
    """
    import_appscan_files(
        folder_path, regscale_ssp_id, scan_date, mappings_path, disable_mapping, s3_bucket, s3_prefix, aws_profile
    )


def import_appscan_files(
    folder_path: PathLike[str],
    regscale_ssp_id: int,
    scan_date: datetime,
    mappings_path: PathLike[str],
    disable_mapping: bool,
    s3_bucket: str,
    s3_prefix: str,
    aws_profile: str,
) -> None:
    """
    Import IBM AppScan scans, vulnerabilities and assets to RegScale from IBM AppScan files

    :param PathLike[str] folder_path: File path to the folder containing IBM AppScan .csv files to process to RegScale
    :param int regscale_ssp_id: The RegScale SSP ID
    :param datetime scan_date: The date of the scan
    :param PathLike[str] mappings_path: The path to the mappings file
    :param bool disable_mapping: Whether to disable custom mappings
    :param str s3_bucket: The S3 bucket to download the files from
    :param str s3_prefix: The S3 prefix to download the files from
    :param str aws_profile: The AWS profile to use for S3 access
    :rtype: None
    """
    if s3_bucket:
        download_from_s3(s3_bucket, s3_prefix, folder_path, aws_profile)
    app = Application()
    if not validate_regscale_object(regscale_ssp_id, "securityplans"):
        app.logger.warning("SSP #%i is not a valid RegScale Security Plan.", regscale_ssp_id)
        return
    if not scan_date or not FlatFileImporter.check_date_format(scan_date):
        scan_date = datetime.now()
    if len(list(Path(folder_path).glob("*.csv"))) == 0:
        app.logger.warning("No IBM AppScan(csv) files found in the specified folder.")
        return
    from regscale.exceptions import ValidationException

    for file in Path(folder_path).glob("*.csv"):
        try:
            AppScan(
                name="IBM AppScan",
                file_path=str(file),
                plan_id=regscale_ssp_id,
                scan_date=scan_date,
                mappings_path=mappings_path,
                disable_mapping=disable_mapping,
            )
        except ValidationException as e:
            app.logger.error(f"Validation error: {e}")
            continue
