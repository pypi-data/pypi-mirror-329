import os
import tarfile
import zipfile

def get_requires_for_build_wheel(config_settings=None):
    return []

def build_wheel(wheel_directory, config_settings=None, metadata_directory=None):
    """
    Create a minimal valid wheel file.
    Returns the filename of the created wheel.
    """
    wheel_name = "dummy_inert-0.0.0-py3-none-any.whl"
    wheel_path = os.path.join(wheel_directory, wheel_name)
    
    # Create a minimal wheel (a ZIP file with a WHEEL file inside)
    with zipfile.ZipFile(wheel_path, "w") as z:
        # Define the .dist-info directory name
        dist_info = "dummy_inert-0.0.0.dist-info"
        wheel_info_path = f"{dist_info}/WHEEL"
        # Write minimal wheel metadata
        wheel_metadata = (
            "Wheel-Version: 1.0\n"
            "Generator: uv.inert\n"
            "Root-Is-Purelib: true\n"
            "Tag: py3-none-any\n"
        )
        z.writestr(wheel_info_path, wheel_metadata)
    return wheel_name

def prepare_metadata_for_build_wheel(metadata_directory, config_settings=None):
    dist_info_name = "dummy_inert-0.0.0.dist-info"
    dist_info_path = os.path.join(metadata_directory, dist_info_name)
    os.makedirs(dist_info_path, exist_ok=True)
    metadata_file = os.path.join(dist_info_path, "METADATA")
    with open(metadata_file, "w", encoding="utf-8") as f:
        f.write("Metadata-Version: 2.1\nName: dummy_inert\nVersion: 0.0.0\n")
    return dist_info_name

def get_requires_for_build_sdist(config_settings=None):
    return []

def build_sdist(sdist_directory, config_settings=None):
    """
    Create a minimal valid sdist archive.
    Returns the filename of the created archive.
    """
    sdist_name = "dummy_inert-0.0.0.tar.gz"
    sdist_path = os.path.join(sdist_directory, sdist_name)
    
    # Create a minimal tar.gz archive containing a dummy file.
    dummy_filename = "DUMMY"
    dummy_file_path = os.path.join(sdist_directory, dummy_filename)
    
    # Write a simple text file to include in the archive.
    with open(dummy_file_path, "w", encoding="utf-8") as f:
        f.write("This is a dummy sdist for inert backend.")
    
    # Create a valid tar.gz archive including the dummy file.
    with tarfile.open(sdist_path, "w:gz") as tar:
        tar.add(dummy_file_path, arcname=dummy_filename)
    
    # Clean up the temporary dummy file.
    os.remove(dummy_file_path)
    
    return sdist_name
