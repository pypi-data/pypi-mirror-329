#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""xray RegScale integration"""
from datetime import datetime
from os import PathLike

import click
from pathlib import Path

from regscale.core.app.application import Application
from regscale.core.app.utils.file_utils import download_from_s3
from regscale.exceptions import ValidationException
from regscale.models.integration_models.flat_file_importer import FlatFileImporter
from regscale.models.integration_models.xray import XRay


@click.group()
def xray():
    """Performs actions on xray files."""


@xray.command(name="import_xray")
@FlatFileImporter.common_scanner_options(
    message="File path to the folder containing JFrog XRay .json files to process to RegScale.",
    prompt="File path for JFrog XRay files",
    import_name="xray",
)
def import_xray(
    folder_path: PathLike[str],
    regscale_ssp_id: int,
    scan_date: datetime,
    mappings_path: Path,
    disable_mapping: bool,
    s3_bucket: str,
    s3_prefix: str,
    aws_profile: str,
) -> None:
    """
    Import JFrog XRay scans, vulnerabilities and assets to RegScale from XRay .json files
    """
    import_xray_files(
        folder_path=folder_path,
        regscale_ssp_id=regscale_ssp_id,
        scan_date=scan_date,
        mappings_path=mappings_path,
        disable_mapping=disable_mapping,
        s3_bucket=s3_bucket,
        s3_prefix=s3_prefix,
        aws_profile=aws_profile,
    )


def import_xray_files(
    folder_path: PathLike[str],
    regscale_ssp_id: int,
    scan_date: datetime,
    mappings_path: Path,
    disable_mapping: bool,
    s3_bucket: str,
    s3_prefix: str,
    aws_profile: str,
) -> None:
    """
    Function to import XRay files to RegScale as assets and vulnerabilities

    :param PathLike[str] folder_path: Path to the folder containing XRay files
    :param int regscale_ssp_id: RegScale SSP ID
    :param datetime scan_date: Scan date
    :param Path mappings_path: Path to the header mapping file
    :param bool disable_mapping: Disable mapping
    :param str s3_bucket: S3 bucket to download the files from
    :param str s3_prefix: S3 prefix to download the files from
    :param str aws_profile: AWS profile to use for S3 access
    :rtype: None
    """
    if s3_bucket:
        download_from_s3(s3_bucket, s3_prefix, folder_path, aws_profile)
    from regscale.validation.record import validate_regscale_object

    # click.types.Path to pathlib.Path
    folder_path = Path(folder_path)
    app = Application()
    if not validate_regscale_object(regscale_ssp_id, "securityplans"):
        app.logger.warning("SSP #%i is not a valid RegScale Security Plan.", regscale_ssp_id)
        return
    if len(list(folder_path.glob("*.json"))) == 0:
        app.logger.warning("No xray(JSON) files found in the specified folder.")
        return
    if not scan_date or not FlatFileImporter.check_date_format(scan_date):
        scan_date = datetime.now()
    for file in list(folder_path.glob("*.json")):
        try:
            XRay(
                name="Xray",
                file_path=str(file),
                file_type=file.suffix,
                regscale_ssp_id=regscale_ssp_id,
                scan_date=scan_date,
                mappings_path=mappings_path,
                disable_mapping=disable_mapping,
            )
        except ValidationException as e:
            app.logger.error(f"Validation error: {e}")
            continue
