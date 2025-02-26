import upath

def get_project_path() -> upath.UPath:
    """
    Get the path to this project's root directory.

    Returns
    -------
    upath.UPath
        Absolute path to this project's root directory.
    """
    project_root = upath.UPath(__file__).absolute().parent.parent.parent
    return project_root

def get_data_dir() -> upath.UPath:
    """
    Get the path to the root data directory.

    Returns
    -------
    pathlib.Path
        Absolute path to the data directory.
    """
    return get_project_path() / 'data'

def get_system_data_dir() -> upath.UPath:
    """
    Get the path to the system data directory.

    Returns
    -------
    upath.UPath
        Absolute path to the system data directory.
    """
    return upath.UPath('/var/data/articles/')