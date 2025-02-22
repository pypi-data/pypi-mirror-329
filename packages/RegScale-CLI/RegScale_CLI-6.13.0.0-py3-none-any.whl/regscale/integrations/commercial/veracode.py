#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Veracode RegScale integration"""
from datetime import datetime
from os import PathLike
from typing import Optional

import click
from pathlib import Path

from regscale.core.app.application import Application
from regscale.core.app.utils.file_utils import download_from_s3
from regscale.models.integration_models.flat_file_importer import FlatFileImporter
from regscale.models.integration_models.veracode import Veracode
from regscale.validation.record import validate_regscale_object


@click.group()
def veracode():
    """Performs actions on Veracode export files."""


FlatFileImporter.show_mapping(
    group=veracode,
    import_name="veracode",
)


@veracode.command(name="import_veracode")
@FlatFileImporter.common_scanner_options(
    message="File path to the folder containing Veracode .xlsx files to process to RegScale.",
    prompt="File path for Veracode files",
    import_name="veracode",
)
def import_veracode(
    folder_path: PathLike[str],
    regscale_ssp_id: int,
    scan_date: datetime,
    mappings_path: Path,
    disable_mapping: bool,
    s3_bucket: str,
    s3_prefix: str,
    aws_profile: str,
):
    """
    Import scans, vulnerabilities and assets to RegScale from Veracode export files
    """
    import_veracode_data(
        folder_path=folder_path,
        regscale_ssp_id=regscale_ssp_id,
        scan_date=scan_date,
        mappings_path=mappings_path,
        disable_mapping=disable_mapping,
        s3_bucket=s3_bucket,
        s3_prefix=s3_prefix,
        aws_profile=aws_profile,
    )


def import_veracode_data(
    folder_path: PathLike[str],
    regscale_ssp_id: int,
    scan_date: datetime,
    mappings_path: Path,
    s3_bucket: str,
    s3_prefix: str,
    aws_profile: str,
    disable_mapping: Optional[bool] = False,
) -> None:
    """Import scans, vulnerabilities and assets to RegScale from Veracode export files"

    :param os.PathLike[str] folder_path: Path to the folder containing Veracode files
    :param int regscale_ssp_id: RegScale SSP ID
    :param datetime scan_date: Scan date
    :param os.PathLike[str] mappings_path: Path to the header mapping file
    :param str s3_bucket: S3 bucket to download the files from
    :param str s3_prefix: S3 prefix to download the files from
    :param str aws_profile: AWS profile to use for S3 access
    :param bool disable_mapping: Disable mapping
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
    xml_file_list = list(Path(folder_path).glob("*.xml"))  # Support Veracode file format
    csv_file_list = list(Path(folder_path).glob("*.xlsx"))  # Support Coalfire Excel format
    file_list = xml_file_list + csv_file_list
    if len(file_list) == 0:
        app.logger.warning("No Veracode files found in the specified folder.")
        return
    from regscale.exceptions import ValidationException

    for file in file_list:
        try:
            Veracode(
                name="Veracode",
                app=app,
                file_path=str(file),
                file_type=file.suffix,
                parent_id=regscale_ssp_id,
                parent_module="securityplans",
                scan_date=scan_date,
                mappings_path=mappings_path,
                disable_mapping=disable_mapping,
            )
        except ValidationException as e:
            app.logger.error(f"Validation error: {e}")
            continue
