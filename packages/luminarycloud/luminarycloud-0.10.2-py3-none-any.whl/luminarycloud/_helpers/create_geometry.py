# Copyright 2024 Luminary Cloud, Inc. All Rights Reserved.
from luminarycloud._proto.api.v0.luminarycloud.geometry import geometry_pb2 as geometrypb
from luminarycloud._proto.upload import upload_pb2 as uploadpb
from os import PathLike
from .._client import Client
from .upload import upload_file
from typing import Any, Optional
from luminarycloud._helpers import util

import logging

logger = logging.getLogger(__name__)


def create_geometry(
    client: Client,
    cad_file_path: PathLike,
    project_id: str,
    *,
    name: Optional[str] = None,
    scaling: Optional[float] = None,
    wait: bool = False,
) -> geometrypb.Geometry:

    cad_file_meta = util.get_file_metadata(cad_file_path)
    logger.info(
        f"creating geometry in {project_id} by uploading file: {cad_file_meta.name}.{cad_file_meta.ext}, "
        + f"size: {cad_file_meta.size} bytes, sha256: {cad_file_meta.sha256_checksum}, "
        + f"crc32c: {cad_file_meta.crc32c_checksum}"
    )

    finish_res = upload_file(
        client,
        project_id,
        uploadpb.ResourceParams(geometry_params=uploadpb.GeometryParams()),
        cad_file_path,
    )[1]

    # create geometry
    if name is None:
        # if the caller did not provide a name, use the file name
        name = cad_file_meta.name
    if scaling is None:
        # default to no scaling
        scaling = 1.0
    create_geo_res: geometrypb.CreateGeometryResponse = client.CreateGeometry(
        geometrypb.CreateGeometryRequest(
            project_id=project_id, name=name, url=finish_res.url, scaling=scaling, wait=wait
        )
    )
    geo = create_geo_res.geometry
    logger.info(f"created geometry {geo.name} ({geo.id})")
    return geo
