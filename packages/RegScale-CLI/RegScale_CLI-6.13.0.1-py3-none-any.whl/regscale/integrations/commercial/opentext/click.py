"""
This module contains the Click commands for the opentext integration.
"""

# pylint: disable=W0621

from datetime import datetime
from os import PathLike
from typing import Optional

import click
from pathlib import Path

from regscale.core.app.application import Application
from regscale.core.app.utils.file_utils import download_from_s3
from regscale.integrations.commercial.opentext.scanner import WebInspect
from regscale.models.integration_models.flat_file_importer import FlatFileImporter
from regscale.validation.record import validate_regscale_object


@click.group()
def fortify():
    """Performs actions on the OpenText Fortify"""


@fortify.group(name="web_inspect")
def web_inspect():
    """Performs actions on the OpenText Web Inspect files."""


@web_inspect.command(name="import_file")
@FlatFileImporter.common_scanner_options(
    message="File path to the folder containing Fortify WebInspect .xml files to process to RegScale.",
    prompt="File path for Web Inspect files",
    import_name="web_inspect",
)
def import_file(
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
    Import and process a folder of Fortify WebInspect XML file(s).
    """
    import_opentext_file(
        folder_path=folder_path,
        regscale_ssp_id=regscale_ssp_id,
        scan_date=scan_date,
        mappings_path=mappings_path,
        disable_mapping=disable_mapping,
        s3_bucket=s3_bucket,
        s3_prefix=s3_prefix,
        aws_profile=aws_profile,
    )


def import_opentext_file(
    folder_path: PathLike[str],
    regscale_ssp_id: int,
    scan_date: datetime,
    mappings_path: Optional[Path] = None,
    disable_mapping: Optional[bool] = False,
    s3_bucket: Optional[str] = None,
    s3_prefix: Optional[str] = None,
    aws_profile: Optional[str] = None,
) -> None:
    """
    Import and process a folder of Fortify WebInspect XML file(s).

    :param click.Path folder_path: The Path to a folder of XML file(s) to import
    :param int regscale_ssp_id: RegScale SSP ID
    :param datetime scan_date: The date of the scan
    :param Optional[Path] mappings_path: Path to the header mapping file, default: None
    :param Optional[bool] disable_mapping: Disable the header mapping, default: False
    :param Optional[str] s3_bucket: S3 bucket to download scan files from, default: None
    :param Optional[str] s3_prefix: Prefix (folder path) within the S3 bucket, default: None
    :param Optional[str] aws_profile: AWS profile to use for S3 access, default: None
    :return: None
    """
    if s3_bucket:
        download_from_s3(s3_bucket, s3_prefix, folder_path, aws_profile)
    app = Application()
    if not validate_regscale_object(regscale_ssp_id, "securityplans"):
        app.logger.warning("SSP #%i is not a valid RegScale Security Plan.", regscale_ssp_id)
        return
    if not scan_date or not FlatFileImporter.check_date_format(scan_date):
        scan_date = datetime.now()
    file_list = list(Path(folder_path).glob("*.xml"))  # Support Veracode file format
    if len(file_list) == 0:
        app.logger.warning("No Fortify WebInspect files found in the specified folder.")
        return
    from regscale.exceptions import ValidationException

    for file in file_list:
        try:
            WebInspect(
                name="Web Inspect",
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
            app.logger.error(f"Validation error on file {file}: {e}")
            continue
