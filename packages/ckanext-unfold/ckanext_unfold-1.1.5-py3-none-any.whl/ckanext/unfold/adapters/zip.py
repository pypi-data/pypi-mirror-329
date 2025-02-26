from __future__ import annotations

import logging
from datetime import datetime as dt
from io import BytesIO
from typing import Any, Optional
from zipfile import BadZipFile, LargeZipFile, ZipFile, ZipInfo

import requests

import ckan.plugins.toolkit as tk

import ckanext.unfold.exception as unf_exception
import ckanext.unfold.types as unf_types
import ckanext.unfold.utils as unf_utils

log = logging.getLogger(__name__)


def build_directory_tree(
    filepath: str, resource_view: dict[str, Any], remote: Optional[bool] = False
) -> list[unf_types.Node]:
    try:
        if remote:
            file_list = get_ziplist_from_url(filepath)
        else:
            with ZipFile(filepath) as archive:
                # zip format do not support encrypted filenames so we don't have
                # to check for pass protection, we have enough information from
                # `infolist` method

                file_list: list[ZipInfo] = archive.infolist()
    except (LargeZipFile, BadZipFile) as e:
        raise unf_exception.UnfoldError(f"Error openning archive: {e}")
    except requests.RequestException as e:
        raise unf_exception.UnfoldError(f"Error fetching remote archive: {e}")

    nodes: list[unf_types.Node] = []

    for entry in file_list:
        nodes.append(_build_node(entry))

    return nodes


def _build_node(entry: ZipInfo) -> unf_types.Node:
    parts = [p for p in entry.filename.split("/") if p]
    name = unf_utils.name_from_path(entry.filename)
    fmt = "folder" if entry.is_dir() else unf_utils.get_format_from_name(name)

    return unf_types.Node(
        id=entry.filename or "",
        text=unf_utils.name_from_path(entry.filename),
        icon="fa fa-folder" if entry.is_dir() else unf_utils.get_icon_by_format(fmt),
        state={"opened": True},
        parent="/".join(parts[:-1]) + "/" if parts[:-1] else "#",
        data=_prepare_table_data(entry),
    )


def _prepare_table_data(entry: ZipInfo) -> dict[str, Any]:
    name = unf_utils.name_from_path(entry.filename)
    fmt = "" if entry.is_dir() else unf_utils.get_format_from_name(name)
    modified_at = tk.h.render_datetime(
        dt(*entry.date_time), date_format=unf_utils.DEFAULT_DATE_FORMAT
    )

    return {
        "size": unf_utils.printable_file_size(entry.compress_size)
        if entry.compress_size
        else "",
        "type": "folder" if entry.is_dir() else "file",
        "format": fmt,
        "modified_at": modified_at or "--",
    }


def get_ziplist_from_url(url) -> list[ZipInfo]:
    head = requests.head(url)
    end = None

    if "content-length" in head.headers:
        end = int(head.headers["content-length"])

    if "content-range" in head.headers:
        end = int(head.headers["content-range"].split("/")[1])

    if not end:
        return []

    return _get_remote_zip_infolist(url, end - 65536, end)


def _get_remote_zip_infolist(url: str, start, end) -> list[ZipInfo]:
    resp = requests.get(
        url,
        headers={
            "Range": "bytes={}-{}".format(start, end),
        },
        timeout=unf_utils.DEFAULT_TIMEOUT,
    )

    return ZipFile(BytesIO(resp.content)).infolist()
