#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prisma RegScale integration"""
from datetime import datetime
from os import PathLike
from typing import Optional

import click
from pathlib import Path

from regscale.core.app.application import Application
from regscale.core.app.utils.file_utils import download_from_s3
from regscale.models.integration_models.flat_file_importer import FlatFileImporter
from regscale.models.integration_models.prisma import Prisma
from regscale.validation.record import validate_regscale_object


@click.group()
def prisma():
    """Performs actions on Prisma export files."""


@prisma.command(name="import_prisma")
@FlatFileImporter.common_scanner_options(
    message="File path to the folder containing Nexpose .csv files to process to RegScale.",
    prompt="File path for Prisma files",
    import_name="prisma",
)
def import_prisma(
    folder_path: PathLike[str],
    regscale_ssp_id: int,
    scan_date: datetime,
    mappings_path: PathLike[str],
    disable_mapping: bool,
    s3_bucket: str,
    s3_prefix: str,
    aws_profile: str,
):
    """
    Import scans, vulnerabilities and assets to RegScale from Prisma export files
    """
    import_prisma_data(
        folder_path=folder_path,
        regscale_ssp_id=regscale_ssp_id,
        scan_date=scan_date,
        mappings_path=mappings_path,
        disable_mapping=disable_mapping,
        s3_bucket=s3_bucket,
        s3_prefix=s3_prefix,
        aws_profile=aws_profile,
    )


def import_prisma_data(
    folder_path: PathLike[str],
    regscale_ssp_id: int,
    scan_date: datetime,
    s3_bucket: str,
    s3_prefix: str,
    aws_profile: str,
    mappings_path: Optional[PathLike[str]] = None,
    disable_mapping: bool = False,
) -> None:
    """
    Import Prisma data to RegScale

    :param PathLike[str] folder_path: Path to the folder containing Prisma .csv files
    :param int regscale_ssp_id: RegScale System Security Plan ID
    :param datetime scan_date: Date of the scan
    :param str s3_bucket: S3 bucket to download the files from
    :param str s3_prefix: S3 prefix to download the files from
    :param str aws_profile: AWS profile to use for S3 access
    :param Optional[Path] mappings_path: Path to the header mapping file, defaults to None
    :param bool disable_mapping: Whether to disable custom mapping, defaults to False
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
        app.logger.warning("No Prisma(csv) files found in the specified folder.")
        return
    from regscale.exceptions import ValidationException

    for file in Path(folder_path).glob("*.csv"):
        try:
            Prisma(
                name="Prisma",
                file_path=str(file),
                regscale_ssp_id=regscale_ssp_id,
                scan_date=scan_date,
                mappings_path=mappings_path,
                disable_mapping=disable_mapping,
            )
        except ValidationException as e:
            app.logger.error(f"Validation error: {e}")
            continue
