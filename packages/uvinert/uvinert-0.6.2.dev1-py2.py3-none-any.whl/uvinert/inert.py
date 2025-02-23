import os

def get_requires_for_build_wheel(config_settings=None):
    """No extra requirements."""
    return []

def build_wheel(wheel_directory, config_settings=None, metadata_directory=None):
    """
    Create a dummy wheel file.
    Returns the filename of the created wheel.
    """
    wheel_name = "dummy_inert-0.0.0-py3-none-any.whl"
    wheel_path = os.path.join(wheel_directory, wheel_name)
    # Create an empty file as a placeholder.
    with open(wheel_path, "wb") as f:
        f.write(b"")
    return wheel_name

def prepare_metadata_for_build_wheel(metadata_directory, config_settings=None):
    """
    Create a dummy .dist-info directory with minimal METADATA.
    Returns the name of the created .dist-info directory.
    """
    dist_info_name = "dummy_inert-0.0.0.dist-info"
    dist_info_path = os.path.join(metadata_directory, dist_info_name)
    os.makedirs(dist_info_path, exist_ok=True)
    metadata_file = os.path.join(dist_info_path, "METADATA")
    with open(metadata_file, "w", encoding="utf-8") as f:
        f.write("Metadata-Version: 2.1\nName: dummy_inert\nVersion: 0.0.0\n")
    return dist_info_name

def get_requires_for_build_sdist(config_settings=None):
    """No extra requirements for sdist."""
    return []

def build_sdist(sdist_directory, config_settings=None):
    """
    Create a dummy sdist archive.
    Returns the filename of the created archive.
    """
    sdist_name = "dummy_inert-0.0.0.tar.gz"
    sdist_path = os.path.join(sdist_directory, sdist_name)
    # Create an empty file as a placeholder.
    with open(sdist_path, "wb") as f:
        f.write(b"")
    return sdist_name
