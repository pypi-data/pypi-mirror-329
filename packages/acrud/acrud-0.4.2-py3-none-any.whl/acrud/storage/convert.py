# standard imports
from typing import Type
from io import BytesIO
import os
from urllib.parse import urlparse

# package imports
from multimethod import multidispatch

# local imports
from ..settings import (
    SUPPORTS_CSV,
    SUPPORTS_JSON,
    SUPPORTS_PICKLE,
    SUPPORTS_PDF,
)

# Conditional imports dependent on supported file types
if SUPPORTS_PDF:
    from PyPDF2 import PdfReader, PdfWriter
if SUPPORTS_JSON:
    import json
if SUPPORTS_PICKLE:
    import dill


def get_file_path_extension(file_path: str) -> str:
    """
    Get the extension of the file path.
    """
    return file_path.split(".")[-1]


def get_url_extension(url: str) -> str:
    """
    Get the extension of the URL.
    """
    # Parse the URL to get the path component
    parsed_url = urlparse(url)
    # Extract the file path
    file_path = parsed_url.path
    # Get just the filename from the path
    filename = os.path.basename(file_path)
    # Get the extension without the dot (e.g., "txt")
    _, extension = os.path.splitext(filename)
    return extension.replace(".", "")


def get_type(key: str) -> Type:
    """
    Get the type of the file based on the file extension.
    """
    if key.startswith("http"):
        file_type = get_url_extension(key)
    else:
        file_type = get_file_path_extension(key)
    match file_type:
        case "txt":
            return str
        case "csv":
            return str
        case "json":
            return dict
        case "pkl":
            return object
        case "pdf":
            return PdfReader


@multidispatch
def convert(data, return_type):
    raise NotImplementedError(
        f"Automatic conversion from {data.__class__} to {return_type} is not yet supported."
    )


if SUPPORTS_CSV:

    # Conversion to bytes
    @convert.register
    def _(data: str, return_type: Type[bytes]):
        # Convert CSV (string) to bytes
        return data.encode("utf-8")

    # Conversion from bytes
    @convert.register
    def _(data: bytes, return_type: Type[str]):
        # Convert bytes to CSV (string)
        return data.decode("utf-8")


if SUPPORTS_JSON:

    @convert.register
    def _(data: dict, return_type: Type[bytes]):
        # Convert JSON (dict) to bytes
        return json.dumps(data).encode("utf-8")

    @convert.register
    def _(data: bytes, return_type: Type[dict]):
        # Convert bytes to JSON (dict)
        return json.loads(data.decode("utf-8"))


if SUPPORTS_PICKLE:

    @convert.register
    def _(data: bytes, return_type: Type[object]):
        # Pickle is already in bytes, return as is
        return data

    @convert.register
    def _(data: object, return_type: Type[bytes]):
        # Convert object to bytes using pickle
        buffer = BytesIO()
        dill.dump(data, buffer)
        buffer.seek(0)
        return buffer.getvalue()


if SUPPORTS_PDF:

    @convert.register
    def _(data, return_type: Type[bytes]):
        # Convert PdfReader to bytes
        output_buffer = BytesIO()
        pdf_writer = PdfWriter()

        # Copy all pages from the reader to the writer
        for page in data.pages:
            pdf_writer.add_page(page)

        # Copy metadata
        if data.metadata:
            pdf_writer.add_metadata(data.metadata)

        # Write to buffer
        pdf_writer.write(output_buffer)
        output_buffer.seek(0)
        return output_buffer.getvalue()

    @convert.register
    def _(data: bytes, return_type: Type[PdfReader]):
        # Convert bytes to PdfReader
        buffer = BytesIO(data)
        return PdfReader(buffer)
