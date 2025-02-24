import os
from osgeo import gdal

def get_orthomosaic_metadata(file_path):
    """
    Extracts metadata from an orthomosaic raster file.

    Args:
        file_path (str): The path to the orthomosaic file (e.g., .tif, .geotiff).

    Returns:
        dict: A dictionary containing the metadata, or None if an error occurs.
    """
    try:
        if os.path.exists(file_path):
            dataset = gdal.Open(file_path)
        elif dataset is None:
            raise Exception(f"Could not open or read the file: {file_path}")

        metadata = {}

        # Get general metadata
        metadata['driver_long_name'] = dataset.GetDriver().LongName
        metadata['raster_x_size'] = dataset.RasterXSize
        metadata['raster_y_size'] = dataset.RasterYSize
        metadata['band_count'] = dataset.RasterCount
        metadata['projection'] = dataset.GetProjection()
        metadata['geotransform'] = dataset.GetGeoTransform()
        metadata['size'] = os.path.getsize(file_path)/1000000000

        
        # Get metadata from the raster bands
        for i in range(1, dataset.RasterCount + 1):
            band = dataset.GetRasterBand(i)
            band_metadata = band.GetMetadata()
            metadata[f'band_{i}_metadata'] = band_metadata

        # Get all metadata domains
        metadata_domains = dataset.GetMetadataDomainList()
        #for domain in metadata_domains:
        #    domain_metadata = dataset.GetMetadata(domain)
        #    metadata[f'domain_{domain}'] = domain_metadata

        dataset = None  # Close the dataset
        return metadata

    except Exception as e:
        print(f"Error: {e}")
        return None

#def delete_dsstore(path, files_to_delete=(".DS_Store", "__MACOSX")):
#    """
#    Deletes all ".DS_store" files under a specified directory.
#
#    Args:
#        path (str, optional): The directory path where the ".DS_store" files should be deleted.
#        files_to_delete (tuple): The files to be deleted.
#
#    Example:
#        ```python
#        from ultralytics.utils.downloads import delete_dsstore
#
#        delete_dsstore("path/to/dir")
#        ```
#
#    Note:
#        ".DS_store" files are created by the Apple operating system and contain metadata about folders and files. They
#        are hidden system files and can cause issues when transferring files between different operating systems.
#    """
#    for file in files_to_delete:
#        matches = list(Path(path).rglob(file))
#        LOGGER.info(f"Deleting {file} files: {matches}")
#        for f in matches:
#            f.unlink()
            
#def check_disk_space(url="https://ultralytics.com/assets/coco8.zip", path=Path.cwd(), sf=1.5, hard=True):
#    """
#    Check if there is sufficient disk space to download and store a file.
#
#    Args:
#        url (str, optional): The URL to the file. Defaults to 'https://ultralytics.com/assets/coco8.zip'.
#        path (str | Path, optional): The path or drive to check the available free space on.
#        sf (float, optional): Safety factor, the multiplier for the required free space. Defaults to 1.5.
#        hard (bool, optional): Whether to throw an error or not on insufficient disk space. Defaults to True.
#
#    Returns:
#        (bool): True if there is sufficient disk space, False otherwise.
#    """
#    try:
#        r = requests.head(url)  # response
#        assert r.status_code < 400, f"URL error for {url}: {r.status_code} {r.reason}"  # check response
#    except Exception:
#        return True  # requests issue, default to True
#
#    # Check file size
#    gib = 1 << 30  # bytes per GiB
#    data = int(r.headers.get("Content-Length", 0)) / gib  # file size (GB)
#    total, used, free = (x / gib for x in shutil.disk_usage(path))  # bytes
#
#    if data * sf < free:
#        return True  # sufficient space
#
#    # Insufficient space
#    text = (
#        f"WARNING ⚠️ Insufficient free disk space {free:.1f} GB < {data * sf:.3f} GB required, "
#        f"Please free {data * sf - free:.1f} GB additional disk space and try again."
#    )
#    if hard:
#        raise MemoryError(text)
#    LOGGER.warning(text)
#    return False
